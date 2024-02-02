from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from jalali_date import datetime2jalali, date2jalali
from article_module.models import Article, ArticleComment


class ArticlesListView(ListView):
    model = Article
    paginate_by = 5
    template_name = 'article_module/articel_module.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        # context['date'] = datetime2jalali(self.request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        # print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
            'comment_count': ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/comment_patial.html', context)

    return HttpResponse('Response')