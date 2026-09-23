# Localisation policy (A12)

English is the only maintained release localisation.

All checked-in and generated localisation YAML must live under `localisation/english/` and use the `l_english:` header. The content compiler validates generated localisation and the repository tree; tests fail if another maintained language directory is introduced.

Community translations can be reviewed and distributed separately later, but they are not generated automatically and are not part of the maintained release contract. Machine-translated filler is specifically excluded.
