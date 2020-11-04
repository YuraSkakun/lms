from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from group.forms import GroupAddForm, GroupEditForm, GroupDeleteForm
from group.models import Group

# Create your views here.


def generate_groups(request, num=1):
    for _ in range(num):
        Group.generate_group()
    qs = Group.objects.all()
    new_groups = qs[len(qs) - num:]
    result = '<br>'.join(
        str(group)
        for group in new_groups
    )
    return HttpResponse(result)


def groups_list(request):
    qs = Group.objects.all()

    if request.GET.get('gname'):
        qs = qs.filter(name=request.GET.get('gname'))

    if request.GET.get('gcourse'):
        qs = qs.filter(course=request.GET.get('gcourse'))

    # if request.GET.get('gname') or request.GET.get('gcourse'):
    #     qs =qs.filter(
    #         Q(name=request.GET.get('gname')) | Q(
    #             course=request.GET.get('gcourse'))
    #         )

    # result = '<br>'.join(
    #     str(group)
    #     for group in qs
    # )
    # return HttpResponse(result)
    return render(
        request=request,
        template_name='groups_list.html',
        context={
            'groups_list': qs,
            'title': 'Groups list'
        }
    )


def groups_add(request):

    if request.method == 'POST':
        form = GroupAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groups:list'))
    else:
        form = GroupAddForm

    return render(
        request=request,
        template_name='groups_add.html',
        context={
            'form': form,
            'title': 'Groups add'
        }
    )


def groups_edit(request, id):
    try:
        group = Group.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Group with id={id} doesn\'t exist')

    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)

        if form.is_valid():
            group = form.save()
            print(f'Grope has been saved: {group}')
            return HttpResponseRedirect(reverse('groups:list'))
    else:
        form = GroupEditForm(
            instance=group
        )

    return render(
        request=request,
        template_name='groups_edit.html',
        context={
            'form': form,
            'title': 'Group edit',
            'group': group
        }
    )


def groups_delete(request, id):
    try:
        group = Group.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Group with id={id} doesn\'t exist')

    if request.method == 'POST':
        form = GroupDeleteForm(request.POST, instance=group)

        group.delete()
        if form.is_valid():
            return HttpResponseRedirect(reverse('groups:list'))
    else:
        form = GroupDeleteForm(
            instance=group
        )

    return render(
        request=request,
        template_name='groups_delete.html',
        context={
            'form': form,
            'title': 'Group delete',
        }
    )


class GroupsListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups_list.html'
    context_object_name = 'groups_list'
    login_url = reverse_lazy('login')
    paginate_by = 3

    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        qs = qs.order_by('-id')

        # if request.GET.get('gname'):
        #     qs = qs.filter(name=request.GET.get('gname'))
        #
        # if request.GET.get('gcourse'):
        #     qs = qs.filter(course=request.GET.get('gcourse'))

        if request.GET.get('gname') or request.GET.get('gcourse'):
            qs = qs.filter(Q(name=request.GET.get('gname')) | Q(
                course=request.GET.get('course')))

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Groups list'
        return context


class GroupsUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'groups_edit.html'
    form_class = GroupEditForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('groups:list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Edit group'
        return context


class GroupsCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups_add.html'
    form_class = GroupAddForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('groups:list')


class GroupsDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'groups_delete.html'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('groups:list')
