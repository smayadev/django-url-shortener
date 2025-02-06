from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from main.models import Paths
from .serializers import PathsSerializer
from .permissions import HasUserAPIKey, HasAdminAPIKey


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
    permission_classes = [HasUserAPIKey]

    def create(self, request):
        serializer = PathsSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(PathsSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResolveURLViewSet(viewsets.ViewSet):
    """
    Allows users to resolve a short URL.
    """
    permission_classes = [HasUserAPIKey]

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
    permission_classes = [HasAdminAPIKey]

    def get_queryset(self):
        return Paths.objects.all()

    def retrieve(self, request, pk=None):
        """
        Returns placeholder stats for a short URL
        """
        obj = self.get_queryset().filter(short_code=pk).first()

        if obj:

            stats_data = {
                'short_code': obj.short_code,
                'dest_url': obj.dest_url,
                'clicks': 0,
                'unique_visitors': 0,
                'last_visited': None,
            }

            return Response(stats_data, status=status.HTTP_200_OK)
        return Response({'error': '404 Not Found'}, status=status.HTTP_404_NOT_FOUND)
