import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def main(request):
    return render(request, 'quotes/base.html', context={'title': 'Quotes'})
