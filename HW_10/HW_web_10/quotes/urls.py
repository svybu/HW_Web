from django.urls import path
from .views import add_author, add_quote, main, author_detail, find_by_tag

app_name = 'quotes'

urlpatterns = [
    path('', main, name='main'),
    path('add_author/', add_author, name='add_author'),
    path('add_quote/', add_quote, name='add_quote'),
    path('author_detail/<int:id>/', author_detail, name='author_detail'),
    path('tag/<int:_id>/', find_by_tag, name='find_by_tag'),

]
