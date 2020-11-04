from django.core.management.base import BaseCommand, CommandError
from group.models import Group


class Command(BaseCommand):
    help = 'Generate new Group or Groups'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=0)

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        try:
            for _ in range(count):
                Group.generate_group()

        except Exception as ex:
            raise CommandError('Generate group failed: "%s"' % ex)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} group(s)'))
