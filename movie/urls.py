from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import *
urlpatterns = [
    path('movie/', MovieList.as_view(),name='movie_list'),
    path('movie-filter/',MovieList_Filter.as_view(),name='filter'),
    path('movie-search/',MovieList_Search.as_view(),name='search'),
    path('detail/<pk>/',MovieDetail.as_view(),name='movie_detail'),
    path('stream/',streamlist.as_view(),name='streamlist'),
    path('review/all/',reviewList.as_view(),name='reviewlist'),
    path('review/<pk>/',reviewDetail.as_view(),name='review_detail'),
    path('review/<pk>/all/',ReviewList.as_view(),name='review_list'),
    path('review/<pk>/create/',CreateReview.as_view(),name='create_review'),
    path('account/login/',ObtainAuthToken.as_view(),name='login'),
    path('account/register/',register_user,name='register'),
    path('account/logout/',logout_view,name='logout'),
    path('review/',userReview.as_view(),name='user_review'),
]