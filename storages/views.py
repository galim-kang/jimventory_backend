from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Storage, Menu
from .serializers import StorageSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class StorageCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hostUser=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateStorageView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            storage = Storage.objects.get(pk=pk, hostUser=request.user)
        except Storage.DoesNotExist:
            return Response({'message': 'Storage not found or not authorized to update'}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = StorageSerializer(storage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
