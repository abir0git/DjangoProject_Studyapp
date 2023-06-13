from django.shortcuts import render, redirect
from django.db.models import Q
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
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    ) 
    # topic__name means name of topic , 2 _ used
    # contains have different search options
    topics = Topic.objects.all()
    content = {'Rooms':rooms, 'Topics' : topics, 'room_count':rooms.count}
    return render(request, 'bas/home.html', content)

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