from django.db import models
from django.utils.translation import gettext_lazy as _

class AbstractNewsCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Назва категорії'))
    slug = models.SlugField(unique=True, verbose_name=_('URL-ідентифікатор (slug)'))

    class Meta:
        abstract = True
        verbose_name = _('Категорія новин')
        verbose_name_plural = _('Категорії новин')

    def __str__(self):
        return self.name


class NewsCategory(AbstractNewsCategory):
    class Meta(AbstractNewsCategory.Meta):
        abstract = False


class AbstractNewsArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Заголовок новини'))
    summary = models.TextField(blank=True, verbose_name=_('Короткий анонс'))
    content = models.TextField(verbose_name=_('Повний текст новини'))
    image = models.ImageField(upload_to='news/%Y/%m/', blank=True, null=True, verbose_name=_('Головне зображення'))
    is_urgent = models.BooleanField(
        default=False,
        verbose_name=_('Важливе / термінове оголошення (виділяється вгорі сайту)')
    )
    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата та час оприлюднення'))
    is_published = models.BooleanField(default=True, verbose_name=_('Опубліковано'))

    class Meta:
        abstract = True
        verbose_name = _('Новина / Оголошення')
        verbose_name_plural = _('Новини та оголошення')
        ordering = ['-is_urgent', '-published_at']

    def __str__(self):
        return self.title


class NewsArticle(AbstractNewsArticle):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name=_('Категорія')
    )

    class Meta(AbstractNewsArticle.Meta):
        abstract = False
