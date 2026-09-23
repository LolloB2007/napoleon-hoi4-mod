import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'content'))
from pdx import parse, walk
from build_10_era import ACTIONS, DEFAULTS, build, apply_action, monthly_model

class EraTests(unittest.TestCase):
    def test_all_generated_scripts_parse(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'):
                parse(text)
    def test_cooldowns_and_costs(self):
        self.assertEqual(len(ACTIONS),12)
        for action in ACTIONS:
            self.assertGreater(action[2],0)
            self.assertGreaterEqual(action[3],90)
    def test_no_unfunded_negative_delta(self):
        for a in ACTIONS:
            for key,delta in a[6].items():
                if key=='treasury' and delta<0:
                    self.assertGreaterEqual(a[4].get(key,0),-delta)
    def test_all_actions_bounds(self):
        for a in ACTIONS:
            for n in (0,20,50,70,100):
                state={k:n for k in DEFAULTS}
                for at_war in (False,True):
                    result=apply_action(state,a,at_war=at_war,revolutionary_france=True)
                    if result:
                        self.assertTrue(all(0<=v<=100 for v in result.values()))
    def test_borrowing_limit(self):
        self.assertIsNone(apply_action(DEFAULTS|{'debt':71},ACTIONS[0]))
    def test_no_money_recruitment(self):
        self.assertIsNone(apply_action(DEFAULTS|{'treasury':0},ACTIONS[3]))
    def test_levee_route_and_war(self):
        state=DEFAULTS|{'fervor':50}
        self.assertIsNone(apply_action(state,ACTIONS[4],at_war=True))
        self.assertIsNone(apply_action(state,ACTIONS[4],revolutionary_france=True))
        self.assertIsNotNone(apply_action(state,ACTIONS[4],at_war=True,revolutionary_france=True))
    def test_monthly_peace(self):
        result=monthly_model(DEFAULTS|{'war_exhaustion':20},at_war=False,foreign_occupation=False)
        self.assertEqual(result['war_exhaustion'],16)
        self.assertEqual(result['treasury'],53)
    def test_foreign_war_cost(self):
        result=monthly_model(DEFAULTS,at_war=True,foreign_occupation=True)
        self.assertEqual(result['war_exhaustion'],4)
        self.assertEqual(result['supply_pressure'],2)
    def test_monthly_bounds(self):
        for n in (0,100):
            for war in (False,True):
                result=monthly_model({k:n for k in DEFAULTS},at_war=war,foreign_occupation=True)
                self.assertTrue(all(0<=v<=100 for v in result.values()))
    def test_monthly_not_quadratic(self):
        hooks=build(ROOT)['common/on_actions/nap_era.txt']
        monthly=next(e for e in parse(hooks)[0].value if e.key=='on_monthly')
        self.assertNotIn('every_country',[e.key for e in walk(monthly.value)])
    def test_execution_rechecks_resources(self):
        effects=build(ROOT)['common/scripted_effects/nap_era.txt']
        for a in ACTIONS:
            effect=next(e for e in parse(effects) if e.key=='nap_era_action_'+a[0])
            self.assertEqual(effect.value[0].key,'if')
    def test_init_only_once(self):
        self.assertIn('NOT = { has_country_flag = nap_era_initialized }',build(ROOT)['common/scripted_effects/nap_era.txt'])
    def test_no_forced_cores_or_land(self):
        for name,text in build(ROOT).items():
            if name.endswith('.txt'):
                self.assertNotIn('transfer_state',text)
                self.assertNotIn('add_core_of',text)

if __name__=='__main__': unittest.main()
