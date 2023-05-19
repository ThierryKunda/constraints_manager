from z3 import Solver, Or, And, Int, sat

s = Solver()
slots = [Int(f"slot{i}") for i in range(5)]
constrs = [slots[i] != slots[i+1] for i in range(slots)]
s.add(constrs)
if s.check() == sat:
    print(s.model())
