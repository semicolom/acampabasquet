MINI = 10
INF = 20
CAD = 30
JUN = 50
SEN = 60
VET = 70

CATEGORIES = [
    (MINI, "Mini"),
    (INF, "Infantil"),
    (CAD, "Cadet"),
    (JUN, "Junior"),
    (SEN, "Senior"),
    (VET, "Veterans"),
]

MASC = 'masc'
FEM = 'fem'
MIX = 'mix'

MODALITIES = [
    (MASC, "Masculí"),
    (FEM, "Femení"),
    (MIX, "Mixte"),
]

SINGLE = 'single'
DOUBLE = 'double'

COMPETITION_TYPE_CHOICES = [
    (SINGLE, "Partit unic"),
    (DOUBLE, "Anada i tornada"),
]

GAME_FIELDS_CHOICES = [
    (1, "Pista 1"),
    (2, "Pista 2"),
]

MATCH_TYPE_COMPETITION = 'competition'
MATCH_TYPE_FRIENDLY = 'friendly'
MATCH_TYPE_FINAL = 'final'
MATCH_TYPES = [
    (MATCH_TYPE_COMPETITION, "Competició"),
    (MATCH_TYPE_FRIENDLY, "Amistós"),
    (MATCH_TYPE_FINAL, "Final"),
]
