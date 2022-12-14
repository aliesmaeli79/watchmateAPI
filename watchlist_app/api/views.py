from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from . import pagination, throttling, serializers, permissions
from ..models import WatchList, StreamPlatform, Review


class UserReview(generics.ListAPIView):

    #queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    #permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):

    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie.")

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating +
                                serializer.validated_data['rating']) / 2

        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)


class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    #permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         Watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(
#             Watchlist, context={'request': request})
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(
#             data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):

    permission_classes = [permissions. IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamDetailsAV(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(
            platform, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchSerializer
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    pagination_class = pagination.WatchListCPagination


class WatchListAV(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        Movies = WatchList.objects.all()
        serializer = serializers.WatchSerializer(Movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailsAV(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):

        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchSerializer(movie, data=request.data)
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
