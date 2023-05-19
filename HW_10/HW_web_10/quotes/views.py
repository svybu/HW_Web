from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag


def main(request):
    quotes = Quote.objects.all()
    authors = Author.objects.all()
    tags = Tag.objects.all()
    context = {
        'quotes': quotes,
        'authors': authors,
        'tags': tags
    }
    return render(request, 'quotes/base.html', context)


def author_detail(request, id):
    author = Author.objects.get(pk=id)
    context = {
        'author': author
    }

    return render(request, 'quotes/author_detail.html', context)


def find_by_tag(request, _id):
    per_page = 5
    if isinstance(_id, int):
        quotes = Quote.objects.filter(tags=_id).all()
    elif isinstance(_id, str):
        _id = Tag.objects.filter(name=_id).first()
        quotes = Quote.objects.filter(tags=_id.id).all()
    context = {'quotes': quotes}
    return render(request, 'quotes/base.html', context)


"""class AuthorCreateView(View):
    form_class = AuthorForm
    template_name = 'quotes/author_add.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect('author_detail', pk=author.pk)
        return render(request, self.template_name, {'form': form})"""


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quotes/base.html', )
    else:
        form = AuthorForm()
    return render(request, 'quotes/author_add.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quotes/base.html')

    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})
