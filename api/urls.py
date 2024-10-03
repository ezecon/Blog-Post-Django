from django.urls import path
from .views import *

urlpatterns = [
     path("blogposts/", BlogPostListCreate.as_view(),name="blogpost-view-create"),
     path("blogposts/<int:pk>/", BlogPostListView.as_view(),name="update")
]
