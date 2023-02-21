from iha.models import IHA, IHACategory
from iha.api.serializers import IHASerializer, IHACategorySerializer
from iha.filters import IHAFilter

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class IHAListCreateAPIView(APIView):
    def get(self, request):
        ihas = IHA.objects.all().order_by("-date_of_update")
        ihas = IHAFilter(request.GET, queryset=ihas).qs

        check_active_status = self.request.query_params.get('status',None)
        if check_active_status is not None:
            ihas = ihas.filter(status=check_active_status)

        serializer = IHASerializer(ihas, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IHADetailAPIView(APIView):

    def get_object(self, pk):
        iha_instance = get_object_or_404(IHA, pk=pk)
        return iha_instance

    def get(self, request, pk):
        iha = self.get_object(pk=pk)
        serializer = IHASerializer(iha)
        return Response(serializer.data)

    def put(self, request, pk):
        iha = self.get_object(pk=pk)
        serializer = IHASerializer(iha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        iha = self.get_object(pk=pk)
        iha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IHACategoryListCreateAPIView(APIView):

    def get(self, request):
        categories = IHACategory.objects.all()
        serializer = IHACategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = IHACategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







