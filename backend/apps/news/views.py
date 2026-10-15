from rest_framework import viewsets, permissions, filters
from .models import NewsCategory, NewsArticle
from .serializers import NewsCategorySerializer, NewsArticleSerializer

class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.AllowAny]

class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.filter(is_published=True).select_related('category')
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'summary', 'content']
