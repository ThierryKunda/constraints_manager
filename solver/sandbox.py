from z3 import Int, IntSort, Array, Solver, sat, ForAll, Implies, And, Exists, Lambda, If, RealSort, Const, Store, K
import z3_datatypes as dt
from constraints import *

arr = Array('arr', IntSort(), IntSort())
i = Const('i', dt.DateTimeInterval)
j = Const('j', dt.DateTimeInterval)
t = Array('m', dt.DateTimeInterval, dtypes.DateTimeInterval, dt.Slot)
r = dt.Room.croom(-1, -1, False, False, False)
i_0 = dt.DateTimeInterval.cdti(
    dt.Datetime.cdt(20, 5, 2023, 15, 30),
    dt.Datetime.cdt(20, 5, 2023, 16, 0)
)
i_1 = dt.DateTimeInterval.cdti(
    dt.Datetime.cdt(100, 100, 100, 100, 100),
    dt.Datetime.cdt(100, 100, 100, 100, 100)
)
sl = dt.Slot.cslot(
    dt.Datetime.cdt(-1, -1, -1, -1, -1),
    dt.Datetime.cdt(-1, -1, -1, -1, -1),
    -1,
    -1,
    r
)

s = Solver()
lm = Lambda([i, j],  If(
    And(
        ordered_datetimes(dt.start_time(i), dt.end_time(i)),
        j != i
    ),
    dt.Slot.cslot(
        dt.start_time(i),
        dt.end_time(i),
        0,
        0,
        r
    ),
    sl
))
# print()
s.add(t == lm)

if s.check() == sat:
    m = s.model()
    # print(m)
    print(f"{m.eval(m[t][i_0, i_1])}")
    # for i in range(8):
    #     print(f"m[{i}] = {m.eval(m[t][i])}")
else:
    print('Insatisfiable')