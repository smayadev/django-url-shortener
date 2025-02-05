from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main.models import Paths
from .serializers import PathsSerializer


class ShortenURLApiView(APIView):

    def post(self, request, *args, **kwargs):
        '''
        Take a long URL and shorten it
        '''
        data = {
            'dest_url': request.data.get('dest_url')
        }
        serializer = PathsSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(PathsSerializer(obj).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)