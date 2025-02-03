import random
import string
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
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
            messages.success(request, 'Added')
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