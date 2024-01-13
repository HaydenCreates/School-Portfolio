from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from users.models import Profile  # Import your Profile model

class Command(BaseCommand):
    help = 'Create custom permissions for profiles'

    def handle(self, *args, **kwargs):
        # Get the content type for the Profile model
        content_type = ContentType.objects.get_for_model(Profile)

        # Create a permission for teachers
        teacher_permission = Permission.objects.create(
            codename='can_view_all',
            name='TeacherPermissions',
            content_type=content_type,
        )

        # Create a permission for students
        student_permission = Permission.objects.create(
            codename='can_view_individual',
            name='StudentPermissions',
            content_type=content_type,
        )

        self.stdout.write(self.style.SUCCESS('Custom permissions created successfully'))
