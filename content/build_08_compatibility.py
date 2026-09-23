"""A08 compatibility baseline: HOI4 1.19.x with La Resistance required."""
def build(root):
    return {
      'common/scripted_triggers/nap_compatibility.txt': 'nap_required_dlc_available = { has_dlc = "La Resistance" }\n',
      'common/on_actions/nap_compatibility.txt': '''on_actions = {
 on_startup = { effect = {
  FRA = { if = { limit = { NOT = { nap_required_dlc_available = yes } } country_event = { id = nap_compatibility.1 hours = 1 } } }
 } }
}
''',
      'events/00_compatibility.txt': '''add_namespace = nap_compatibility
country_event = {
 id = nap_compatibility.1
 title = nap_compatibility.1.t
 desc = nap_compatibility.1.d
 picture = GFX_report_event_generic_assembly
 is_triggered_only = yes
 option = { name = nap_compatibility.1.a set_global_flag = nap_missing_required_dlc }
}
''',
      'localisation/english/nap_compatibility_l_english.yml': '''\ufeffl_english:
 nap_compatibility.1.t:0 "Required DLC Missing"
 nap_compatibility.1.d:0 "Napoleonic Era targets Hearts of Iron IV 1.19.x and requires La Résistance. This configuration is unsupported without that DLC enabled."
 nap_compatibility.1.a:0 "Return with La Résistance enabled."
''',
      'docs/compatibility.md': '''# Compatibility baseline (A08)

Supported development target: **Hearts of Iron IV 1.19.x**.

Required paid DLC: **La Résistance**.

Other paid DLC is not a project requirement unless separately approved later. The runtime startup check surfaces a warning when La Résistance is disabled; the repository does not pretend that a launcher descriptor can enforce DLC ownership.

Static parsing and unit tests do not certify engine compatibility. Acceptance still requires a clean 1.19.x launch with La Résistance enabled and review of error.log/game.log.
'''
    }
