from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import BlogPost
from .serializers import BlogPostSerializer
# Create your views here.

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class= BlogPostSerializer

    def delete (self, request, *arg, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class= BlogPostSerializer
    lookup_field = "pk"

