from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from main.models import Paths
from .serializers import PathsSerializer


class PathsViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling URL shortening and resolution.
    """
    queryset = Paths.objects.all()
    serializer_class = PathsSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to shorten a URL
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests to resolve a short URL
        """
        obj = self.get_queryset().filter(short_code=pk).first()
        if obj:
            return Response({"dest_url": obj.dest_url}, status=status.HTTP_200_OK)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
