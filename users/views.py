
from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserSerializer
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class SignUpView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if CustomUser.objects.filter(email=request.data.get('email')).exists():
            return Response({"email": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class UpdateUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
