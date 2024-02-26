from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView
from article_module.models import Article


def index(request):
    return render(request, 'admin_panel/home/index.html')


class ArticlesListView(ListView):
    model = Article
    paginate_by = 12
    template_name = 'admin_panel/article/article_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        return query


class ArticleEditView(UpdateView):
    model = Article
    template_name = 'admin_panel/article/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')