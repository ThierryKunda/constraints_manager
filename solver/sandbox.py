from z3 import Int, IntSort, Array, Solver, sat, ForAll, Implies, And, Exists, Lambda, If, RealSort, Const, Store, K
import z3_datatypes as dt
import constraints
import functions as funcs
from random import randint
# print()
# s.add(t == lm)

slots = [Const(f'sl{i}', dt.Slot) for i in range(4*2)]
rooms = [
    dt.Room.croom(i, 30, False, True, True, False, False, False)
    for i in range(10)
]

courses = [
    dt.Course.ccourse(i, dt.Datetime.cdt(1, 9, 2023, 9, 0), randint(80, 85), randint(3,4))
    for i in range(2)
]

order = [
    dt.OrderPosition.order(i, dt.SessionType.lecture, 1, 60)
    for i in range(4)
] + [
    dt.OrderPosition.order(i, dt.SessionType.lecture, 2, 60)
    for i in range(4)
]

formatted = [And(constraints.datetime_formatted(dt.slot_start_time(sl)), constraints.datetime_formatted(dt.slot_end_time(sl))) for sl in slots]
ordered = [constraints.start_before_end(sl) for sl in slots]
in_day_interval = [And(constraints.day_interval(sl, 8, 0, 18, 30)) for sl in slots]
in_year_interval = [constraints.year_interval(sl, 1, 9, 2023, 2, 9, 2023) for sl in slots]
auto_exclusion = constraints.auto_exclusion(slots, 15)
pause_dejeuner = [constraints.pause_dejeuner(sl, 12, 30, 13, 30) for sl in slots]
calendrier_valide = [constraints.calendrier_valide(sl) for sl in slots]
meme_j = [constraints.meme_jour(sl) for sl in slots]
duree_min = [constraints.duree_min(sl, 120) for sl in slots]
in_rooms = [constraints.in_rooms(sl, rooms) for sl in slots]
in_courses = [constraints.in_courses(sl, courses) for sl in slots]
pos_uniques = constraints.positions_uniques(slots)
pos_ordonnees = constraints.positions_ordonnees(slots)
deb_cours = []
taille_promo = []
taille_groupe = []
for c in courses:
    deb_cours += [constraints.debut_cours(sl, c, 4) for sl in slots]
    taille_promo += [constraints.taille_promo(sl, c) for sl in slots]
    taille_groupe += [constraints.taille_groupe(sl, c) for sl in slots]
type_seance_supporte = [constraints.seance_supporte_par_salle(sl) for sl in slots]
type_seance_donnee = [constraints.type_seance_donnee(sl) for sl in slots]
attrib_creneau = [constraints.attribuer_creneau(slots, o) for o in order]
duree_seance = [constraints.duree_seance(sl) for sl in slots]
s = Solver()

# s.add(*formatted, *ordered, *in_day_interval, *auto_exclusion, *pause_dejeuner)

models = funcs.all_models(
    s,
    *ordered,
    *formatted,
    *in_day_interval,
    *in_year_interval,
    *auto_exclusion,
    *pause_dejeuner,
    *calendrier_valide,
    *meme_j,
    *duree_min,
    *in_rooms,
    *in_courses,
    # *pos_uniques,
    # *pos_ordonnees,
    *deb_cours,
    *taille_promo,
    *taille_groupe,
    *type_seance_supporte,
    *type_seance_donnee,
    *attrib_creneau,
    *duree_seance,
    max_models=1
)
if len(models) > 0:
    print(*models, sep="\n")
else:
    print("Insatisfiable")
# if s.check() == sat:
#     print(s.model())
# else:
#     print('Insatisfiable')