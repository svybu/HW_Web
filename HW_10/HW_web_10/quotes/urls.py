from django.urls import path
from .views import AuthorCreateView, main, author_detail, find_by_tag

app_name = 'quotes'

urlpatterns = [
    path('', main, name='main'),
    path('authors_add/', AuthorCreateView.as_view(), name='author_add'),
    path('author_detail/<int:id>/', author_detail, name='author_detail'),
    path('tag/<int:_id>/', find_by_tag, name='find_by_tag'),

]
