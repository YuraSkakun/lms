from django.forms import ModelForm
from group.models import Group


class GroupBaseForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class GroupAddForm(GroupBaseForm):
    pass


class GroupEditForm(GroupBaseForm):
    pass


class GroupDeleteForm(GroupBaseForm):
    pass
