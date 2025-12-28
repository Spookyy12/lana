from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        try:
            User = get_user_model()

            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@test.local',
                    password='admin12345'
                )
                print('✅ Test superuser created: admin / admin12345')

        except (OperationalError, ProgrammingError):
            # база ещё не готова — пропускаем
            pass
