from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils.html import format_html
from kombu.exceptions import OperationalError
import redis
import random
from .models import Paths, Captcha
from .forms import PathsForm
from .tasks import send_click_to_rabbitmq

def get_captcha(request):
    """
    Generate a random captcha challenge from Captcha
    and return it in a JsonResponse
    """
    field_names = [field.name for field in Captcha._meta.fields]

    queryset = Captcha.objects.values_list('id', 'question', 'answer')

    results = {
        row[0]: {field: row[i] for i, field in enumerate(field_names) if field != "id"}
        for row in queryset
    }
    challenge = random.choice(list(results.keys()))

    return JsonResponse({
        'captcha_id': challenge,
        'question': results[challenge]['question']
    })



class IndexView(TemplateView):
    template_name = "main/index.html"
    form_class = PathsForm
    model = Paths

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        captcha_id = request.POST.get('captcha-challenge-id')
        captcha_response = request.POST.get('captcha-response', '').strip().lower()

        if not captcha_id.isdigit():
            messages.error(request, 'Anti-spam verification failed, invalid id')
            return HttpResponseRedirect(self.request.path_info)

        captcha = Captcha.objects.filter(pk=int(captcha_id)).first()

        if not captcha or captcha_response != captcha.answer:
            messages.error(request, 'Anti-spam verification failed, invalid answer')
            return HttpResponseRedirect(self.request.path_info)

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

def get_client_ip(request):
    """
    Extracts the client IP address from the request headers
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]  # Get the first IP in the list
    return request.META.get("REMOTE_ADDR")

def redirect_to_dest(request, short_code):
    short_url = get_object_or_404(Paths, short_code=short_code)
    cached_url = None

    try:
        cache_key = f'url:{short_code}'
        cached_url = redis_client.get(cache_key)

        if cached_url:
            print('Cache hit!')
        else:
            print('Cache miss!')
            redis_client.setex(cache_key, 3600, short_url.dest_url)

    except (redis.ConnectionError, redis.TimeoutError):
        print('Redis connection failed when redirecting URL')

    user_ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    referrer = request.META.get("HTTP_REFERER", "")

    try:
        print(f'Dispatching click tracking to rabbitmq for {short_code}')
        send_click_to_rabbitmq.delay(short_code, user_ip, user_agent, referrer)
    except OperationalError as e:
        print(f"OperationalError: Failed to send click to rabbitmq: {e}")
    except Exception as e:
        print(f"Exception: Failed to send click to rabbitmq: {e}")

    if cached_url:
        return redirect(cached_url)
    
    return redirect(short_url.dest_url)
