from z3 import Datatype, IntSort, ArraySort, Solver, Const, And, Int

Datetime = Datatype('Datetime')
Datetime.declare(
    'cdt',
    ('month', IntSort()),
    ('day', IntSort()),
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


Room = Datatype('Room')
Room.declare(
    'croom',
    ('room_id', IntSort()),
    ('capacity', IntSort()),
    ('session_types', ArraySort(IntSort(), IntSort())),
    ('availabilities', ArraySort(IntSort(), Datetime))
)
Room = Room.create()

room_id = Room.room_id
capacity = Room.capacity
session_types = Room.session_types
availabilities = Room.availabilities

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

# SlotList = Datatype('SlotList')
# SlotList.declare('empty')
# SlotList.declare(
#     'head',
#     ('value', Slot),
#     ('tail', SlotList)
# )
# SlotList = SlotList.create()

# IntList = Datatype('IntList')
# IntList.declare('empty')
# IntList.declare(
#     'head',
#     ('value', IntSort()),
#     ('tail', IntList)
# )
# IntList = IntList.create()

X = [ Int('x%s' % i) for i in range(5) ]
Y = [ Int('y%s' % i) for i in range(5) ]

if __name__ == '__main__':
    s = Solver()
    # a = Const('a', Slot)
    # s.add(hour(slot_start_time(a)) > 1020)
    X_gt_Y = [ X[i] > Y[i] for i in range(5) ]
    c = And(X_gt_Y)
    s.add(c, )
    print(s.check())
    print(s.model())