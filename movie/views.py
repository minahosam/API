from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authtoken.models import Token
# Create your views here.
class MovieList_Filter(generics.ListAPIView):
    serializer_class=movieSerializer
    queryset=Movie.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'moviePlatform__name']
class MovieList_Search(generics.ListAPIView):
    serializer_class=movieSerializer
    queryset=Movie.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'moviePlatform__name']
class MovieList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):        
        movie = Movie.objects.all()
        serialize=movieSerializer(movie,many=True)
        return Response(serialize.data)
    def post(self, request):
        serialize=movieSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serialize.errors)
class MovieDetail(APIView):
    def get(self,request,pk):
        movie=Movie.objects.get(pk=pk)
        serialize=movieSerializer(movie)
        return Response(serialize.data)
    def put(self,request,pk):
        movie=Movie.objects.get(pk=pk)
        serialize=movieSerializer(movie,data=request.data)
        return Response(serialize.data)
    def delete(self, request,pk):
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class streamlist(APIView):
    def get(self,request):
        stream=StreamPlatform.objects.all()
        serialize=streamPlatformSerializer(stream,many=True,context={'request': request})
        return Response(serialize.data)
    def post(self, request):
        serialize=streamPlatformSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)
class reviewList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = review.objects.all()
    serializer_class = reviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class reviewDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = review.objects.all()
    serializer_class = reviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class ReviewList(generics.ListAPIView):
    serializer_class=reviewSerializer
    def get_queryset(self):
        pk=self.kwargs['pk']
        print(pk)
        request_movie=review.objects.filter(review_movie=pk)
        return request_movie
class CreateReview(generics.CreateAPIView):
    serializer_class=reviewSerializer
    def get_queryset(self):
        return review.objects.all()
    def perform_create(self,serializer):
        pk=self.kwargs['pk']
        request_movie=Movie.objects.get(pk=pk)
        author=self.request.user
        review__=review.objects.filter(review_movie=request_movie,review_author=author)
        if review__.exists():
            raise ValidationError('Only One Review Allowed')
        if request_movie.people_rating == 0:
            request_movie.avg_rating=serializer.validated_data['rate']
        else:
            request_movie.avg_rating=(request_movie.avg_rating + serializer.validated_data['rate'])/2
        request_movie.people_rating=request_movie.people_rating + 1
        request_movie.save()
        serializer.save(review_movie=request_movie,review_author=author)
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movies=Movie.objects.all()
#         serialize=movieSerializer(movies,many=True)
#         return Response(serialize.data)
#     elif request.method == 'POST':
#         serialize=movieSerializer(data=request.data)
#         if serialize.is_valid():
#             serialize.save()
#             return Response(serialize.data)
#         else:
#             return Response(serialize.errors)
# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
#     if request.method == 'GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#             serialize=movieSerializer(movie) 
#             return Response(serialize.data)
#         except Movie.DoesNotExist:
#             return Response({'file':'not found'},status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         movie=Movie.objects.get(pk=pk)
#         serialize=movieSerializer(movie,data=request.data)
#         if serialize.is_valid():
#             serialize.save()
#             return Response(serialize.data)
#         else:
#             return Response(serialize.errors)
#     elif request.method == 'DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST',])
def register_user(request):
    if request.method == 'POST':
        serialize=userRegistration(data=request.data)
        data={}
        if serialize.is_valid():
            account=serialize.save()
            if account :
                data['response']='register successfully'
                data['username']=account.username
                data['email']=account.email
                token = Token.objects.get(user=account).key
                data['token']=token
                
            else:
                data['response']='error'
            return Response(data,status=status.HTTP_201_CREATED)  
        else:
            return Response(serialize.errors)
        
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
class userReview(generics.ListAPIView):
    serializer_class=reviewSerializer
    # def get_queryset(self):
    #     pk=self.kwargs['username']
    #     print(pk)
    #     user_rev=review.objects.filter(review_author__username=pk)
    #     return user_rev
    def get_queryset(self):
        pk=self.request.query_params.get('username')
        rev_user=review.objects.filter(review_author__username=pk)
        return rev_user