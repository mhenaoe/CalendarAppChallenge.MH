from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


@dataclass
class Reminder:
    EMAIL: ClassVar[str]= "email"
    SYSTEM: ClassVar[str] = "system"

    date_time: datetime
    type: str = EMAIL

    def __str__(self) ->str:
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL):
        reminder = Reminder(date_time, type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
           del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self):
        return (f"ID: {id} n/ Event title: {self.title} n/ Description: {self.description}"
                f" n/ Time: {self.start_at} - {self.end_at}")

class Day:
    def __init__(self, date_: date):
        self.slots: dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self):
        current_time = time(0, 0)
        while current_time < time(23, 45):
            self.slots[current_time] = None
            minutes = current_time.hour * 60 + current_time.minute + 15
            hours, minutes = divmod(minutes, 60)
            current_time = time(hours, minutes)

    def add_event(self, event_id: str, start_at: time, end_at: time):
        current_time = start_at
        slots_to_fill = []
        while current_time < end_at:
            if self.slots.get(current_time) is not None:
                from app.services.util import slot_not_available_error
                slot_not_available_error()

        for slot in slots_to_fill:
            self.slots[slot] = event_id

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot]= None
                deleted= True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at:time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
               else:
                   self.slots[slot] = event_id




# TODO: Implement Calendar class here
