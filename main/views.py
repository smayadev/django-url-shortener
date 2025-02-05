import random
import string
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.html import format_html
import redis
from .models import Paths
from .forms import PathsForm


class IndexView(TemplateView):
    template_name = "main/index.html"
    form_class = PathsForm
    model = Paths

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            site_url = settings.SITE_URL
            short_url = f'{site_url}/{obj.short_code}'
            copy_button = format_html(
            '''
            <a href="#" onclick="navigator.clipboard.writeText('{}')" title="Copy URL to Clipboard">
                <i class="fa-regular fa-clipboard" style="margin-right: 10px; color: #007bff; cursor: pointer;"></i>
            </a>
            ''',
            short_url
            )
            messages.success(request, f'Your shortened URL is <strong>{short_url}</strong> {copy_button}')
        else:
            messages.error(request, form.errors.get('dest_url', [''])[0])
        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        data = {
            'message': 'Enter the URL to shorten and click "Go!"',
            'add_form': self.form_class
        }
        return render(request, self.template_name, data)


redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'], decode_responses=True)

def redirect_to_dest(request, short_code):

    short_url = get_object_or_404(Paths, short_code=short_code)

    try:
        cache_key = f'url:{short_code}'

        cached_url = redis_client.get(cache_key)

        if cached_url:
            return redirect(cached_url)
        
        redis_client.setex(cache_key, 3600, short_url.dest_url)
    except (redis.ConnectionError, redis.TimeoutError):
        print('redis connection failed when redirecting URL')

    return redirect(short_url.dest_url)