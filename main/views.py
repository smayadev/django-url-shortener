import random
import string
from urllib.parse import urlparse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.html import format_html
from .models import Paths
from .forms import PathsForm


class IndexView(TemplateView):
    template_name = "main/index.html"
    form_class = PathsForm
    model = Paths

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        src_path = ''
        while True:
            tmp_path = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            check = Paths.objects.filter(src_path=tmp_path)
            if not check:
                src_path = tmp_path
                break
        if form.is_valid():
            obj = form.save(commit=False)
            obj.src_path = src_path
            obj.save()
            short_url = f'{request.scheme}://{request.get_host()}/{src_path}'
            copy_button = format_html(
            '''
            <a href="#" onclick="navigator.clipboard.writeText('{}')" title="Copy to Clipboard">
                <i class="fas fa-copy" style="margin-right: 10px; color: #007bff; cursor: pointer;"></i>
            </a>
            ''',
            short_url
            )
            messages.success(request, f'Success! Your shortened URL is <strong>{short_url}</strong> {copy_button}')
        else:
            messages.error(request, f'Add failed{form.errors}')
        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        data = {
            'message': 'Enter the URL to shorten and click "Go!"',
            'add_form': self.form_class
        }
        return render(request, self.template_name, data)


def redirect_to_dest(request, src_path):
    url_entry = get_object_or_404(Paths, src_path=src_path)
    return redirect(url_entry.dest_url)