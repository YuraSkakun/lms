from django.core.exceptions import ValidationError
from django.forms import ModelForm
from teacher.models import Teacher


class TeacherBaseForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherAddForm(TeacherBaseForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if Teacher.objects.all().filter(email=email).exists():
            raise ValidationError('Email already exist')
        return email


class TeacherEditForm(TeacherBaseForm):

    pass


class TeacherDeleteForm(TeacherBaseForm):
    pass
