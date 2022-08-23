from dataclasses import dataclass
from os import stat
from ..models import WatchList, StreamPlatform
from .serializers import WatchSerializer, StreamPlatformSerializer
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView


class StreamPlatformAV(APIView):

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamDetailsAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):

    def get(self, request):
        Movies = WatchList.objects.all()
        serializer = WatchSerializer(Movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailsAV(APIView):

    def get(self, request, pk):

        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # @api_view(['GET', 'POST'])
        # def movie_list(request):

        #     if request.method == 'GET':
        #         Movies = Movie.objects.all()
        #         serializer = MovieSerializer(Movies, many=True)
        #         return Response(serializer.data)

        #     if request.method == 'POST':
        #         serializer = MovieSerializer(data=request.data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return Response(serializer.data)
        #         else:
        #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # @api_view(['GET', 'PUT', 'DELETE'])
        # def movie_details(request, pk):

        #     if request.method == 'GET':
        #         try:
        #             movie = Movie.objects.get(pk=pk)
        #         except Movie.DoesNotExist:
        #             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        #         serializer = MovieSerializer(movie)
        #         return Response(serializer.data)

        #     if request.method == 'PUT':
        #         movie = Movie.objects.get(pk=pk)
        #         serializer = MovieSerializer(movie, data=request.data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return Response(serializer.data)
        #         else:
        #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     if request.method == 'DELETE':
        #         movie = Movie.objects.get(pk=pk)
        #         movie.delete()
        #         return Response(status=status.HTTP_204_NO_CONTENT)
