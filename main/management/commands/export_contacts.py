import csv
from django.core.management.base import BaseCommand
from main.models import Contact

class Command(BaseCommand):
    help = 'Export contacts to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=' File path of the CSV to export')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['name', 'email', 'phone_number', 'address']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for contact in Contact.objects.all():
                    writer.writerow({
                        'name': contact.name,
                        'email': contact.email,
                        'phone_number': contact.phone_number,
                        'address': contact.address
                    })
            self.stdout.write(self.style.SUCCESS('Contacts exported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting contacts: {e}'))
