from django.urls import path

from teacher.views import teachers_list, generate_teachers, teachers_add, teachers_edit, teachers_delete, \
    TeachersListView, TeachersCreateView, TeachersUpdateView, TeachersDeleteView

app_name = 'teachers'

urlpatterns = [
    # path('', teachers_list, name='list'),
    path('', TeachersListView.as_view(), name='list'),

    path('gen/', generate_teachers, name='gen'),

    # path('add/', teachers_add, name='add'),
    path('add/', TeachersCreateView.as_view(), name='add'),

    # path('edit/<int:id>', teachers_edit, name='edit'),
    path('edit/<int:pk>', TeachersUpdateView.as_view(), name='edit'),

    # path('delete/<int:id>', teachers_delete, name='delete'),
    path('delete/<int:pk>', TeachersDeleteView.as_view(), name='delete'),
]
