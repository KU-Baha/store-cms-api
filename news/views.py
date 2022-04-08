from rest_framework import viewsets
from .serializers import (
    PostSerializer,
)
from .models import (
    Post
)


class PostViewSet(viewsets.ModelViewSet):
    """
    Пост
    Реализованы все базовые методы ModelViewSet
    """
    serializer_class = PostSerializer
    queryset = Post.objects.filter(deleted=False)