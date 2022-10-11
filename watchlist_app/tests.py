from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='password')               # create user
        self.token = Token.objects.get(
            user__username=self.user)          # get token
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)  # login

        self.stream = models.StreamPlatform.objects.create(                   # manually create platform
            name="Netflix", about="#1 Streaming Platform", website="https://Netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://Netflix.com"
        }
        respoonse = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        respoonse = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        respoonse = self.client.get(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    def test_streamplatform_put(self):  # for update
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform - updated",
            "website": "https://Netflix.com"
        }
        respoonse = self.client.put(
            reverse('streamplatform-detail', args=(self.stream.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete(self):  # for delete
        respoonse = self.client.delete(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='password')               # create user
        self.token = Token.objects.get(
            user__username=self.user)          # get token
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)  # login

        self.stream = models.StreamPlatform.objects.create(                   # manually create platform
            name="Netflix", about="#1 Streaming Platform", website="https://Netflix.com")

        self.watchlist = models.WatchList.objects.create(title="Example Movie", storyline="Example Story",
                                                         active=True, platform=self.stream)

    def test_watchList_create(self):           # for create watchlist
        data = {
            "title": "Example Movie",
            "storyline": "Example Story",
            "platform": self.stream,
            "active": True,
        }
        respoonse = self.client.post(reverse('Watch-list'), data)
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchList_list(self):                   # for get list weatchlist
        respoonse = self.client.get(
            reverse('Watch-list'))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    # for get only movie individual

    def test_watchList_ind(self):
        respoonse = self.client.get(
            reverse('Watch-details', args=(self.watchlist.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title,
                         'Example Movie')   # match title movie

        self.assertEqual(models.WatchList.objects.count(),
                         1)     # match count movie

    def test_watchList_update(self):                  # for update test
        data = {
            "title": "Example Movie - updated!",
            "storyline": "Example Story updated!",
            "platform": self.stream,
            "active": True,
        }
        respoonse = self.client.put(
            reverse('Watch-details', args=(self.watchlist.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchList_delete(self):              # for delete tests
        respoonse = self.client.delete(
            reverse('Watch-details', args=(self.watchlist.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='password')               # create user
        self.token = Token.objects.get(
            user__username=self.user)          # get token
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)  # login

        self.stream = models.StreamPlatform.objects.create(                   # manually create platform
            name="Netflix", about="#1 Streaming Platform", website="https://Netflix.com")

        self.watchlist = models.WatchList.objects.create(title="Example Movie", storyline="Example Story",
                                                         active=True, platform=self.stream)

        self.watchlist2 = models.WatchList.objects.create(title="Example Movie 2", storyline="Example Story2",
                                                          active=True, platform=self.stream)

        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="good movie",
                                                   watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "good movie",
            "watchlist": self.watchlist,
            "active": True,
        }
        respoonse = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(models.Review.objects.get().rating, 5)
        self.assertEqual(models.Review.objects.count(), 2)

        respoonse = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "good movie",
            "watchlist": self.watchlist,
            "active": True,
        }
        self.client.force_authenticate(user=None)   # no login
        respoonse = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "good movie - updated !",
            "watchlist": self.watchlist,
            "active": False,
        }
        respoonse = self.client.put(
            reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        respoonse = self.client.get(
            reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        respoonse = self.client.get(
            reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(respoonse.status_code, status.HTTP_200_OK)

    # def test_review_delete(self):
    #     respoonse = self.client.delete(
    #         reverse('review-detail', args=(self.review.id,)))
    #     self.assertEqual(respoonse.status_code, status.HTTP_200_OK)
