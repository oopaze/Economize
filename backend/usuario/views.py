from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import response, status

from tabelas.models import Usuario
from .serializers import UsuarioSerializer, UsuarioReadSerializer

class UserListView(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioReadSerializer
    permission_classes = [IsAdminUser]
    paginate_by = 10


class UserDeleteView(DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminUser]
    
    def delete(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        serializer = self.serializer_class(user)
        data = serializer.data
        data.pop('password', None)
        
        super().delete(request, *args, **kwargs)
        return response.Response(data, status=status.HTTP_202_ACCEPTED)


class UserCreateView(CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        data = serializer.data
        data.pop('password', None)

        user = Usuario.objects.create(
            **data
        )
        user.set_password(serializer.data.get('password', None))
        user.save()

    def post(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        serializer = self.serializer_class(user)
        data = serializer.data
        data.pop('password', None)
        
        super().post(request, *args, **kwargs)
        return response.Response(data, status=status.HTTP_201_CREATED)


class UserPasswordChangeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user
    
    def put(self, *args, **kwargs):
        usuario = self.get_object()
        password = self.request.data.get('password', None)
        if password is not None:
            usuario.set_password(password)
            usuario.save()      
            return response.Response ({
                    'message': 'Password updated successfully',
                    'data': []
                })  

        return response.Response({
            'error': 'Somente o atributo "password" pode ser editado.',
        }, status.HTTP_406_NOT_ACCEPTABLE)