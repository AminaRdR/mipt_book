from typing import Tuple, Any

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin
from django.contrib.postgres import fields
from collections import namedtuple


class Pair(models.Model):
    name = models.CharField(max_length=64, blank=False)
    time_slot_index = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(14),
            MinValueValidator(1)
        ])
    week_day_index = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ])
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Pair: {self.name}'

    def get_time_slot(self) -> tuple[Any, Any, Any]:
        CurrentPair = namedtuple('CurrentPair', ['number', 'start_time', 'end_time'])
        current_pair_list = [
            CurrentPair(1, "09:00", "10:25"),
            CurrentPair(2, "10:25", "12:10"),
            CurrentPair(3, "12:10", "13:55"),
            CurrentPair(4, "13:55", "15:30"),
            CurrentPair(5, "15:30", "17:05"),
            CurrentPair(6, "17:05", "18:30"),
            CurrentPair(7, "18:30", "20:00"),
            CurrentPair(8, "20:00", "22:00"),
            CurrentPair(9, "22:00", "23:59"),
            CurrentPair(10, "00:00", "01:30"),
            CurrentPair(11, "01:30", "03:00"),
            CurrentPair(12, "03:00", "04:30"),
            CurrentPair(13, "04:30", "06:00"),
            CurrentPair(14, "06:00", "08:00")]
        _ = next(pair for pair in current_pair_list if pair.number == self.time_slot_index)
        return _.number, _.start_time, _.end_time

    def get_week_day(self) -> str:
        current_day_list = [
            (1, "Понедельник"),
            (2, "Вторник"),
            (3, "Среда"),
            (4, "Четверг"),
            (5, "Пятница"),
            (6, "Суббота"),
            (7, "Воскресенье")]
        _ = next(pair for pair in current_day_list if pair[0] == self.week_day_index)
        return _[1]


class EventType(models.Model):
    name = models.CharField(max_length=64, blank="Пользовательское мероприятие")
    rules = models.CharField(max_length=64, blank="Гость")
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'EventType: {self.name}'


class EventItem(models.Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=255, blank=False)
    audience_number = models.CharField(max_length=64, blank=True)

    pair = models.ForeignKey(
        "Pair",
        on_delete=models.CASCADE,
        related_name="event_item_pair",
        blank=False,
        null=False)

    owner_user_wallet = models.CharField(max_length=255, blank=False)

    event_type = models.ForeignKey(
        "EventType",
        on_delete=models.CASCADE,
        related_name="event_type_of_event",
        blank=False,
        null=False)

    def __str__(self):
        return f'EventItem: {self.name} | {self.pair} | {self.event_type}'

    def setup_pair(self, time_slot_index: int, week_day_index: int):
        if time_slot_index in range(1,15) and week_day_index in range(1,8):
            current_pair = Pair.objects.get(
                time_slot_index=time_slot_index,
                week_day_index=week_day_index
            )
            self.pair = current_pair
            return True
        else:
            return False

    def setup_user(self, username: str):
        if len(username) < 50:
            self.owner_user_wallet = username
            return True
        else:
            return False


class UserSearch(models.Model):
    data = models.CharField(max_length=150, blank=False)
    owner_user_wallet = models.CharField(max_length=255, blank=False)
    order_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f'Search: u={self.owner_user_wallet} | t={self.data}'

    def get_result(self):
        return {
            "result": "This is text",
            "data": self.data,
            "user": self.owner_user_wallet,
            "request_time": self.order_time
        }


@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", "time_slot_index", "week_day_index", "description", )


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "rules", "description")
    list_display = ("id", "name", "rules", "description", )


@admin.register(EventItem)
class EventItemAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description", "owner_user_wallet")
    list_display = ("id", "name", "description", "owner_user_wallet", )


@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    search_fields = ("id", "data", "owner_user_wallet", "order_time")
    list_display = ("id", "data", "owner_user_wallet", "order_time", )
