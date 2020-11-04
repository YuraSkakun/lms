# Create your views here.

from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from student.forms import StudentAddForm, StudentEditForm, StudentDeleteForm
from student.models import Student

# Create your views here.


def generate_students(request, num=2):
    for _ in range(num):
        Student.generate_student()
    qs = Student.objects.all()
    new_students = qs[len(qs) - num:]
    result = '<br>'.join(
        str(student)
        for student in new_students
    )
    return HttpResponse(result)


def students_list(request):
    qs = Student.objects.all().select_related('group')

    if request.GET.get('fname'):
        qs = qs.filter(first_name=request.GET.get('fname'))

    if request.GET.get('lname'):
        qs = qs.filter(last_name=request.GET.get('lname'))

    # if request.GET.get('fname') or request.GET.get('lname'):
    #     qs =qs.filter(
    #         Q(first_name=request.GET.get('fname')) | Q(
    #             last_name=request.GET.get('lname'))
    #         )

    # result = '<br>'.join(
    #     str(student)
    #     for student in qs
    # )
    # return HttpResponse(result)
    return render(
        request=request,
        template_name='students_list.html',
        # context={'students_list': result}
        context={
            'students_list': qs,
            'title': 'Student list'
        }
    )


def students_add(request):

    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            # student = form.save()
            # print(f'Student created: {student} ')
            return HttpResponseRedirect(reverse('students:list'))
    else:
        form = StudentAddForm

    return render(
        request=request,
        template_name='students_add.html',
        context={
            'form': form,
            'title': 'Student add'
        }
    )


def students_edit(request, id):
    # return HttpResponse(f'EDIT STUDENT: {id}')
    try:
        student = Student.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Student with id={id} doesn\'t exist')

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))
    else:
        form = StudentEditForm(
            instance=student
        )

    return render(
        request=request,
        template_name='students_edit.html',
        context={
            'form': form,
            'title': 'Student edit',
            'student': student
        }
    )


def students_delete(request, id):
    try:
        student = Student.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Student with id={id} doesn\'t exist')

    # if request.method == 'POST':
    #     form = StudentDeleteForm(request.POST, instance=student)
    #     student.delete()
    #     if form.is_valid():
    #         return HttpResponseRedirect(reverse('students'))
    # else:
    #     form = StudentEditForm(
    #         instance=student
    #     )
    #
    # return render(
    #     request=request,
    #     template_name='students_delete.html',
    #     context={
    #         'form': form,
    #         'title': 'Student delete'
    #     }
    # )
    if request.method == 'POST':
        student.delete()
        return HttpResponseRedirect(reverse('students:list'))

    return render(
        request=request,
        template_name='students_delete.html',
        context={
            'student': student,
            'title': 'Student delete'
        }
    )


"""
class MyView:

    @classmethod
    def post(cls, request):
        print('post')

    @classmethod
    def get(cls, request):
        print('get')

    @classmethod
    def as_view(cls):
        def view(request):
            if request.method == 'POST':
                cls.post(request)
            elif request.method == 'GET':
                cls.get(request)
        return view
"""


class StudentsListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students_list.html'
    context_object_name = 'students_list'
    login_url = reverse_lazy('login')
    paginate_by = 5

    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        qs = qs.select_related('group')
        qs = qs.order_by('-gitid')

        if request.GET.get('fname'):
            qs = qs.filter(first_name=request.GET.get('fname'))

        if request.GET.get('lname'):
            qs = qs.filter(last_name=request.GET.get('lname'))

        # if request.GET.get('fname') or request.GET.get('lname'):
        #     qs =qs.filter(
        #         Q(first_name=request.GET.get('fname')) | Q(
        #             last_name=request.GET.get('lname'))
        #         )

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        # params = self.request.GET

        context['title'] = 'Student list'
        # context['query_params'] = '&'.join(f'{k}={v}' for k, v in params.items() if k != 'page')

        # context['query_params'] = urlencode({k: v for k, v in params.items() if k != 'page'})
        return context


class StudentsUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'students_edit.html'
    form_class = StudentEditForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('students:list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Edit student'
        return context


class StudentsCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'students_add.html'
    form_class = StudentAddForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('students:list')


class StudentsDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students_delete.html'
    # pk_url_kwarg = 'id'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        messages.success(self.request, 'Student has been deleted')
        return reverse('students:list')
