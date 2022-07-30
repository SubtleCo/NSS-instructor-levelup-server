"""Viewset for Events"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer


class EventView(ViewSet):
    """A ViewSet for events"""

    def retrieve(self, request: Request, pk):
        """Get a single event"""
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request: Request):
        """Get all events"""
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()
        game = request.query_params.get("game")
        if game:
            events = events.filter(game_id=game)

        # check to see if the gamer is attending each event, set "joined"
        for event in events:
            event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request: Request):
        """Handles POST requests for games"""
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk):
        """Handles a PUT request on an event, returning no body and a 204 on success"""
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles a DELETE request on an event"""
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Handles a post request for signing up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': "nothing to see here"}, status=status.HTTP_201_CREATED)


    @action(methods=["delete"], detail=True)
    def leave(self, request, pk):
        """Handles a delete request for leaving an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': "Have fun being a hermit Alex"}, status=status.HTTP_204_NO_CONTENT)
        
    
class EventSerializer(serializers.ModelSerializer):
    """Serializer for Events"""
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'joined')
        depth = 1


class CreateEventSerializer(serializers.ModelSerializer):
    """Serializes and validates a created event"""
    class Meta:
        model = Event
        fields = (
            'id',
            'game',
            'description',
            'date',
            'time'
        )
