import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,dumps,walk
from build_content import compile_sources
from build_30_coalitions import build,opening_effects,postprocess,ROUNDS,ROSTER,OPENING,eligible_round,transfer_subsidy,settle_model,cap_guard

class CoalitionTests(unittest.TestCase):
    def test_scripts_parse(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'):parse(text)
        parse(opening_effects())
    def test_seven_ordered_rounds(self):
        self.assertEqual([r[0] for r in ROUNDS],list(range(1,8)))
        self.assertFalse(eligible_round(4,{1,2}))
        self.assertTrue(eligible_round(4,{1,2,3}))
        self.assertFalse(eligible_round(4,{1,2,3,4}))
    def test_no_round_without_context(self):
        for args in ({'french_context':False},{'host_free':False}):
            self.assertFalse(eligible_round(1,set(),**args))
    def test_subsidy_conserves_treasury(self):
        for a in range(101):
            for b in range(101):
                result=transfer_subsidy(a,b)
                if result:
                    self.assertEqual(sum(result),a+b)
                    self.assertTrue(all(0<=n<=100 for n in result))
    def test_subsidy_restrictions(self):
        self.assertIsNone(transfer_subsidy(14,0))
        self.assertIsNone(transfer_subsidy(100,86))
        self.assertIsNone(transfer_subsidy(50,50,False))
    def test_jassy_bounded(self):
        state={'wars':{frozenset(('RUS','TUR')),frozenset(('RUS','SWE'))},'resolved':set(),'owners':{192:'TUR',797:'TUR'}}
        result=settle_model(state,winner='RUS',loser='TUR',jassy=True)
        self.assertEqual(result['owners'],{192:'RUS',797:'TUR'})
        self.assertIn(frozenset(('RUS','SWE')),result['wars'])
    def test_jassy_third_party_preserved(self):
        state={'wars':{frozenset(('RUS','TUR'))},'resolved':set(),'owners':{192:'HAB'}}
        self.assertEqual(settle_model(state,winner='RUS',loser='TUR',jassy=True)['owners'],state['owners'])
    def test_settlement_idempotent(self):
        state={'wars':{frozenset(('RUS','TUR'))},'resolved':set(),'owners':{192:'TUR'}}
        once=settle_model(state,winner='RUS',loser='TUR',jassy=True)
        self.assertEqual(once,settle_model(once,winner='RUS',loser='TUR',jassy=True))
    def test_reverse_jassy_restores_ottoman_land_only_if_russian_owned(self):
        state={'wars':{frozenset(('RUS','TUR'))},'resolved':set(),'owners':{192:'RUS',797:'HAB'}}
        result=settle_model(state,winner='TUR',loser='RUS',jassy=True)
        self.assertEqual(result['owners'][192],'TUR')
        self.assertEqual(result['owners'][797],'HAB')
    def test_no_land_change_when_reverse_jassy_has_third_party_owner(self):
        state={'wars':{frozenset(('RUS','TUR'))},'resolved':set(),'owners':{192:'HAB'}}
        self.assertEqual(settle_model(state,winner='TUR',loser='RUS',jassy=True)['owners'],state['owners'])
    def test_no_settlement_without_war(self):
        state={'wars':set(),'resolved':set(),'owners':{192:'TUR'}}
        self.assertEqual(settle_model(state,winner='RUS',loser='TUR',jassy=True),state)
    def test_locks_precede_peace(self):
        for effect in parse(opening_effects()):
            entries=list(walk(effect.value));keys=[e.key for e in entries]
            if 'white_peace' not in keys:
                continue
            self.assertLess(keys.index('set_global_flag'),keys.index('white_peace'))
            self.assertLess(keys.index('clr_global_flag'),keys.index('white_peace'))
    def test_state_core_scope(self):
        text=opening_effects()
        self.assertNotIn('add_state_core',text)
        self.assertNotIn('remove_state_core',text)
        self.assertIn('192 = { add_core_of = RUS remove_core_of = TUR }',text)
    def test_separate_peace_detaches_first(self):
        effect=next(e for e in parse(build(ROOT)['common/scripted_effects/nap_coalitions.txt']) if e.key=='nap_coalition_separate_peace')
        text=dumps([effect])
        self.assertLess(text.index('remove_from_faction'),text.index('white_peace'))
        self.assertIn('has_faction_template = nap_coalition_template',text)
    def test_dismantle_guarded_by_own_template(self):
        entries=parse(build(ROOT)['common/scripted_effects/nap_coalitions.txt'])
        for node in walk(entries):
            if node.key=='if' and node.children('dismantle_faction'):
                self.assertIn('has_faction_template = nap_coalition_template',dumps(node.children('limit')))
    def test_invite_accept_requires_resources_and_consent(self):
        events=parse(build(ROOT)['events/06_coalitions.txt'])
        for n,*_ in ROUNDS:
            e=next(e for e in events if e.key=='country_event' and e.scalar('id')==f'nap_coalition.{100+n}')
            self.assertEqual(len(e.children('option')),2)
            accept=e.children('option')[0]
            self.assertIn('nap_treasury < 8',dumps(accept.children('trigger')))
            self.assertIn('nap_treasury < 8',dumps(accept.children('if')[0].children('limit')))
            self.assertNotIn('declare_war_on',dumps(e.children('option')[1:]))
    def test_event_and_decision_counts(self):
        out=build(ROOT)
        self.assertEqual(len([e for e in parse(out['events/06_coalitions.txt']) if e.key=='country_event']),27)
        self.assertEqual(len(parse(out['common/decisions/nap_coalitions.txt'])[0].value),25)
    def test_event_localisation(self):
        out=build(ROOT);loc=out['localisation/english/nap_coalitions_l_english.yml']
        for event in parse(out['events/06_coalitions.txt']):
            if event.key!='country_event':continue
            for child in event.children('title')+event.children('desc'):
                self.assertIn(' '+child.value+':0 ',loc)
            for option in event.children('option'):
                self.assertIn(' '+option.scalar('name')+':0 ',loc)
    def test_callback_scope_reversal(self):
        self.assertIn('ROOT = { tag = RUS } FROM = { tag = TUR }',cap_guard())
        self.assertIn('FROM = { tag = RUS } ROOT = { tag = TUR }',cap_guard(True))
        self.assertIn('napoleonic_end_russo_turkish_jassy_a_victory',cap_guard())
        self.assertIn('napoleonic_end_russo_turkish_jassy_b_victory',cap_guard())
        self.assertIn('nap_coalition_coalition_victory_settlement',cap_guard())
        self.assertIn('nap_coalition_french_victory_settlement',cap_guard())
    def test_a03_coalition_has_outcome_aware_settlements(self):
        text=build(ROOT)['common/scripted_effects/nap_coalitions.txt']
        self.assertIn('nap_coalition_french_victory_settlement',text)
        self.assertIn('nap_coalition_coalition_victory_settlement',text)
        self.assertIn('add_political_power = 100',text)
        self.assertIn('add_political_power = -100',text)
    def test_monthly_not_quadratic(self):
        hooks=parse(build(ROOT)['common/on_actions/nap_coalitions.txt'])[0]
        self.assertNotIn('every_country',[e.key for e in walk(hooks.children('on_monthly')[0].value)])
    def test_opening_postprocessor(self):
        # Tests integration mechanics against a fixture; CI generation also
        # exercises the byte-identical retained source blobs from master.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'content/legacy';folder.mkdir(parents=True)
            folder.joinpath('m2_diplomacy.txt').write_text('napoleonic_setup_1789_diplomacy = { set_global_flag = existing_setup } old = { }')
            folder.joinpath('ENG.txt').write_text('focus_tree = { focus = { id = ENG_test completion_reward = { create_faction = coalition_against_france } } }')
            folder.joinpath('m2_events.txt').write_text('\n'.join('country_event = { id = napoleonic_diplomacy.'+str(r[9])+' option = { name = test '+r[1]+' = yes } }' for r in OPENING))
            out=postprocess({},root)
            self.assertIn('existing_setup',out['common/scripted_effects/napoleonic_diplomacy_setup.txt'])
            self.assertNotIn('old =',out['common/scripted_effects/napoleonic_diplomacy_setup.txt'])
            self.assertNotIn('create_faction',out['common/national_focus/ENG.txt'])
            for e in parse(out['events/04_1789_diplomacy.txt']):
                self.assertEqual(len(e.children('immediate')),1)
                self.assertEqual(len(e.children('is_triggered_only')),1)
                self.assertFalse(e.children('trigger'))
                self.assertFalse(e.children('mean_time_to_happen'))
                self.assertEqual(len(e.children('option')[0].value),1)
    def test_compiler_postpass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'content').mkdir()
            (root/'content/build_a.py').write_text('def build(root): return {"events/test.txt":"before"}\ndef postprocess(outputs,root): return {"events/test.txt":outputs["events/test.txt"]+" after"}\n')
            self.assertEqual(compile_sources(root)['events/test.txt'],b'before after')
    def test_postpass_path_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'content').mkdir()
            (root/'content/build_a.py').write_text('def build(root): return {}\ndef postprocess(outputs,root): return {"../outside":"no"}\n')
            with self.assertRaises(ValueError):compile_sources(root)

if __name__=='__main__':unittest.main()
