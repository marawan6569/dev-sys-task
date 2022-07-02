from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status, renderers, parsers
from rest_framework.authtoken.models import Token

from .validators import Validator
from .models import User
from .serializers import (
    UserSerializer, CreateUserSerializer, AuthTokenSerializer, StatusSerializer, CreateStatusSerializer
)
# Create your views here.


class CreateUserAPI(CreateAPIView):
    """
    Create user
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        errors_dict = {}
        for field in request.data:
            if field == 'csrfmiddlewaretoken' or field == 'password':
                continue

            if field == 'avatar':
                if request.data['avatar'] == '' or request.data['avatar'] is None:
                    s, v = False, {'error': 'blank'}
                else:
                    file_name = request.data['avatar'].name.split('.')[-1]
                    s, v = Validator(field_name=field, value=file_name, model=User)

            else:
                s, v = Validator(field_name=field, value=request.data[field], model=User)

            if not s:
                errors_dict[field] = v

        if errors_dict == {}:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(CreateAPIView):
    """
    login and return a token
    """
    serializer_class = AuthTokenSerializer
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }

        return Response(content)


class CreateStatusAPI(CreateAPIView):
    """
    Create status for user
    """
    serializer_class = CreateStatusSerializer

    def post(self, request, *args, **kwargs):
        user = Token.objects.filter(key=request.data['token']).first()
        if not user:
            return Response({'error': 'Invalid auth-token or phone number'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if user.user.phone_number != request.data['phone_number']:
                return Response({'error': 'Invalid auth-token or phone number'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response({
                "status": StatusSerializer(user, context=self.get_serializer_context()).data,

            }, status=status.HTTP_201_CREATED)
        else:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
