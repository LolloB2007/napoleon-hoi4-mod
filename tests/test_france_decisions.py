import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]

from pdx import parse,walk,dumps
from build_20_france import build as build_france
from build_21_france_decisions import build,postprocess,VARS,CONTINENTAL_TARGETS,CATEGORIES


class FranceDecisionMechanicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=build_france(ROOT)
        cls.own=build(ROOT)
        cls.outputs=cls.base|cls.own|postprocess(cls.base|cls.own,ROOT)
        cls.decisions=parse(cls.own['common/decisions/nap_france_campaigns.txt'])
        cls.effects=parse(cls.own['common/scripted_effects/nap_france_campaigns.txt'])
        cls.effects_by_key={e.key:e for e in cls.effects}
        cls.focus_tree=parse(cls.outputs['common/national_focus/FRA.txt'])
        cls.focuses={n.scalar('id'):n for n in walk(cls.focus_tree) if n.key=='focus' and isinstance(n.value,list) and n.scalar('id')}

    def test_generated_scripts_parse(self):
        for path,text in self.own.items():
            if path.endswith('.txt'):
                parse(text)
        for path in ('common/national_focus/FRA.txt','events/01_french_revolution.txt','events/02_napoleonic_wars.txt','events/03_collapse.txt'):
            parse(self.outputs[path])

    def test_six_french_categories_plus_foreign_customs(self):
        cats={e.key for e in self.decisions}
        self.assertEqual(cats,set(CATEGORIES))
        for key in (
            'nap_fra_revolutionary_crisis','nap_fra_napoleon_rise',
            'nap_fra_continental_system','nap_fra_peninsular_war',
            'nap_fra_russian_campaign','nap_fra_restoration_cycle'
        ):
            self.assertIn(key,cats)

    def test_decision_system_uses_bounded_variables(self):
        init=dumps([self.effects_by_key['nap_fra_decision_initialize']])
        clamp=dumps([self.effects_by_key['nap_fra_decision_clamp']])
        for name,default in VARS.items():
            self.assertIn(f'nap_fra_{name}',init)
            self.assertIn(f'nap_fra_{name}',clamp)
            self.assertIn('100',clamp)
            self.assertIn('0',clamp)

    def test_revolution_has_institutions_factions_finance_vendee_and_terror(self):
        text=dumps(self.decisions)
        for key in (
            'nap_fra_establish_national_assembly',
            'nap_fra_legislative_assembly',
            'nap_fra_national_convention',
            'nap_fra_support_girondins',
            'nap_fra_support_jacobins',
            'nap_fra_issue_assignats',
            'nap_fra_negotiate_vendee',
            'nap_fra_columns_vendee',
            'nap_fra_committee_public_safety',
            'nap_fra_debate_terror',
            'nap_fra_thermidorian_reaction',
            'nap_fra_install_directory',
        ):
            self.assertIn(key,text)

    def test_napoleon_ascent_requires_campaign_prestige(self):
        text=dumps(self.decisions)
        for key in (
            'nap_fra_open_italian_campaign','nap_fra_conclude_italian_campaign',
            'nap_fra_prepare_egypt','nap_fra_return_egypt',
            'nap_fra_stage_brumaire','nap_fra_proclaim_empire_decision',
            'nap_fra_coronation','nap_fra_appoint_marshals'
        ):
            self.assertIn(key,text)
        self.assertIn('nap_fra_napoleon_prestige < 45',text)
        self.assertIn('nap_fra_napoleon_prestige < 60',text)

    def test_continental_system_has_country_enforcement_and_evasion(self):
        text=dumps(self.decisions)
        for tag,_ in CONTINENTAL_TARGETS:
            self.assertIn('nap_fra_continental_pressure_'+tag.lower(),text)
        self.assertIn('nap_continental_evade_customs',text)
        self.assertIn('nap_continental_enforce_locally',text)
        effects=self.own['common/scripted_effects/nap_france_campaigns.txt']
        self.assertIn('nap_british_continental_pressure',effects)
        self.assertIn('nap_continental_compliance',effects)

    def test_peninsular_war_has_resistance_and_bounded_exits(self):
        text=dumps(self.decisions)
        for key in (
            'nap_fra_launch_peninsular_intervention','nap_fra_peninsular_depots',
            'nap_fra_peninsular_conciliate','nap_fra_peninsular_columns',
            'nap_fra_peninsular_rotate','nap_fra_peninsular_settlement',
            'nap_fra_peninsular_withdraw'
        ):
            self.assertIn(key,text)
        effects=self.own['common/scripted_effects/nap_france_campaigns.txt']
        self.assertIn('nap_fra_peninsular_resistance',effects)
        self.assertIn('white_peace = SPR',effects)
        self.assertIn('white_peace = POR',effects)
        self.assertNotIn('annex_country',effects)

    def test_russian_campaign_has_preparation_attrition_and_three_outcomes(self):
        text=dumps(self.decisions)
        for key in (
            'nap_fra_russia_magazines','nap_fra_russia_remounts','nap_fra_russia_allies',
            'nap_fra_russia_launch','nap_fra_russia_forward_depots',
            'nap_fra_russia_winter_quarters','nap_fra_russia_press_on',
            'nap_fra_russia_settlement','nap_fra_russia_retreat'
        ):
            self.assertIn(key,text)
        monthly=dumps([self.effects_by_key['nap_fra_decision_monthly']])
        self.assertIn('nap_fra_russian_supply = -6',monthly)
        self.assertIn('nap_fra_russian_cohesion = -4',monthly)
        self.assertIn('napoleonic_collapse.1',monthly)
        self.assertIn('napoleonic_wars.13',self.own['common/scripted_effects/nap_france_campaigns.txt'])

    def test_restoration_hundred_days_and_survival_path_exist(self):
        text=dumps(self.decisions)
        for key in (
            'nap_fra_fontainebleau','nap_fra_restore_bourbons',
            'nap_fra_restoration_charter','nap_fra_return_elba',
            'nap_fra_hundred_days_rally','nap_fra_hundred_days_liberal',
            'nap_fra_hundred_days_battle','nap_fra_second_abdication',
            'nap_fra_hundred_days_survive','nap_fra_concert'
        ):
            self.assertIn(key,text)
        self.assertIn('has_war = no',text)
        self.assertIn('nap_fra_hundred_days_survived',self.own['common/scripted_effects/nap_france_campaigns.txt'])

    def test_major_transition_focuses_no_longer_auto_fire_events(self):
        pairs={
            'FRA_reign_of_terror_focus':'french_revolution.10',
            'FRA_brumaire_coup':'french_revolution.14',
            'FRA_proclaim_empire':'napoleonic_wars.3',
            'FRA_continental_system_focus':'napoleonic_wars.10',
            'FRA_invade_russia':'napoleonic_wars.16',
            'FRA_return_from_elba':'napoleonic_collapse.8',
        }
        for focus,event in pairs.items():
            reward='\n'.join(dumps(x.value) if isinstance(x.value,list) else str(x.value) for x in self.focuses[focus].children('completion_reward'))
            self.assertNotIn(event,reward,focus)

    def test_iberian_focus_no_longer_auto_declares_war(self):
        reward=dumps(self.focuses['FRA_invade_iberia'].children('completion_reward'))
        self.assertNotIn('declare_war_on',reward)
        self.assertIn('nap_fra_peninsular_decisions_unlocked',reward)

    def test_italy_and_egypt_focuses_unlock_instead_of_auto_complete(self):
        italy=dumps(self.focuses['FRA_italian_campaign'].children('completion_reward'))
        egypt=dumps(self.focuses['FRA_egyptian_expedition'].children('completion_reward'))
        self.assertNotIn('italian_campaign_won',italy)
        self.assertNotIn('egyptian_expedition_complete',egypt)
        self.assertIn('nap_fra_italian_decisions_unlocked',italy)
        self.assertIn('nap_fra_egyptian_decisions_unlocked',egypt)

    def test_decision_owned_events_are_triggered_only(self):
        event_paths=('events/01_french_revolution.txt','events/02_napoleonic_wars.txt','events/03_collapse.txt')
        events={}
        for path in event_paths:
            for e in parse(self.outputs[path]):
                if e.key in ('country_event','news_event') and e.scalar('id'):
                    events[e.scalar('id')]=e
        for eid in (
            'french_revolution.12','french_revolution.14',
            'napoleonic_wars.3','napoleonic_wars.13','napoleonic_wars.16',
            'napoleonic_collapse.1','napoleonic_collapse.5','napoleonic_collapse.12'
        ):
            self.assertEqual(events[eid].scalar('is_triggered_only'),'yes',eid)
            self.assertFalse(events[eid].children('mean_time_to_happen'),eid)
            self.assertFalse(events[eid].children('trigger'),eid)

    def test_fixed_delay_transition_calls_are_removed(self):
        paths=('events/01_french_revolution.txt','events/02_napoleonic_wars.txt','events/03_collapse.txt')
        text='\n'.join(self.outputs[p] for p in paths)
        # These transitions are now explicit decisions, not automatic delayed callbacks.
        self.assertNotIn('id = french_revolution.11\n\t\t\t\tdays = 320',text)
        self.assertNotIn('id = napoleonic_wars.4\n',dumps(parse(self.outputs['events/02_napoleonic_wars.txt'])[0].children('option')))
        collapse=self.outputs['events/03_collapse.txt']
        self.assertNotIn('days = 22',collapse)
        self.assertNotIn('days = 109',collapse)

    def test_localisation_and_docs_exist(self):
        loc=self.own['localisation/english/nap_france_campaigns_l_english.yml']
        for category in CATEGORIES:
            self.assertIn(' '+category+':0 ',loc)
        self.assertIn('Russian campaign',self.own['docs/france-decision-mechanics.md'])
        self.assertIn('Peninsular War',self.own['docs/france-decision-mechanics.md'])


if __name__=='__main__':
    unittest.main()
