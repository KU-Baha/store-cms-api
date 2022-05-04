from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Сериалайзер пост
    """

    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'image', 'title', 'description', 'create_date', 'update_date')
