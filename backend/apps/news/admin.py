from django.contrib import admin
from .models import NewsCategory, NewsArticle

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_urgent', 'is_published', 'published_at')
    list_filter = ('is_urgent', 'is_published', 'category')
    search_fields = ('title', 'summary', 'content')
