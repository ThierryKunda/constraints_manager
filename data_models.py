from enum import Enum
from datetime import datetime

from pydantic import BaseModel, constr, PositiveInt

import solver.z3_datatypes as z3_dt

DateTimeFormat = constr(regex=r"[0-9]{2}/[0-9]{2}/[0-9]{4}(-[0-9]{2}:[0-9]{2})?")
TimeFormat = constr(regex=r"[0-9]{2}:[0-9]{2}")


class SessionType(str, Enum):
    lecture = "lecture"
    tutorial = "tutorial"
    practicum = "practicum"
    midterm = "midterm"
    exam = "exam"
    oral = "oral"


class TimeInterval():
    start: TimeFormat
    end: TimeFormat


class DateTimeInterval():
    start: DateTimeFormat
    end: DateTimeFormat


class DayInterval(BaseModel):
    day_start: TimeFormat
    day_end: TimeFormat


class SchoolYearInterval(BaseModel):
    start_date: DateTimeFormat
    end_date: DateTimeFormat


class LunchPause(BaseModel):
    lunch_start: TimeFormat
    lunch_end: TimeFormat

class Test(BaseModel):
    session_type: SessionType
    test_start: TimeFormat
    test_end: TimeFormat


class ClassRoom(BaseModel):
    id: int
    capacity: int
    session_types: list[SessionType]

    def get_Z3_representation(self):
        return z3_dt.Room.croom(
            self.id,
            self.capacity,
            SessionType.lecture in self.session_types,
            SessionType.tutorial in self.session_types,
            SessionType.practicum in self.session_types,
            SessionType.midterm in self.session_types,
            SessionType.exam in self.session_types,
            SessionType.oral in self.session_types,
        )


class Group(BaseModel):
    group_id: PositiveInt
    size: PositiveInt


class Course(BaseModel):
    id: PositiveInt
    course_start: DateTimeFormat
    students_per_group: list[Group]


class SessionOrder(BaseModel):
    order_position: PositiveInt
    session_type: SessionType
    course_id: PositiveInt
    duration: PositiveInt


class GenerationRequest(BaseModel):
    day_interval: DayInterval
    school_year_interval: SchoolYearInterval
    lunch: LunchPause
    session_min_duration: int
    tests_dates: Test
    classrooms: list[ClassRoom]
    courses: list[Course]
    sessions_order: SessionOrder

class Slot(BaseModel):
    order: SessionOrder
    start: DateTimeFormat
    end: DateTimeFormat
    room_id: int
    course_id: int


if __name__ == "__main__":
    r0 = ClassRoom(id=1, capacity=100, session_types=[SessionType.tutorial, SessionType.practicum])
    print(r0)
    print(r0.get_Z3_representation())