import random
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from main.models import Paths, Captcha
from .serializers import PathsSerializer
from .permissions import HasAnyAPIKey, HasAdminAPIKey, HasSystemAPIKey
from .models import PathsAPIKey
import clickhouse_connect
from clickhouse_connect.driver.exceptions import OperationalError


class PathsViewSet(viewsets.ModelViewSet):
    """
    Admin-only view to list and manage shortened URLs.
    """
    queryset = Paths.objects.all()
    serializer_class = PathsSerializer
    permission_classes = [HasAdminAPIKey]


class ShortenURLViewSet(viewsets.ViewSet):
    """
    Allows users to shorten URLs
    """
    permission_classes = [HasAnyAPIKey]

    def create(self, request):
        serializer = PathsSerializer(data=request.data)

        api_key = request.headers.get("Authorization", "").replace("Api-Key ", "").strip()
        api_key_obj = PathsAPIKey.objects.filter(prefix=api_key[:8]).first()

        if not api_key_obj:
            return Response({'error': 'Invalid API Key'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            obj = serializer.save(api_key=api_key_obj)
            return Response(PathsSerializer(obj).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResolveURLViewSet(viewsets.ViewSet):
    """
    Allows users to resolve a short URL.
    """
    permission_classes = [HasAnyAPIKey]

    def get_queryset(self):
        return Paths.objects.all()

    def retrieve(self, request, pk=None):
        """
        Handle GET requests to resolve a short URL
        """
        obj = self.get_queryset().filter(short_code=pk).first()
        if obj:
            return Response({"dest_url": obj.dest_url}, status=status.HTTP_200_OK)
        return Response({'error': '404 Not Found'}, status=status.HTTP_404_NOT_FOUND)
    

class StatsViewSet(viewsets.ViewSet):
    """
    Returns analytics for a given short URL.
    """
    permission_classes = [HasAnyAPIKey]

    def get_queryset(self):
        return Paths.objects.all()

    def retrieve(self, request, pk=None):
        """
        Returns stats for a short URL
        """
        api_key = request.headers.get('Authorization', '').replace('Api-Key ', '').strip()
        api_key_prefix = api_key[:8]
        api_key_obj = PathsAPIKey.objects.filter(prefix=api_key_prefix).first()

        obj = self.get_queryset().filter(short_code=pk).first()

        if not api_key_obj:
            return Response({'error': 'Invalid API Key'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not obj:
            return Response({'error': 'Invalid short_code'}, status=status.HTTP_400_BAD_REQUEST)

        # API key must be admin or the user who added the short url being retrieved
        if api_key_obj.is_system or (not api_key_obj.is_admin and obj.api_key.prefix != api_key_prefix):
            return Response(
                {'error': '403 Forbidden'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_HOST,
                interface=settings.CLICKHOUSE_INTERFACE,
                port=settings.CLICKHOUSE_HTTP_PORT, 
                username=settings.CLICKHOUSE_USER, 
                password=settings.CLICKHOUSE_PASSWORD,
                connect_timeout=settings.CLICKHOUSE_HTTP_TIMEOUT,
            )
            parameters = {'short_code': obj.short_code}
            query_result = client.query('SELECT short_code, sumMerge(total_clicks) AS total_clicks, uniqCombinedMerge(unique_visitors) AS unique_visitors, maxMerge(last_visited) AS last_visited FROM url_shortener.clicks_aggregated where short_code = {short_code:String} GROUP BY short_code order by total_clicks desc limit 1', parameters=parameters)

            column_names, rows = query_result.column_names, query_result.result_rows

            if not rows:
                stats_data = {'warning': 'No stats found for this short code'}
            else:
                stats_data = dict(zip(column_names, rows[0]))

            return Response(stats_data, status=status.HTTP_200_OK)
        except OperationalError as e:
            print(f"Clickhouse connection failed: {e}")
            return Response(
                {'error': '500 Internal Server Error: stats backend unavailable'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class CaptchaQuestionViewSet(viewsets.ViewSet):
    """
    Allows a system user to retrieve a random captcha question.
    """
    permission_classes = [HasSystemAPIKey]

    def get_queryset(self):
        return Captcha.objects.all()
    
    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        """
        Check if the provided answer matches the captcha question answer in the db
        """
        obj = self.get_queryset().filter(pk=pk).first()

        try:
            user_answer = str(request.data.get('answer')).lower().strip()
            obj_answer = str(obj.answer).lower().strip()
            if obj_answer == user_answer:
                return Response({'match': True}, status=status.HTTP_200_OK)
            else:
                return Response({'match': False}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': 'Invalid captcha_id'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Handle GET requests to retrieve a random captcha question
        """
        try:
            field_names = [field.name for field in Captcha._meta.fields]

            queryset = Captcha.objects.values_list('id', 'question', 'answer')

            results = {
                row[0]: {field: row[i] for i, field in enumerate(field_names) if field != "id"}
                for row in queryset
            }
            challenge = random.choice(list(results.keys()))

            return Response(
                {'captcha_id': challenge, 'question': results[challenge]['question']}, 
                status=status.HTTP_200_OK
            )
        except:
            print("Error retrieving captcha question")
            return Response(
                {'error': '404 Not Found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
