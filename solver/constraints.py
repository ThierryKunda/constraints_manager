from z3 import BoolRef, And, Solver, Const, Int, ForAll, Implies, Array, IntSort, And, Store, Sqrt, Or, Real, simplify, Empty

from functions import all_models
import z3_datatypes as dtypes

def datetime_formatted(d) -> BoolRef:
    return And(
        dtypes.day(d) == 15,
        dtypes.month(d) == 5,
        dtypes.year(d) == 2023, 
        dtypes.hour(d) >= 0,
        dtypes.hour(d) <= 23,
        dtypes.minutes(d) >= 0,
        dtypes.minutes(d) <= 59,
        dtypes.minutes(d) % 15 == 0
    )

def ordered_datetimes(d1, d2) -> BoolRef:
    return (
        dtypes.hour(d1) * 60
        + dtypes.minutes(d1)
    ) - (
        dtypes.hour(d2) * 60
        + dtypes.minutes(d2)
    ) <= 0

def last(d1, d2, duration: int):
    return (
        dtypes.hour(d2) * 60
        + dtypes.minutes(d2)
    ) - (
        dtypes.hour(d1) * 60
        + dtypes.minutes(d1)
    ) == duration

def start_before_end(slot) -> BoolRef:
    return ordered_datetimes(dtypes.slot_start_time(slot), dtypes.slot_end_time(slot))

def session_type_formatted(st):
    return 0 <= st <= 3


if __name__ == "__main__":
    s = Solver()
    sl = Const('sl', dtypes.Slot)
    d1 = Const('d1', dtypes.Datetime)
    d2 = Const('d2', dtypes.Datetime)
    st = Int('st')
    i = Int('i')
    j = Int('j')
    my_array = Array('my_array', IntSort(), IntSort())
    print(*all_models(
        s,
        datetime_formatted(d1),
        datetime_formatted(d2),
        last(d1, d2, 60)
    ), sep="\n")
