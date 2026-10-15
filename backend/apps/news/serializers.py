from rest_framework import serializers
from .models import NewsCategory, NewsArticle

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug']

class NewsArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'category', 'category_name', 'title', 'summary', 'content', 'image', 'is_urgent', 'published_at']
