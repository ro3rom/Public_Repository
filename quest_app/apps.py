from django.apps import AppConfig

class QuestAppConfig(AppConfig):
    name = 'quest_app'

    def ready(self):
        import quest_app.signals  # signals.pyをインポート
