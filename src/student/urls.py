from django.urls import path

from student.views import students_list, generate_students, students_add, students_edit, students_delete, \
    StudentsListView, StudentsUpdateView, StudentsCreateView, StudentsDeleteView

app_name = 'students'

urlpatterns = [
    # path('', students_list, name='list'),
    # path('', MyView.as_view(), name='list'),
    path('', StudentsListView.as_view(), name='list'),

    path('gen/', generate_students, name='gen'),

    # path('add/', students_add, name='add'),
    path('add/', StudentsCreateView.as_view(), name='add'),

    # path('edit/<int:id>', students_edit, name='edit'),
    path('edit/<int:pk>', StudentsUpdateView.as_view(), name='edit'),

    # path('delete/<int:id>', students_delete, name='delete'),
    path('delete/<int:pk>', StudentsDeleteView.as_view(), name='delete'),
]
