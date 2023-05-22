from z3 import Datatype, IntSort, ArraySort, Solver, Const, BoolSort

Datetime = Datatype('Datetime')
Datetime.declare(
    'cdt',
    ('day', IntSort()),
    ('month', IntSort()),
    ('year', IntSort()),
    ('hour', IntSort()),
    ('minutes', IntSort())
)
Datetime = Datetime.create()

month = Datetime.month
day = Datetime.day
year = Datetime.year
hour = Datetime.hour
minutes = Datetime.minutes

DateTimeInterval = Datatype('DateTimeInterval')
DateTimeInterval.declare(
    'cdti',
    ('start', Datetime),
    ('end', Datetime)
)
DateTimeInterval = DateTimeInterval.create()
start_time = DateTimeInterval.start
end_time = DateTimeInterval.end


Room = Datatype('Room')
Room.declare(
    'croom',
    ('room_id', IntSort()),
    ('capacity', IntSort()),
    ('lecture', BoolSort()),
    ('tutorial', BoolSort()),
    ('practicum', BoolSort()),
    ('midterm', BoolSort()),
    ('exam', BoolSort()),
    ('oral', BoolSort()),
)
Room = Room.create()

room_id = Room.room_id
capacity = Room.capacity

Course = Datatype('Course')
Course.declare(
    'ccourse',
    ('id', IntSort()),
    ('start', Datetime),
)
Course = Course.create()
course_start = Course.start

SessionType = Datatype('SessionType')
SessionType.declare('lecture')
SessionType.declare('tutorial')
SessionType.declare('practicum')
SessionType.declare('midterm')
SessionType.declare('exam')
SessionType.declare('oral')
SessionType = SessionType.create()

OrderPosition = Datatype('OrderPosition')
OrderPosition.declare(
    'order',
    ('order_position', IntSort()),
    ('session_type', SessionType),
    ('course_id', IntSort()),
    ('duration', IntSort()),
)
OrderPosition = OrderPosition.create()

indice_position = OrderPosition.order_position

Slot = Datatype('Slot')
Slot.declare(
    ('cslot'),
    ('assigned', BoolSort()),
    ('order_position', OrderPosition),
    ('start_time', Datetime),
    ('end_time', Datetime),
    ('session_type', SessionType),
    ('subject', Course),
    ('room', Room)
)
Slot = Slot.create()

assigned = Slot.assigned
slot_start_time = Slot.start_time
slot_end_time = Slot.end_time
session_type = Slot.session_type
subject = Slot.subject
room = Slot.room
order_position = Slot.order_position

# def datetimes_from_interval(
#         start_hour: int, start_minute: int,
#         end_hour: int, end_minute: int
# ):
#     res = []
#     for i in range(end_hour-start_hour):
#         res 

if __name__ == '__main__':
    s = Solver()
    a = Const('a', Slot)
    s.add(hour(slot_start_time(a)) > 1020)
    print(s.check())
    print(s.model())