from rest_framework import serializers

from .models import Article
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import UserProfile


class ArticleSerializers(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            'required': 'article title cannot be empty',
            'max_length': 'article title cannot exceed 500 characters'
        }
    )
    description = serializers.CharField(
        required=False,
        max_length=1000,
        error_messages={
            'max_length': 'description cannot exceed 1000 characters'
        }
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'article body cannot be empty'
        }
    )

    author = serializers.SerializerMethodField(read_only=True)

    def get_author(self, obj):
        """Get the profile of the author of the article"""
        serializer = ProfileSerializer(
            instance=UserProfile.objects.get(user=obj.author))
        return serializer.data

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'created_at', 'updated_at',
                  'author')