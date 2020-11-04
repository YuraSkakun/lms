from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from teacher.models import Teacher
from teacher.forms import TeacherAddForm, TeacherEditForm, TeacherDeleteForm


def generate_teachers(request):
    for _ in range(1):
        Teacher.generate_teacher()
    abc = Teacher.objects.all()
    return HttpResponse(abc)


def teachers_list(request):
    qsg = Teacher.objects.all()

    if request.GET.get('tfname') or request.GET.get('tlname') or request.GET.get('email'):
        qsg = qsg.filter(Q(first_name=request.GET.get('tfname')) | Q(
            last_name=request.GET.get('tlname')) | Q(email=request.GET.get('email')))

    return render(
        request=request,
        template_name='teachers_list.html',
        context={'teachers_list': qsg,
                 'title': 'Teachers list'
                 }
    )


def teachers_add(request):
    if request.method == 'POST':
        form = TeacherAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))

    else:
        form = TeacherAddForm()

    return render(
        request=request,
        template_name='teachers_add.html',
        context={'form': form,
                 'title': 'Teachers add'
                 }
    )


def teachers_edit(request, id):
    try:
        teacher = Teacher.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'teacher with id={id} does not exist')

    if request.method == 'POST':
        form = TeacherEditForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))
    else:
        form = TeacherEditForm(
            instance=teacher
        )

    return render(
        request=request,
        template_name='teachers_edit.html',
        context={
            'form': form,
            'title': 'Teachers edit',
            'teacher': teacher
        }
    )


def teachers_delete(request, id):
    try:
        teacher = Teacher.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'teacher with id={id} does not exist')

    if request.method == 'POST':
        form = TeacherDeleteForm(request.POST, instance=teacher)
        teacher.delete()
        if form.is_valid():
            return HttpResponseRedirect(reverse('teachers:list'))
    else:
        form = TeacherDeleteForm(
            instance=teacher
        )

    return render(
        request=request,
        template_name='teachers_delete.html',
        context={
            'form': form,
            'title': 'Teacher delete'
        },
    )


class TeachersListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers_list.html'
    context_object_name = 'teachers_list'
    login_url = reverse_lazy('login')
    paginate_by = 2

    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        qs = qs.order_by('-id')

        if request.GET.get('tfname') or request.GET.get('tlname') or request.GET.get('email'):
            qs = qs.filter(Q(first_name=request.GET.get('tfname')) | Q(
                last_name=request.GET.get('tlname')) | Q(email=request.GET.get('email')))

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Teacher list'
        return context


class TeachersUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    template_name = 'teachers_edit.html'
    form_class = TeacherEditForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('teachers:list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Edit teachers'
        return context


class TeachersCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    template_name = 'teachers_add.html'
    form_class = TeacherAddForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('teachers:list')


class TeachersDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers_delete.html'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('teachers:list')
