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
    ('practicum', BoolSort())
)
Room = Room.create()

room_id = Room.room_id
capacity = Room.capacity

Slot = Datatype('Slot')
Slot.declare(
    ('cslot'),
    ('start_time', Datetime),
    ('end_time', Datetime),
    ('session_type', IntSort()),
    ('subject', IntSort()),
    ('room', Room)
)
Slot = Slot.create()

slot_start_time = Slot.start_time
slot_end_time = Slot.end_time
session_type = Slot.session_type
subject = Slot.subject
room = Slot.room

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