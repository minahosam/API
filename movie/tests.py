from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import *
# Create your tests here.
class registrationTestCase(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testCase",password="123456")
        self.stream = StreamPlatform.objects.create(name="testStream",about="testStream",url='http://www.test.com')
        self.token = Token.objects.get(user__username='testCase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    def test_register(self):
        data ={
            'username': 'test',
            'email': 'test@example.com',
            'password': '123456',
            'password2':'123456'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
class loginlogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testCase",password="P@sw0rd55")
    def test_login(self):
        data ={
            "username": "testCase",
            "password": "P@sw0rd55"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
class logoutTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="testCase",password="123456")
    def test_logout(self):
        self.token = Token.objects.get(user__username='testCase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
class streamTestCase(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testCase",password="123456")
        self.stream = StreamPlatform.objects.create(name="testStream",about="testStream",url='http://www.test.com')
        self.token = Token.objects.get(user__username='testCase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    def test_create(self):
        data ={
            "name": "testStream",
            "about": "testStream",
            'url': "http://www.test.com"
        }
        response = self.client.post(reverse('streamlist'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_list(self):
        response = self.client.get(reverse('streamlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
class movieTestCase(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testCase",password="123456")
        self.stream = StreamPlatform.objects.create(name="testStream",about="testStream",url='http://www.test.com')
        self.movie = Movie.objects.create(name='testMovie',description="testMovie",moviePlatform=self.stream)
        self.token = Token.objects.get(user__username='testCase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    def test_movieList(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_movieCreate(self):
        data ={
            "name": "testMovie",
            "description": "testMovie",
            'moviePlatform': self.stream
        }
        response = self.client.post(reverse('streamlist'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_movieDetails(self):
        response = self.client.get(reverse('movie_detail',args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().name, 'testMovie')
class reviewTestCase(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testCase",password="123456")
        self.userC= User.objects.create_user(username="testCase2",password="123456")
        self.stream = StreamPlatform.objects.create(name="testStream",about="testStream",url='http://www.test.com')
        self.movie = Movie.objects.create(name='testMovie',description="testMovie",moviePlatform=self.stream)
        self.token = Token.objects.get(user__username='testCase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.movie2 = Movie.objects.create(name='testMovie',description="testMovie",moviePlatform=self.stream)
        self.review= review.objects.create(rate=4,review_comment='testReview',review_movie=self.movie2,review_author=self.user)
    def test_reviewList(self):
        response = self.client.get(reverse('reviewlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_reviewCreate(self):
        data ={
            "rate": 5,
            "review_comment": "testReview1",
            'review_movie': self.movie,
            'review_author':self.userC
        }
        response = self.client.post(reverse('create_review',args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_reviewDetails(self):
        response = self.client.get(reverse('review_detail',args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Movie.objects.count(), 1)
        # self.assertEqual(Movie.objects.get().review_comment, 'testReview')
