from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import User, Contact, Spam
from .serializers import UserSerializer, ContactSerializer, SpamSerializer
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import logging

# Configure logging
logger = logging.getLogger(__name__)

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'message': 'Login successful'
        })


class MarkSpamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        logger.debug(f"Received phone_number: {phone_number}")
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        spam, created = Spam.objects.get_or_create(phone_number=phone_number)
        logger.debug(f"Spam object created: {created}, Current count: {spam.count}")

        if not created:
            spam.count += 1
            spam.save()
            logger.debug(f"Updated spam count: {spam.count}")

        return Response({"message": "Number marked as spam"}, status=status.HTTP_200_OK)

# class SearchByNameView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ContactSerializer

#     def get_queryset(self):
#         query = self.request.query_params.get('query', '')
#         return Contact.objects.filter(Q(name__istartswith=query) | Q(name__icontains=query)).distinct()

class SearchByNameView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        print(f"Search query: {query}")
        queryset = Contact.objects.filter(Q(name__istartswith=query) | Q(name__icontains=query)).distinct()
        print(f"Queryset: {queryset}")
        return queryset

class SearchByPhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        contacts = Contact.objects.filter(phone_number=phone_number)
        if contacts:
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No contact found"}, status=status.HTTP_404_NOT_FOUND)



























# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import CreateAPIView, ListAPIView
# from .models import User, Contact, Spam
# from .serializers import UserSerializer, ContactSerializer, SpamSerializer
# from django.db.models import Q
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

# class RegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# # class CustomAuthToken(ObtainAuthToken):
#     # def post(self, request, *args, **kwargs):
#     #     serializer = self.serializer_class(data=request.data,
#     #                                        context={'request': request})
#     #     serializer.is_valid(raise_exception=True)
#     #     user = serializer.validated_data['user']
#     #     token, created = Token.objects.get_or_create(user=user)
#     #     return Response({
#     #         'token': token.key,
#     #         'message': 'Login successful'
#     #     })

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# class MarkSpamView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         phone_number = request.data.get('phone_number')
#         spam, created = Spam.objects.get_or_create(phone_number=phone_number)
#         if not created:
#             spam.count += 1
#             spam.save()
#         return Response({"message": "Number marked as spam"}, status=status.HTTP_200_OK)

# class SearchByNameView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ContactSerializer

#     def get_queryset(self):
#         query = self.request.query_params.get('query', '')
#         return Contact.objects.filter(Q(name__istartswith=query) | Q(name__icontains=query)).distinct()

# class SearchByPhoneNumberView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         phone_number = request.query_params.get('phone_number')
#         contacts = Contact.objects.filter(phone_number=phone_number)
#         if contacts:
#             serializer = ContactSerializer(contacts, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"error": "No contact found"}, status=status.HTTP_404_NOT_FOUND)
