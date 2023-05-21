from z3 import Int, IntSort, Array, Solver, sat, ForAll, Implies, And, Exists, Lambda, If, RealSort, Const, Store, K
import z3_datatypes as dt
import constraints
import functions as funcs
# print()
# s.add(t == lm)

slots = [Const(f'sl{i}', dt.Slot) for i in range(4)]
# positive_dt = [And(constraints.positive_datetime_values(dt.slot_start_time(sl)), constraints.positive_datetime_values(dt.slot_end_time(sl))) for sl in slots]
formatted = [And(constraints.datetime_formatted(dt.slot_start_time(sl)), constraints.datetime_formatted(dt.slot_end_time(sl))) for sl in slots]
ordered = [constraints.start_before_end(sl) for sl in slots]
in_day_interval = [And(constraints.day_interval(sl, 8, 0, 18, 30)) for sl in slots]
auto_exclusion = constraints.auto_exclusion(slots)
pause_dejeuner = [constraints.pause_dejeuner(sl, 12, 30, 13, 30) for sl in slots]
s = Solver()

# s.add(*formatted, *ordered, *in_day_interval, *auto_exclusion, *pause_dejeuner)

models = funcs.all_models(s, *ordered, *formatted, *in_day_interval, *auto_exclusion, *pause_dejeuner, max_models=3)
print(*models, sep="\n")
# if s.check() == sat:
#     print(s.model())
# else:
#     print('Insatisfiable')