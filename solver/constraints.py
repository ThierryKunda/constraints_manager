from random import randint
from z3 import BoolRef, And, Solver, Const, Int, Implies, And, Or, Implies, Not

from functions import all_models
import z3_datatypes as dtypes

def datetime_formatted(d) -> BoolRef:
    return And(
        dtypes.day(d) >= 1,
        dtypes.month(d) >= 1,
        dtypes.year(d) >= 1,
        dtypes.hour(d) >= 0,
        dtypes.hour(d) <= 23,
        dtypes.minutes(d) >= 0,
        dtypes.minutes(d) <= 59,
        dtypes.minutes(d) % 15 == 0
    )

def ordered_datetimes(d1, d2, margin: int = 0) -> BoolRef:
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
            dtypes.minutes(d1) < dtypes.minutes(d2) + margin
        )
    )

def last(d1, d2, duration: int):
    return (
        (dtypes.hour(d2) * 60)
        + dtypes.minutes(d2)
    ) - (
        (dtypes.hour(d1) * 60)
        + dtypes.minutes(d1)
    ) >= duration

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

def year_interval(slot, start_day: int, start_month: int, start_year: int, end_day: int, end_month: int, end_year: int) -> BoolRef:
    return And(
        Or(
            start_year < dtypes.year(dtypes.slot_start_time(slot)),
            And(
                start_year == dtypes.year(dtypes.slot_start_time(slot)),
                start_month < dtypes.month(dtypes.slot_start_time(slot)),
            ),
            And(
                start_year == dtypes.year(dtypes.slot_start_time(slot)),
                start_month == dtypes.month(dtypes.slot_start_time(slot)),
                start_day <= dtypes.day(dtypes.slot_start_time(slot)),
            )
        ),
        Or(
            dtypes.year(dtypes.slot_end_time(slot)) < end_year,
            And(
            dtypes.year(dtypes.slot_end_time(slot)) == end_year,
            dtypes.month(dtypes.slot_end_time(slot)) < end_month,
            ),
            And(
                dtypes.year(dtypes.slot_end_time(slot)) == end_year,
                dtypes.month(dtypes.slot_end_time(slot)) == end_month,
                dtypes.day(dtypes.slot_end_time(slot)) <= end_day,
            )
        ),

    )

def meme_jour(slot) -> BoolRef:
    return And(
        dtypes.day(dtypes.slot_start_time(slot)) == dtypes.day(dtypes.slot_end_time(slot)),
        dtypes.month(dtypes.slot_start_time(slot)) == dtypes.month(dtypes.slot_end_time(slot)),
        dtypes.year(dtypes.slot_start_time(slot)) == dtypes.year(dtypes.slot_end_time(slot)),
    )

def equivalent(P: BoolRef, Q: BoolRef):
    return And(
        Implies(P, Q),
        Implies(Q, P),
    )

def auto_exclusion(slots: list, pause: int = 0) -> list[BoolRef]:
    constrs = []
    for i in range(len(slots)):
        for j in range(len(slots)):
            if i != j:
                constrs.append(
                    Or(
                        # ((t1.start < t2.start) et (t1.end < t2.end) et (t1.end + pause < t2.start))
                        And(
                            ordered_datetimes(dtypes.slot_start_time(slots[i]), dtypes.slot_start_time(slots[j])),
                            ordered_datetimes(dtypes.slot_end_time(slots[i]), dtypes.slot_end_time(slots[j])),
                            ordered_datetimes(dtypes.slot_end_time(slots[i]), dtypes.slot_start_time(slots[j]))
                        ),
                        # ((t1.start > t2.start) et (t1.end > t2.end) et (t1.start > t2.end + pause))
                        And(
                            ordered_datetimes(dtypes.slot_start_time(slots[j]), dtypes.slot_start_time(slots[i])),
                            ordered_datetimes(dtypes.slot_end_time(slots[j]), dtypes.slot_end_time(slots[i])),
                            ordered_datetimes(dtypes.slot_start_time(slots[j]), dtypes.slot_end_time(slots[i]), pause)
                        )

                    )
                )
    return constrs

def pause_dejeuner(slot, start_hour: int, start_minute: int, end_hour: int, end_minute: int) -> BoolRef:
    constrs = []
    constrs.append(
        Or(
            dtypes.hour(dtypes.slot_end_time(slot)) < start_hour,
            And(
                dtypes.hour(dtypes.slot_end_time(slot)) == start_hour,
                dtypes.minutes(dtypes.slot_end_time(slot)) <= start_minute,
            ),
        )
    )
    constrs.append(
        Or(
            end_hour < dtypes.hour(dtypes.slot_start_time(slot)),
            And(
                end_hour == dtypes.hour(dtypes.slot_start_time(slot)),
                end_minute <= dtypes.minutes(dtypes.slot_start_time(slot)),
            ),
        )
    )
    return Or(*constrs)

def est_bissextile(annee: int):
    if annee % 4 == 0:
        if annee % 100 == 0:
            return annee % 400
        return True
    return False

def calendrier_valide(slot) -> BoolRef:
    constrs = []
    start_year = dtypes.year(dtypes.slot_start_time(slot))
    end_year = dtypes.year(dtypes.slot_end_time(slot))
    start_month = dtypes.month(dtypes.slot_start_time(slot))
    end_month = dtypes.month(dtypes.slot_end_time(slot))
    start_day = dtypes.day(dtypes.slot_start_time(slot))
    end_day = dtypes.day(dtypes.slot_end_time(slot))
    start_biss = est_bissextile(start_year)
    end_biss = est_bissextile(end_year)
    # Janvier
    constrs += [
        Implies(start_month == 1, start_day <= 31),
        Implies(end_month == 1, end_day <= 31)
    ] 

    # Février
    constrs += [
        Implies(start_month == 2, Or(And(start_biss, start_day <= 29), And(not start_biss, start_day <= 28))),
        Implies(end_month == 2, Or(And(end_biss, end_day <= 29), And(not end_biss, end_day <= 28)))

    ]
    # Mars
    constrs += [
        Implies(start_month == 3, start_day <= 31),
        Implies(end_month == 3, end_day <= 31)
    ]
    # Avril
    constrs += [
        Implies(start_month == 4, start_day <= 30),
        Implies(end_month == 4, end_day <= 30)
    ]
    # Mai
    constrs += [
        Implies(start_month == 5, start_day <= 31),
        Implies(end_month == 5, end_day <= 31)
    ]
    # Juin
    constrs += [
        Implies(start_month == 6, start_day <= 30),
        Implies(end_month == 6, end_day <= 30)
    ]
    # Juillet
    constrs += [
        Implies(start_month == 7, start_day <= 31),
        Implies(end_month == 7, end_day <= 31)
    ]
    # Août
    constrs += [
        Implies(start_month == 8, start_day <= 31),
        Implies(end_month == 8, end_day <= 31)
    ]
    # Septembre
    constrs += [
        Implies(start_month == 9, start_day <= 30),
        Implies(end_month == 9, end_day <= 30)
    ]
    # Octobre
    constrs += [
        Implies(start_month == 10, start_day <= 31),
        Implies(end_month == 10, end_day <= 31)
    ]
    # Novembre
    constrs += [
        Implies(start_month == 11, start_day <= 30),
        Implies(end_month == 11, end_day <= 30)
    ]
    # Décembre
    constrs += [
        Implies(start_month == 12, start_day <= 31),
        Implies(end_month == 12, end_day <= 31)
    ]

    return And(*constrs)

def duree_min(slot, duration: int) -> BoolRef:
    return (
        dtypes.hour(dtypes.slot_end_time(slot)) * 60
        + dtypes.minutes(dtypes.slot_end_time(slot))
    ) - (
        dtypes.hour(dtypes.slot_start_time(slot)) * 60
        + dtypes.minutes(dtypes.slot_start_time(slot))
    ) >= duration

def in_rooms(slot, rooms: list) -> BoolRef:
    return Or(*[dtypes.room(slot) == r for r in rooms])

def in_courses(slot, courses: list) -> BoolRef:
    return Or(*[dtypes.subject(slot) == c for c in courses])

def positions_uniques(slots) -> list[BoolRef]:
    constrs = []
    for i in range(len(slots)):
        for j in range(len(slots)):
            if i != j:
                constrs.append(
                    Implies(
                        dtypes.subject(slots[i]) == dtypes.subject(slots[j]),
                        dtypes.indice_position(dtypes.order_position(slots[i])) != dtypes.indice_position(dtypes.order_position(slots[j]))
                    )
                )
    return constrs

def positions_ordonnees(slots) -> list[BoolRef]:
    constrs = []
    for i in range(len(slots)):
        for j in range(len(slots)):
            if i != j:
                constrs.append(
                    equivalent(
                        dtypes.indice_position(dtypes.order_position(slots[i]))
                        < dtypes.indice_position(dtypes.order_position(slots[j])),
                        ordered_datetimes(dtypes.slot_start_time(slots[i]), dtypes.slot_start_time(slots[j]))
                    )
                )
    return constrs

def debut_cours(slot, course, session_amount) -> BoolRef:
    return Implies(
        And(
            ordered_datetimes(dtypes.course_start(course), dtypes.slot_start_time(slot)),
            dtypes.subject(slot) == course,
        ),
        And(
            1 <= dtypes.indice_position(dtypes.order_position(slot)),
            dtypes.indice_position(dtypes.order_position(slot)) < session_amount,
        )
    )

def taille_promo(slot, course) -> BoolRef:
    return Implies(
        And(
            dtypes.subject(slot) == course,
            Not(
                Or(
                    dtypes.session_type(slot) == dtypes.SessionType.tutorial,
                    dtypes.session_type(slot) == dtypes.SessionType.practicum,
                )
            )
        ),
        dtypes.students_amount(course) <= dtypes.capacity(dtypes.room(slot))
    )
    
def taille_groupe(slot, course) -> BoolRef:
    return Implies(
        And(
            dtypes.subject(slot) == course,
            Or(
                dtypes.session_type(slot) == dtypes.SessionType.tutorial,
                dtypes.session_type(slot) == dtypes.SessionType.practicum,
            )
        ),
        (dtypes.students_amount(course) / dtypes.groups_amount(course)) <= dtypes.capacity(dtypes.room(slot))
    )

def seance_supporte_par_salle(slot) -> BoolRef:
    return Or(
        And(
            dtypes.session_type(slot) == dtypes.SessionType.lecture,
            dtypes.supporte_lecture(dtypes.room(slot))
        ),
        And(
            dtypes.session_type(slot) == dtypes.SessionType.tutorial,
            dtypes.supporte_tutorial(dtypes.room(slot))
        ),
        And(
            dtypes.session_type(slot) == dtypes.SessionType.practicum,
            dtypes.supporte_practicum(dtypes.room(slot))
        ),
        And(
            dtypes.session_type(slot) == dtypes.SessionType.midterm,
            dtypes.supporte_midterm(dtypes.room(slot))
        ),
        And(
            dtypes.session_type(slot) == dtypes.SessionType.exam,
            dtypes.supporte_exam(dtypes.room(slot))
        ),
        And(
            dtypes.session_type(slot) == dtypes.SessionType.oral,
            dtypes.supporte_oral(dtypes.room(slot))
        ),
    )

def type_seance_donnee(slot) -> BoolRef:
    return dtypes.order_session_type(dtypes.order_position(slot)) == dtypes.session_type(slot)

def duree_seance(slot) -> BoolRef:
    return last(dtypes.slot_start_time(slot), dtypes.slot_end_time(slot), dtypes.order_duration(dtypes.order_position(slot)))

def attribuer_creneau(slots: list, order_position) -> list[BoolRef]:
    constrs = []
    i = randint(0, len(slots)-1)
    for j in range(len(slots)):
        if i == j:
            constrs.append(dtypes.order_position(slots[i]) == order_position)
        else:
            constrs.append(dtypes.order_position(slots[i]) != order_position)
    return Or(*constrs)

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
