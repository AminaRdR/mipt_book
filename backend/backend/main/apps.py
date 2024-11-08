from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging
import datetime
from collections import namedtuple


def get_week_day():
    now = datetime.datetime.now()
    day_of_week = now.weekday()
    return day_of_week


def get_time(time_string):
    return datetime.datetime.strptime(time_string, "%H:%M")


def get_time_slot():
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
        CurrentPair(13, "04:30", "06:00")]
    now = datetime.datetime.now()

    for current_pair in current_pair_list:
        if get_time(current_pair.start_time).time() < now.time() < get_time(current_pair.end_time).time():
            return current_pair.number
    return -1

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        logging.info("START SETTING UP APPLICATION")
        Audience = self.get_model("Audience")
        Book = self.get_model("Book")

        def update_audience_day(week_day):
            for audience in Audience.objects.all():
                if week_day < 6:
                    # TODO: audience.week_pairs[week_day]
                    audience.day_history.pair = audience.week_pairs[week_day-1]
                elif week_day == 6:
                    audience.make_all_free()
                audience.day_history.save()
                audience.save()

        def clear_audience(time_slot: int):
            audiences = Audience.objects.all()
            for audience in audiences:
                audience.clear_booking(time_slot - 1)
                audience.save()


        def load_booking():
            all_books = Book.objects.all()
            for book in all_books:
                book.load_booking()

        my_week_day = get_week_day()
        my_time_slot = get_time_slot()
        update_audience_day(my_week_day)
        clear_audience(my_time_slot)

        load_booking()

        run_command_after_startup()

@receiver(post_migrate, sender='main')
def run_command_after_migration(sender, kwargs):
    run_command_after_startup()


def run_command_after_startup():
    logging.info(f"Текущий день недели: {get_week_day()}")
    logging.info(f"Текущий временной слот: {get_time_slot()}")
    logging.info("END SETTING UP APPLICATION")
