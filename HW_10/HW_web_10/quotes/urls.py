from django.urls import path
from .views import AuthorCreateView, main, author_detail

app_name = 'quotes'

urlpatterns = [
    path('', main, name='main'),
    path('authors_add/', AuthorCreateView.as_view(), name='author_add'),
    path('author_detail/', author_detail, name='author_detail'),

]
