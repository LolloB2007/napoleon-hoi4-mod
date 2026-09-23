import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]

from pdx import parse,dumps,walk
from build_20_france import build as build_france
from build_21_france_decisions import build as build_decisions,postprocess,CONTINENTAL_TARGETS


class FranceDecisionMechanicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=build_france(ROOT)
        extra=build_decisions(ROOT)
        combined=base|extra
        cls.files=combined|postprocess(combined,ROOT)
        cls.decisions=parse(cls.files['common/decisions/nap_france_campaigns.txt'])
        cls.effects=parse(cls.files['common/scripted_effects/nap_france_campaigns.txt'])
        cls.effect_ids={e.key for e in cls.effects}
        cls.focuses={}
        for node in walk(parse(cls.files['common/national_focus/FRA.txt'])):
            if node.key=='focus' and isinstance(node.value,list) and node.scalar('id'):
                cls.focuses[node.scalar('id')]=node
        cls.events={}
        for path in ('events/01_french_revolution.txt','events/02_napoleonic_wars.txt','events/03_collapse.txt'):
            for event in parse(cls.files[path]):
                if event.key in ('country_event','news_event') and event.scalar('id'):
                    cls.events[event.scalar('id')]=event

    def test_scripts_parse(self):
        for path,text in self.files.items():
            if path.endswith('.txt'):
                parse(text)

    def test_six_france_categories_plus_foreign_evasion(self):
        categories={x.key for x in parse(self.files['common/decisions/categories/nap_france_campaigns.txt'])}
        self.assertEqual(categories,{
            'nap_fra_revolutionary_crisis','nap_fra_napoleon_rise',
            'nap_fra_continental_system','nap_fra_peninsular_war',
            'nap_fra_russian_campaign','nap_fra_restoration_cycle',
            'nap_continental_foreign',
        })

    def test_decision_counts_by_system(self):
        counts={cat.key:len([e for e in cat.value if isinstance(e.value,list)]) for cat in self.decisions}
        self.assertEqual(counts,{
            'nap_fra_revolutionary_crisis':13,
            'nap_fra_napoleon_rise':13,
            'nap_fra_continental_system':11,
            'nap_continental_foreign':2,
            'nap_fra_peninsular_war':7,
            'nap_fra_russian_campaign':9,
            'nap_fra_restoration_cycle':10,
        })
        self.assertEqual(sum(counts.values()),65)

    def test_every_decision_rechecks_through_scripted_effect(self):
        for category in self.decisions:
            for decision in [e for e in category.value if isinstance(e.value,list)]:
                complete=decision.children('complete_effect')
                self.assertEqual(len(complete),1,decision.key)
                calls=[e.key for e in complete[0].value if e.value=='yes']
                self.assertEqual(len(calls),1,decision.key)
                self.assertIn(calls[0],self.effect_ids,decision.key)

    def test_focuses_unlock_decisions_instead_of_auto_transitions(self):
        calls={
            'FRA_reign_of_terror_focus':'french_revolution.10',
            'FRA_brumaire_coup':'french_revolution.14',
            'FRA_proclaim_empire':'napoleonic_wars.3',
            'FRA_continental_system_focus':'napoleonic_wars.10',
            'FRA_invade_russia':'napoleonic_wars.16',
            'FRA_return_from_elba':'napoleonic_collapse.8',
        }
        for focus_id,event_id in calls.items():
            rendered=dumps(self.focuses[focus_id].children('completion_reward'))
            self.assertNotIn(event_id,rendered,focus_id)
            self.assertIn('nap_fra_',rendered,focus_id)
        iberia=dumps(self.focuses['FRA_invade_iberia'].children('completion_reward'))
        self.assertNotIn('declare_war_on',iberia)
        self.assertIn('nap_fra_peninsular_decisions_unlocked',iberia)

    def test_italy_and_egypt_complete_through_decisions(self):
        italy=dumps(self.focuses['FRA_italian_campaign'].children('completion_reward'))
        egypt=dumps(self.focuses['FRA_egyptian_expedition'].children('completion_reward'))
        self.assertNotIn('italian_campaign_won',italy)
        self.assertNotIn('egyptian_expedition_complete',egypt)
        effects=self.files['common/scripted_effects/nap_france_campaigns.txt']
        self.assertIn('set_country_flag = italian_campaign_won',effects)
        self.assertIn('set_country_flag = egyptian_expedition_complete',effects)
        self.assertIn('nap_fra_napoleon_prestige',effects)

    def test_revolution_transitions_are_decision_driven(self):
        terror=self.events['french_revolution.10']
        self.assertNotIn('french_revolution.11',dumps(terror))
        for event_id in ('french_revolution.12','french_revolution.14'):
            event=self.events[event_id]
            self.assertEqual(event.scalar('is_triggered_only'),'yes')
            self.assertFalse(event.children('mean_time_to_happen'))
        decisions=self.files['common/decisions/nap_france_campaigns.txt']
        for key in ('nap_fra_committee_public_safety','nap_fra_debate_terror',
                    'nap_fra_thermidorian_reaction','nap_fra_install_directory'):
            self.assertIn(key,decisions)

    def test_empire_and_coronation_are_separate_decisions(self):
        empire=self.events['napoleonic_wars.3']
        self.assertEqual(empire.scalar('is_triggered_only'),'yes')
        self.assertNotIn('napoleonic_wars.4',dumps(empire))
        decisions=self.files['common/decisions/nap_france_campaigns.txt']
        self.assertIn('nap_fra_proclaim_empire_decision',decisions)
        self.assertIn('nap_fra_coronation',decisions)
        self.assertIn('nap_fra_appoint_marshals',decisions)

    def test_continental_system_has_enforcement_and_evasion(self):
        text=self.files['common/decisions/nap_france_campaigns.txt']
        for tag,_ in CONTINENTAL_TARGETS:
            self.assertIn('nap_fra_continental_pressure_'+tag.lower(),text)
        self.assertIn('nap_continental_evade_customs',text)
        self.assertIn('nap_continental_enforce_locally',text)
        effects=self.files['common/scripted_effects/nap_france_campaigns.txt']
        self.assertIn('nap_british_continental_pressure',effects)
        self.assertIn('nap_continental_compliance',effects)

    def test_peninsular_war_is_resistance_and_supply_system(self):
        effects=self.files['common/scripted_effects/nap_france_campaigns.txt']
        self.assertIn('nap_fra_peninsular_resistance',effects)
        self.assertIn('target = SPR',effects)
        self.assertIn('target = POR',effects)
        self.assertIn('nap_fra_peninsular_guerrilla_war',effects)
        self.assertIn('white_peace = SPR',effects)
        self.assertIn('white_peace = POR',effects)
        self.assertNotIn('transfer_state',effects)
        self.assertNotIn('add_core_of',effects)

    def test_russian_campaign_has_preparation_attrition_and_three_outcomes(self):
        event=self.events['napoleonic_wars.13']
        self.assertEqual(event.scalar('is_triggered_only'),'yes')
        self.assertFalse(event.children('mean_time_to_happen'))
        invasion=self.events['napoleonic_wars.16']
        self.assertEqual(invasion.scalar('is_triggered_only'),'yes')
        collapse=self.events['napoleonic_collapse.1']
        self.assertEqual(collapse.scalar('is_triggered_only'),'yes')
        effects=self.files['common/scripted_effects/nap_france_campaigns.txt']
        for token in (
            'nap_fra_russia_magazines_effect','nap_fra_russia_remounts_effect',
            'nap_fra_russia_allies_effect','nap_fra_russia_launch_effect',
            'nap_fra_russian_supply = -6','nap_fra_russian_cohesion = -4',
            'nap_fra_russia_settlement_effect','nap_fra_russia_retreat_effect',
            'napoleonic_collapse.1',
        ):
            self.assertIn(token,effects)

    def test_restoration_chain_has_no_fixed_follow_on_events(self):
        for source,target in (
            ('napoleonic_collapse.5','napoleonic_collapse.6'),
            ('napoleonic_collapse.8','napoleonic_collapse.9'),
            ('napoleonic_collapse.9','napoleonic_collapse.10'),
        ):
            self.assertNotIn(target,dumps(self.events[source]),source)
        for event_id in ('napoleonic_collapse.5','napoleonic_collapse.12'):
            self.assertEqual(self.events[event_id].scalar('is_triggered_only'),'yes')
        decisions=self.files['common/decisions/nap_france_campaigns.txt']
        for key in (
            'nap_fra_fontainebleau','nap_fra_restore_bourbons',
            'nap_fra_restoration_charter','nap_fra_return_elba',
            'nap_fra_hundred_days_rally','nap_fra_hundred_days_liberal',
            'nap_fra_hundred_days_battle','nap_fra_second_abdication',
            'nap_fra_hundred_days_survive','nap_fra_concert',
        ):
            self.assertIn(key,decisions)

    def test_new_variables_are_initialized_and_clamped(self):
        effects=self.files['common/scripted_effects/nap_france_campaigns.txt']
        for name in (
            'vendee_unrest','assignat_inflation','faction_tension',
            'girondin_influence','jacobin_influence','napoleon_prestige',
            'continental_pressure','peninsular_resistance',
            'russian_supply','russian_cohesion',
        ):
            self.assertIn('set_variable = { nap_fra_'+name+' =',effects)
            self.assertIn('check_variable = { nap_fra_'+name+' > 100 }',effects)
            self.assertIn('check_variable = { nap_fra_'+name+' < 0 }',effects)

    def test_localisation_covers_every_decision(self):
        loc=self.files['localisation/english/nap_france_campaigns_l_english.yml']
        for category in self.decisions:
            self.assertIn(' '+category.key+':0 ',loc)
            for decision in [e for e in category.value if isinstance(e.value,list)]:
                self.assertIn(' '+decision.key+':0 ',loc)
                self.assertIn(' '+decision.key+'_desc:0 ',loc)

    def test_no_new_territorial_shortcuts(self):
        text=self.files['common/decisions/nap_france_campaigns.txt']+self.files['common/scripted_effects/nap_france_campaigns.txt']
        for token in ('transfer_state','add_core_of','annex_country'):
            self.assertNotIn(token,text)


if __name__=='__main__':
    unittest.main()
