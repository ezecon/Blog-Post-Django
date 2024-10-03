from rest_framework import serializers
from .models import BlogPost  # Adjust this based on your models

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
