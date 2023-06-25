from rest_framework.decorators import api_view
from rest_framework.response import Response
from bas.models import Room
from .serializers import RoomSerializer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def addReview(request):
    if(request.method == 'POST'):
        pkr = request.POST.get('pkr')
        review = request.POST.get('review')
        # print(pkr, review)
        room = Room.objects.get(id=pkr)
        room.outside_review = str(room.outside_review) + "##" + str(review)
        room.save()
        return redirect("http://127.0.0.1:5500/outside.html")