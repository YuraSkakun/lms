from django.core.management.base import BaseCommand, CommandError

from group.models import Group
from student.models import Student


class Command(BaseCommand):
    help = 'Generate N fake students'

    def add_arguments(self, parser):
        parser.add_argument('num_students', nargs='?', type=int, default=10)

    def handle(self, *args, **kwargs):
        num_students = kwargs['num_students']

        Student.objects.all().delete()
        groups = list(Group.objects.all())

        try:
            for _ in range(num_students):
                Student.generate_student(groups)

        except Exception as ex:
            raise CommandError('Generate students failed: "%s"' % ex)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_students} students'))
