import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk,dumps
from build_50_territorial import build,postprocess,validate_registry,integration_eligible,integrate_model,release_model
from build_20_france import build as france

class TerritorialTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'content/territorial_registry.json').read_text())
    def test_valid_registry(self):validate_registry(self.data)
    def test_a04_integrations_and_a05_formables_emitted(self):
        text=build(ROOT)['common/decisions/nap_territorial.txt']
        self.assertIn('nap_integrate_savoy_735',text)
        self.assertIn('nap_integrate_austrian_netherlands_6',text)
        for row in self.data['formables']:
            self.assertIn('nap_form_'+row['id'],text)
        self.assertEqual(text.count('add_core_of = FRA'),2)
    def test_all_new_scripts_parse(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'):parse(text)
    def test_six_formable_proposals(self):self.assertEqual(len(self.data['formables']),6)
    def test_approved_empty_formable_fails(self):
        self.data['formables'][0]['required_states']=[]
        with self.assertRaises(ValueError):validate_registry(self.data)
    def test_unattributed_approval_fails(self):
        self.data['integrations'][0]['approved_by']=''
        with self.assertRaises(ValueError):validate_registry(self.data)
    def test_approved_integration_requires_historical_basis(self):
        self.data['integrations'][0]['basis']=''
        with self.assertRaises(ValueError):validate_registry(self.data)
    def test_duplicate_state_fails(self):
        self.data['integrations'][0]['states']=[735,735]
        with self.assertRaises(ValueError):validate_registry(self.data)
    def test_no_string_truthy_approval(self):
        self.data['integrations'][0]['approved']='false'
        with self.assertRaises(ValueError):validate_registry(self.data)
    def test_approved_fixture_generates_delayed_coring(self):
        row=self.data['integrations'][0]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'content').mkdir();(root/'content/territorial_registry.json').write_text(json.dumps(self.data))
            text=build(root)['common/decisions/nap_territorial.txt']
            decision=next(e for e in parse(text)[0].value if e.key=='nap_integrate_savoy_735')
            self.assertEqual(decision.scalar('days_remove'),'180')
            self.assertNotIn('add_core_of',dumps(decision.children('complete_effect')))
            self.assertIn('add_core_of = FRA',dumps(decision.children('remove_effect')))
            self.assertIn('clr_country_flag',dumps(decision.children('cancel_effect')))
            self.assertNotIn('nap_treasury',dumps(decision.children('remove_effect')))
    def test_integration_requires_continuity(self):
        row=self.data['integrations'][0]
        frame=dict(owner='FRA',controller='FRA',route='imperial',compliance=85,resistance=5,at_war=False,already_core=False)
        self.assertTrue(integrate_model(row,[frame]*180))
        self.assertFalse(integrate_model(row,[frame]*179))
        interrupted=[frame]*180;interrupted[90]=frame|{'controller':'HAB'}
        self.assertFalse(integrate_model(row,interrupted))
    def test_unapproved_entry_cannot_core(self):
        row=self.data['integrations'][0]|{'approved':False}
        self.assertFalse(integration_eligible(row,owner='FRA',controller='FRA',route='imperial',compliance=100,resistance=0,at_war=False,already_core=False))
    def test_release_preserves_foreign_land(self):
        states={1:dict(owner='FRA',controller='FRA',cores=['POL']),2:dict(owner='HAB',controller='HAB',cores=['POL']),3:dict(owner='FRA',controller='RUS',cores=['POL']),4:dict(owner='FRA',controller='FRA',cores=['FRA'])}
        result=release_model('FRA','POL',states,set())
        self.assertEqual(result[1]['owner'],'POL')
        for i in (2,3,4):self.assertEqual(result[i],states[i])
    def test_existing_country_not_overwritten(self):
        states={1:dict(owner='FRA',controller='FRA',cores=['POL'])}
        self.assertEqual(release_model('FRA','POL',states,{'POL'}),states)
    def test_a06_restorations_become_puppets(self):
        text=build(ROOT)['common/scripted_effects/nap_territorial.txt']
        for tag in self.data['releasables']:
            node=next(e for e in parse(text) if e.key=='nap_restore_'+tag+'_effect')
            rendered=dumps([node])
            self.assertIn('release = '+tag,rendered)
            self.assertIn('puppet = '+tag,rendered)
            self.assertNotIn('annex_country',rendered)
    def test_client_aid_uses_only_existing_subjects(self):
        text=build(ROOT)['common/scripted_effects/nap_territorial.txt']
        for tag in self.data['clients']:
            node=next(e for e in parse(text) if e.key=='nap_client_aid_'+tag+'_effect')
            self.assertIn('is_subject_of = FRA',dumps([node]))
            self.assertIn('nap_treasury > 88',dumps([node]))
    def test_rhine_offer_replaces_unconditional_puppet(self):
        outputs=france(ROOT)|build(ROOT)
        result=postprocess(outputs,ROOT)
        event=next(e for e in parse(result['events/02_napoleonic_wars.txt']) if e.key=='country_event' and e.scalar('id')=='napoleonic_wars.7')
        self.assertNotIn('puppet',[e.key for e in walk(event.value)])
        self.assertIn('nap_clients.10',dumps([event]))
    def test_french_factions_protect_other_factions(self):
        outputs=france(ROOT)|{'to ask lollo.md':'# Queue'}
        text=postprocess(outputs,ROOT)['common/national_focus/FRA.txt']
        self.assertNotIn('create_faction =',text)
        self.assertEqual(text.count('create_faction_from_template'),3)
        self.assertEqual(text.count('is_in_faction = no'),3)
    def test_territorial_docs_list_actual_proposals(self):
        result=postprocess(france(ROOT)|build(ROOT),ROOT)
        self.assertNotIn('to ask lollo.md',result)
        docs=result['docs/territorial-systems.md']
        for row in self.data['integrations']+self.data['formables']:
            self.assertIn(row['id'],docs)
    def test_formables_grant_explicit_reasonable_cores(self):
        text=build(ROOT)['common/decisions/nap_territorial.txt']
        for row in self.data['formables']:
            self.assertTrue(row['approved'])
            self.assertTrue(row['required_states'])
            self.assertTrue(row['core_states'])
            self.assertTrue(set(row['required_states']).issubset(set(row['core_states'])))
            decision=next(e for e in parse(text)[0].value if e.key=='nap_form_'+row['id'])
            rendered=dumps([decision])
            for sid in row['required_states']:
                self.assertIn(f'{sid} =',rendered)
            self.assertEqual(rendered.count('add_core_of = ROOT'),len(row['core_states']))
            self.assertNotIn('annex_country',rendered)
    def test_default_decision_count(self):
        decisions=parse(build(ROOT)['common/decisions/nap_territorial.txt'])[0].value
        self.assertEqual(len(decisions),36)

if __name__=='__main__':unittest.main()
