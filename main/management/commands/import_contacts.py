import csv
from django.core.management.base import BaseCommand
from main.models import Contact
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Import contacts from the CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=' File path of the CSV to import')
        parser.add_argument('user_id', type=int, help=' ID of the user to associate with the contacts')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(id=user_id)
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Contact.objects.create(
                        user=user,
                        name=row['name'],
                        phone_number=row['phone_number'],
                        email=row['email'],
                        address=row['address']
                    )
            self.stdout.write(self.style.SUCCESS('Contacts imported successfully'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with the given ID does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing contacts: {e}'))
