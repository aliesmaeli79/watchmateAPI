from django.urls import path, include
from watchlist_app.api import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS,
                basename='streamplatform')

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='Watch-list'),
    path('<int:pk>/', views.WatchDetailsAV.as_view(), name='Watch-details'),


    path('', include(router.urls)),



    # path('stream/', views.StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>', views.StreamDetailsAV.as_view(),
    #      name='streamplatform-detail'),

    # path('review/', views.ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),



    path('<int:pk>/review-create',
         views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/',
         views.ReviewDetail.as_view(), name='review-detail')
]
