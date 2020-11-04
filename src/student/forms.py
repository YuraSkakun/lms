from django.core.exceptions import ValidationError
from django.forms import ModelForm
from student.models import Student


# class StudentAddForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'
#         fields = ['first_name', 'last_name']


class StudentBaseForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class StudentAddForm(StudentBaseForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.all().filter(email=email).exists():
            raise ValidationError('Email already exist')
        return email


class StudentEditForm(StudentBaseForm):

    def clean_email(self):

        email = self.cleaned_data['email']

        already_exists = Student.objects. \
            filter(email=email). \
            exclude(id=self.instance.id). \
            count() > 0

        if already_exists:
            raise ValidationError('Email already exists!')

        return email


class StudentDeleteForm(StudentBaseForm):
    pass
