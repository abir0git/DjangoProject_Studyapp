from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms  import UserCreationForm
# Create your views here.
from django.http import HttpResponse
from .models import Room, Topic, Message, Profile
from django.contrib.auth.models import User
from .forms import RoomForm, UserForm

# rooms = [
#     {'id' : 1, 'name' : 'abir'},
#     {'id' : 2, 'name' : 'roy'},
#     {'id' : 3, 'name' : 'abmj'},
# ]

def loginPage(request):
    page = 'login'
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.method =='POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
            return redirect('/login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')
        
    context = {'page' : page}
    return render(request, 'bas/login_reg.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if(request.method == 'POST'):
        # form = UserCreationForm(request.POST)
        # if(form.is_valid()):
        #     user = form.save(commit=False) # so getting user as return value
        #     # user.username = user.username.lower()
        username = request.POST.get('username')
        if(User.objects.filter(username=username).exists()):
            messages.error(request, f"Username already exists")
        else:
            fname = request.POST.get('fullname').split()[0]
            lname = request.POST.get('fullname')[len(fname)+1:]
            user = User.objects.create(
                username = username,
                password = request.POST.get('password'),
                first_name = fname,
                last_name = lname,
            )
            profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    context = {'page' : page, 'form' : form}
    return render(request, 'bas/login_reg.html', context)

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
    messg = Message.objects.filter(room__in=rooms)
    # for all messages in the rooms (got from documentaion)
    Topics = []
    for topic in topics:
        cnt = Room.objects.filter(
        Q(topic__name=topic.name)).count()
        if(cnt > 0):
            Topics.append({'topic' : topic, 'count' : cnt})

    users = User.objects.all()
    Profiles = Profile.objects.all()
    content = {'Rooms':rooms, 'Topics' : Topics, 
               'total_room':Room.objects.all().count, 'Messages' : messg, 'Profiles' : Profiles}
    return render(request, 'bas/home.html', content)

def room(request, pk):
    room = Room.objects.get(id=pk)
    message = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    # Special method to find all message of that room
    if(request.method == 'POST'):
        if('body' in request.POST):
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('Room', pk=room.id)
            # Room in uppercase because I give the name in urls.py
        if('delete-message' in request.POST):
            messg = Message.objects.get(id=request.POST['pkm'])
            messg.delete()
            return redirect('Room', pk=room.id)
    Profiles = Profile.objects.all()
    context = {'Room' : room, 'Message' : message, 'Participants' : participants, 'Profiles' : Profiles}
    return render(request, 'bas/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
        Q(host__username=user.username) &
        (Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q))
    ) 
    messg = user.message_set.all()
    topics = Topic.objects.all()
    Topics = []
    for topic in topics:
        cnt = Room.objects.filter(
        Q(host__username=user.username) & Q(topic__name=topic.name)).count()
        if(int(cnt) > 0):
            Topics.append({'topic' : topic, 'count' : cnt})
    Profiles = Profile.objects.all()
    context = {"user" : user, 'Rooms' : rooms, 'Messages' : messg, 'Topics' : Topics,
               'total_room' : Room.objects.filter(host__username=user.username).count,
                'Profiles' : Profiles }
    return render(request, 'bas/profile.html', context)

@login_required(login_url='/login') 
def createroom(request):
    # form = RoomForm()
    topics = Topic.objects.all()
    if(request.method == 'POST'):
        # form = RoomForm(request.POST)
        # form.instance.host = request.user
        # if(form.is_valid):
        #     form.save()
        #     return redirect('home')
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        room = Room.objects.create(
            host = request.user,
            name = request.POST.get('room_name'),
            description = request.POST.get('room_about'),
            topic = topic
        )
        return redirect(f"/room/{room.id}")
    context = {'Topics' : topics, 'type' : 'create'}
    return render(request, 'bas/room_form.html', context)

@login_required(login_url='/login') 
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    # form = RoomForm(instance=room)
    if(request.user != room.host):
        return HttpResponse("You are not allowed")
    if(request.method == 'POST'):
        # form = RoomForm(request.POST, instance=room) # to update
        # if(form.is_valid()):
        #     form.save()
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        room.name = request.POST.get('room_name')
        room.description = request.POST.get('room_about')
        room.topic = topic
        room.save()
        return redirect(f"/room/{room.id}")
    context = {'Topics' : topics, 'type' : 'update', 'Room' : room}
    return render(request, 'bas/room_form.html', context)

@login_required(login_url='/login') 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if(request.user != room.host):
        return HttpResponse("You are not allowed")
    context = {'obj' : room}
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'bas/delete.html', context)

@login_required(login_url='/login') 
def updateUser(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = UserForm(instance=request.user)
    if(request.method == "POST"):
        form = UserForm(request.POST, instance=user) # to update
        if(form.is_valid()):
            profile.bio = request.POST.get('bio')
            try:
                profile.avatar = request.FILES['profile_pic']
            except:
                pass
            profile.save()
            form.save()
            return redirect(f'/profile/{user.id}/')
    content = {'form' : form, 'Profiles' : [profile]} # need Profiles for navbar view
    return render(request, 'bas/update_user.html', content)