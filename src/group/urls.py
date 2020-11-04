from django.urls import path

from group.views import groups_list, generate_groups, groups_add, groups_edit, groups_delete, GroupsListView, \
    GroupsUpdateView, GroupsCreateView, GroupsDeleteView

app_name = 'groups'

urlpatterns = [
    # path('', groups_list, name='list'),
    path('', GroupsListView.as_view(), name='list'),

    path('gen/', generate_groups, name='gen'),

    # path('add/', groups_add, name='add'),
    path('add/', GroupsCreateView.as_view(), name='add'),

    # path('edit/<int:id>', groups_edit, name='edit'),
    path('edit/<int:pk>', GroupsUpdateView.as_view(), name='edit'),

    # path('delete/<int:id>', groups_delete, name='delete'),
    path('delete/<int:pk>', GroupsDeleteView.as_view(), name='delete'),
]
