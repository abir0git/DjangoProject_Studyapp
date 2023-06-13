from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id' : 1, 'name' : 'abir'},
#     {'id' : 2, 'name' : 'roy'},
#     {'id' : 3, 'name' : 'abmj'},
# ]

def home(request):
    q = request.GET.get('q')
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    return render(request, 'bas/home.html', {'Rooms':rooms, 'Topics' : topics})

def room(request, pk):
    # room = None
    # for r in rooms:
    #     if(r['id'] == int(pk)):
    #         room = r
    room = Room.objects.get(id=pk)
    context = {'Room' : room}
    return render(request, 'bas/room.html', context)

def createroom(request):
    form = RoomForm()
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'bas/room_form.html', context)

def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if(request.method == 'POST'):
        form = RoomForm(request.POST, instance=room) # to update
        if(form.is_valid):
            form.save()
            return redirect(f"/room/{room.id}")
    context = {'form' : form}
    return render(request, 'bas/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj' : room}
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'bas/delete.html', context)