from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = '__all__' # giving all features of room model
        fields = ('name', 'topic', 'description')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']