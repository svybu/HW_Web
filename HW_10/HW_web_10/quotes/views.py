from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm
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


def author_detail(request):
    author = Author.objects.filter(id=request.quote.author.id)

    context = {
        'author': author
    }

    return render(request, 'author_detail.html', context)


class AuthorCreateView(View):
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
        return render(request, self.template_name, {'form': form})


author_add = login_required(AuthorCreateView.as_view())
