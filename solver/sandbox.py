from z3 import Int, IntSort, Array, Solver, sat, ForAll, Implies, And, Exists, Lambda, If, RealSort, Const, Store, K
import z3_datatypes as dt
import constraints
import functions as funcs
# print()
# s.add(t == lm)

slots = [Const(f'sl{i}', dt.Slot) for i in range(4*2)]
rooms = [
    dt.Room.croom(i, 35, False, True, True, False, False, False)
    for i in range(10)
]

courses = [
    dt.Course.ccourse(i, dt.Datetime.cdt(2, 9, 2023, 9, 0))
    for i in range(4)
]

order = [
    dt.OrderPosition.order(i, dt.SessionType.lecture, 1, 60)
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
# attr_slot = constraints.attribuer_creneau(slots, 22, 5, 2023)
in_rooms = [constraints.in_rooms(sl, rooms) for sl in slots]
in_courses = [constraints.in_courses(sl, courses) for sl in slots]
pos_uniques = constraints.positions_uniques(slots)
pos_ordonnees = constraints.positions_ordonnees(slots)
deb_cours = []
for c in courses:
    deb_cours += [constraints.debut_cours(sl, c, 4) for sl in slots]

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
    # *attr_slot,
    *in_rooms,
    *in_courses,
    *pos_uniques,
    *pos_ordonnees,
    *deb_cours,
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