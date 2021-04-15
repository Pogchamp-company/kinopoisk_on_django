from django.http import Http404
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Movie, Score
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from .serializers import MovieSerializer, PersonSerializer
from person.models import Person, Photo

from utils.mixins import Image


def movie_page(request, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    if not movie:
        raise Http404

    context = dict(
        movie=movie,
        recommendations=Movie.objects.filter(~Q(id=movie_id))[:6],
        score=Score.objects.filter(movie=movie, user=request.user).first(),
        score_count=Score.objects.filter(movie=movie).count()
    )
    return render(request, 'movies/movie_page.html', context)


class ScoreView(APIView):
    def put(self, request: Request, movie_id: int):
        score_value = int(request.GET['score'])
        movie = Movie.objects.get(pk=movie_id)
        if not movie:
            return Response({'errors': 'Movie not found'}, status.HTTP_404_NOT_FOUND)
        score = Score.objects.filter(movie=movie, user=request.user).first()
        if not score:
            score = Score(movie=movie,
                          user=request.user)
        score.value = score_value
        score.save()
        return Response({'result': 'success'}, status.HTTP_200_OK)


class SearchView(APIView):
    movie_serializer_class = MovieSerializer
    person_serializer_class = PersonSerializer

    def get(self, request: Request):
        query_filter = request.GET.get('query')
        if not query_filter:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(
            Q(title__icontains=query_filter) | Q(original_title__icontains=query_filter))[:3]
        persons = Person.objects.filter(
            Q(fullname__icontains=query_filter) | Q(ru_fullname__icontains=query_filter))[:3]

        response = {
            # 'topResult': {},
            'movies': [self.movie_serializer_class(movie).data for movie in movies],
            'persons': [self.person_serializer_class(person).data for person in persons]
        }

        return Response(response, status=status.HTTP_200_OK)
