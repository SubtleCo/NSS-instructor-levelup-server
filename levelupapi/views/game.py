"""Viewset for Games"""
from django.http import HttpResponseServerError
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """A ViewSet for games"""

    def retrieve(self, request, pk):
        """Get a single event"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get all games"""
        games = Game.objects.all()
        
        # Filter by GameType if present
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request: Request):
        """Handles POST requests for games"""
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk):
        """Handles PUT request for a game, returning a 204 with no body on success"""
        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Games"""

    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1


class CreateGameSerializer(serializers.ModelSerializer):
    """Represents and validates a created game"""
    class Meta:
        model = Game
        fields = (
            'id',
            'title',
            'maker',
            'number_of_players',
            'skill_level',
            'game_type'
        )
