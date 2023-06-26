from django.shortcuts import render
from .filters import PostFilter

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy, reverse
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_search'
    paginate_by = 10  # вот так мы можем указать количество записей на странице
    
       # Переопределяем функцию получения списка товаров
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context
    
class PostDetail(DetailView):
        # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'     
    
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)
    
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)
    
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

# Представление удаляющее товар.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')    

