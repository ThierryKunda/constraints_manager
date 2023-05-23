from z3 import Solver, Or, And, Int, sat, Implies, ModelRef
import z3_datatypes as custom_dt
from typing import Callable

s = Solver()
slots = [Int(f"slot{i}") for i in range(8, 19)]
constr = [(slots[i] == (slots[i+1] + 1)) for i in range(len(slots)-1)]
for i in range(len(slots)):
    constr.append(8 <= slots[i])
    constr.append(slots[i] <= 19)
    for j in range(len(slots)):
        constr.append(Implies(slots[i] == (slots[j]), i == j))
s.add(constr)
if s.check() == sat:
    print(s.model())
else:
    print("Non satisfiable")
    # t[i] == t[j] => i == j

# def slots_attibutes_uniques(slots_constants: list[custom_dt.Slot], accessor: Callable) -> ModelRef:
#     constr = []
#     for i in range(len(slots_constants)):
#         for j in range(len(slots_constants)):
#             # constr.append(0 < slots_constants[i])
#             # constr.append(slots[i] < 5)
#             constr.append(Implies(accessor(slots[i]) == accessor(slots[j]), i == j))