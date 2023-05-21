from z3 import BoolRef, And, Solver, Const, Int, Implies, And, Or, Implies

from functions import all_models
import z3_datatypes as dtypes

def datetime_formatted(d) -> BoolRef:
    return And(
        dtypes.day(d) == 22,
        dtypes.month(d) == 5,
        dtypes.year(d) == 2023,
        dtypes.hour(d) >= 0,
        dtypes.hour(d) <= 23,
        dtypes.minutes(d) >= 0,
        dtypes.minutes(d) <= 59,
        dtypes.minutes(d) % 15 == 0
    )

def ordered_datetimes(d1, d2) -> BoolRef:
    return Or(
        dtypes.year(d1) < dtypes.year(d2),
        And(
            dtypes.year(d1) == dtypes.year(d2),
            dtypes.month(d1) < dtypes.month(d2)
        ),
        And(
            dtypes.year(d1) == dtypes.year(d2),
            dtypes.month(d1) == dtypes.month(d2),
            dtypes.day(d1) < dtypes.day(d2),
        ),
        And(
            dtypes.year(d1) == dtypes.year(d2),
            dtypes.month(d1) == dtypes.month(d2),
            dtypes.day(d1) == dtypes.day(d2),
            dtypes.hour(d1) < dtypes.hour(d2)
        ),
        And(
            dtypes.year(d1) == dtypes.year(d2),
            dtypes.month(d1) == dtypes.month(d2),
            dtypes.day(d1) == dtypes.day(d2),
            dtypes.hour(d1) == dtypes.hour(d2),
            dtypes.minutes(d1) < dtypes.minutes(d2)
        )
    )

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

def day_interval(slot, start_hour: int, start_minute: int, end_hour: int, end_minute: int) -> BoolRef:
    return And(
        Or(
            start_hour < dtypes.hour(dtypes.slot_start_time(slot)),
            And(
                start_hour == dtypes.hour(dtypes.slot_start_time(slot)),
                start_minute <= dtypes.minutes(dtypes.slot_start_time(slot)),
            )
        ),
        Or(
            dtypes.hour(dtypes.slot_end_time(slot)) < end_hour,
            And(
                dtypes.hour(dtypes.slot_end_time(slot)) == end_hour,
                dtypes.minutes(dtypes.slot_end_time(slot)) <= end_minute,
            )
        )
    )

def equivalent(P: BoolRef, Q: BoolRef):
    return And(
        Implies(P, Q),
        Implies(Q, P),
    )

def auto_exclusion(slots: list) -> list[BoolRef]:
    constrs = []
    for i in range(len(slots)):
        for j in range(len(slots)):
            if i != j:
                constrs.append(
                    Or(
                        And(
                            ordered_datetimes(dtypes.slot_start_time(slots[i]), dtypes.slot_start_time(slots[j])),
                            ordered_datetimes(dtypes.slot_end_time(slots[i]), dtypes.slot_end_time(slots[j])),
                            ordered_datetimes(dtypes.slot_end_time(slots[i]), dtypes.slot_start_time(slots[j]))
                        ),
                        And(
                            ordered_datetimes(dtypes.slot_start_time(slots[j]), dtypes.slot_start_time(slots[i])),
                            ordered_datetimes(dtypes.slot_end_time(slots[j]), dtypes.slot_end_time(slots[i])),
                            ordered_datetimes(dtypes.slot_start_time(slots[j]), dtypes.slot_end_time(slots[i]))
                        )

                    )
                )
    return constrs

if __name__ == "__main__":
    s = Solver()
    sl = Const('sl', dtypes.Slot)
    d1 = Const('d1', dtypes.Datetime)
    d2 = Const('d2', dtypes.Datetime)
    st = Int('st')
    i = Int('i')
    j = Int('j')
    slots = [Const(f"sl{i}", dtypes.Slot) for i in range(5)]
    # print(*all_models(
    #     s,
    #     datetime_formatted(d1),
    #     datetime_formatted(d2),
    #     last(d1, d2, 60)
    # ), sep="\n")
    # if s.check() == sat:
    #     print(s.model())
    # else:
    #     print("Non satisfiable")
