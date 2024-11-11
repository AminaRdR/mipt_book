from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        logging.info("START SETTING UP APPLICATION EVENTS")
        Pair = self.get_model("Pair")
        EventType = self.get_model("EventType")

        def update_base_data():
            # TODO: сделать обработку наличия типа и пары нормальной
            # Pair.objects.all().delete()
            # EventType.objects.all().delete()

            for week_day_index in range(1,8):
                for time_slot_index in range(1,15):
                    repeat_number = len(Pair.objects.filter(week_day_index=week_day_index, time_slot_index=time_slot_index))
                    if repeat_number == 0:
                        # Создаём новые
                        pair = Pair(
                            name="Пара",
                            week_day_index=week_day_index,
                            time_slot_index=time_slot_index,
                            description="Пара номер:")
                        pair.name = f"Пара {week_day_index} {time_slot_index}"
                        pair.description = f"Пара номер: {pair.get_week_day()} {pair.get_time_slot()}"
                        pair.save()
                        logging.info(f"Создана пара: {pair.name}")
                    elif repeat_number == 1:
                        # Пропускаем создание 
                        pass
                    else:
                        Pair.objects.filter(week_day_index=week_day_index, time_slot_index=time_slot_index).delete()
        update_base_data()
        type_user = EventType.objects.get_or_create(
            name="Пользовательское мероприятие",
            rules="user",
            description="Свободное мероприятие созданное пользователем"
        )
        type_seminar = EventType.objects.get_or_create(
            name="Семинар",
            rules="sem",
            description="Семинарская пара"
        )
        type_lecture = EventType.objects.get_or_create(
            name="Лекция",
            rules="loc",
            description="Лекционная пара"
        )
        type_extra = EventType.objects.get_or_create(
            name="Дополнительное",
            rules="ext",
            description="Дополнительное мероприятие в МФТИ"
        )
        for event_type in (type_user, type_seminar, type_lecture, type_extra):
            logging.info(f"Создан тип мероприятия: {event_type}")
            # event_type.save()

        run_command_after_startup()

@receiver(post_migrate, sender='events')
def run_command_after_migration(sender, kwargs):
    run_command_after_startup()

def run_command_after_startup():
    logging.info("END SETTING UP APPLICATION EVENTS")

