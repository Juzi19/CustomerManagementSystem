from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import CustomUser  # Passe das an, falls dein User-Modell anders heißt
from costumer_manangement_system.settings import get_secret

class Command(BaseCommand):
    help = 'Creates a superuser if no users exist'

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = get_secret('ADMIN_PASSWORD')  # Sicherstellen, dass das Passwort später geändert wird
                self.stdout.write(self.style.SUCCESS(f'Creating superuser {username} ({email})'))

                admin = CustomUser.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
        else:
            self.stdout.write(self.style.WARNING('Admin accounts can only be initialized if no accounts exist'))
