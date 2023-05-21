from z3 import Int, IntSort, Array, Solver, sat, ForAll, Implies, And, Exists, Lambda, If, RealSort, Const, Store, K
import z3_datatypes as dt
import constraints
import functions as funcs
# print()
# s.add(t == lm)

slots = [Const(f'sl{i}', dt.Slot) for i in range(4)]
formatted = [And(constraints.datetime_formatted(dt.slot_start_time(sl)), constraints.datetime_formatted(dt.slot_end_time(sl))) for sl in slots]
ordered = [constraints.start_before_end(sl) for sl in slots]
in_day_interval = [And(constraints.day_interval(sl, 8, 0, 18, 30)) for sl in slots]
in_year_interval = [constraints.year_interval(sl, 22, 5, 2023, 22, 5, 2023) for sl in slots]
auto_exclusion = constraints.auto_exclusion(slots, 15)
pause_dejeuner = [constraints.pause_dejeuner(sl, 12, 30, 13, 30) for sl in slots]
calendrier_valide = [constraints.calendrier_valide(sl) for sl in slots]
meme_j = [constraints.meme_jour(sl) for sl in slots]
duree_min = [constraints.duree_min(sl, 120) for sl in slots]

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
    max_models=3
)
print(*models, sep="\n")
# if s.check() == sat:
#     print(s.model())
# else:
#     print('Insatisfiable')