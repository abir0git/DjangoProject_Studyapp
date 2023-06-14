from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = '__all__' # giving all features of room model
        fields = ('name', 'topic', 'description')