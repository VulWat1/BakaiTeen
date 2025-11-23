# from django.apps import AppConfig


# class QuestConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'quest'

from django.apps import AppConfig


class QuestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quest'

    def ready(self):
        import quest.signals  # import signals to activate them
