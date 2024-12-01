from datetime import datetime, timedelta, timezone
import random
import time
import jwt
import logging
from django.shortcuts import render
import string
import zoneinfo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from referral_system import settings

from .models import UserProfile, VerificationCodes
from .serializers import UserSerializer, VerificationCodesSerializer
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # отображает ваш HTML файл


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def generate_code():
    symbols = string.ascii_letters + string.digits
    
    return ''.join(random.choice(symbols) for _ in range(6))

@api_view(['Post'])
def send_code(request):
    """Отправляет код по номеру телефона"""
    phone_number = request.data['phone_number']
    if not phone_number:
        logger.warning("Phone number is missing")
        return Response({"detail": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    ver_code = ''.join(random.choice('1234567890') for _ in range(4))
    
    try:
        ver_code_obj = VerificationCodes.objects.get(phone=phone_number)
        logger.info(f"Phone {phone_number} is registered.")
    except:
        ver_code_obj= VerificationCodes.objects.create(phone=phone_number, created_at=datetime.now(zoneinfo.ZoneInfo("Europe/Moscow")))
        logger.info(f"New phone {phone_number} in system.")
    serializer = VerificationCodesSerializer(ver_code_obj, data={'phone':phone_number, 'code':ver_code, 'created_at':datetime.now(zoneinfo.ZoneInfo("Europe/Moscow"))})
    
    if serializer.is_valid():
        logger.debug(f"Serialized verification data: {serializer.validated_data}")
        serializer.save()
    else:
        logger.error(f"Verification code serialization failed for phone {phone_number}: {serializer.errors}")

    
    time.sleep(2)
    logger.info(f"Code sent to {phone_number}")
    return Response({'message': 'Code sent', 'code':ver_code}, status=status.HTTP_200_OK)

@api_view(['Post'])
def check_code(request):
    """Проверяет код, отправленный на номер телефона"""
    phone_number = request.data.get('phone_number')
    code = request.data.get('verification_code')
    
    try:
        ver_code_obj = VerificationCodes.objects.get(phone=phone_number)
        logger.info(f"Verification code obj for phone {phone_number} found.")
        try:
            if datetime.now(zoneinfo.ZoneInfo("Europe/Moscow")) - ver_code_obj.created_at > timedelta(minutes=30):
                logger.warning(f"Code for phone {phone_number} expired.")
                return Response({'error': 'Code are required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
        
        if code != ver_code_obj.code:
            logger.warning(f"Invalid code entered for phone {phone_number}.")
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"Code for phone {phone_number} validated successfully.")
        client_code = generate_code()
        
        user, _= UserProfile.objects.get_or_create(username=phone_number, phone_number=phone_number)
        logger.debug(f"Generated client code: {client_code}")

        serializer = UserSerializer(user, data={'username':phone_number,'phone_number':phone_number, 'invited_code':client_code})
        
        try:
            if serializer.is_valid():
                logger.info(f"User {phone_number} data serialized successfully.")
                serializer.save()
            else:
                logger.error(f"User serialization failed for phone {phone_number}: {serializer.errors}")

        except Exception as e:
            print(e)
        refresh = RefreshToken.for_user(user)
        
        response = Response({
            'code': client_code,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        
        response.set_cookie('Authorization',f'Bearer {refresh}')
        logger.info(f"Token generated for phone {phone_number}.")
        return response
        
    except:
        logger.error(f"Verification code for phone {phone_number} does not exist.")
        return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def post_invited_code(request):
    """Добавление кода приглашения"""
    if 'Authorization' not in request.COOKIES:
        logger.warning("Authentication credentials were not provided.")
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    invited_code = request.data.get('invited_code')
    
    try:
        invited_by_user = UserProfile.objects.get(invited_code=invited_code)
        logger.info(f"Invited by user found: {invited_by_user.id}")
    except:
        logger.error(f"Invalid invited code: {invited_code}")
        return Response({"error": "Invalid invited code"}, status=status.HTTP_400_BAD_REQUEST) 
    
    
    try:
        payload = jwt.decode(request.COOKIES['Authorization'][7:], settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired.")
        return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.DecodeError:
        logger.error("Invalid token.")
        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    if not user_id:
        return Response({"error": "User ID not found in token."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = UserProfile.objects.get(id=user_id)
        logger.info(f"User found: {user.id}")
    except UserProfile.DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
        return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.invited_by:
        invited_user = UserProfile.objects.get(id=user.invited_by.id)
        logger.info(f"User {user.id} was invited by {user.invited_by.id}")
        return Response({'invited_by': user.invited_by.id, "invited_code":invited_user.invited_code}, status=status.HTTP_200_OK)
        
    serializer = UserSerializer(user, data={"invited_by":invited_by_user.id}, partial=True)
    
    if serializer.is_valid():
        logger.info(f"User {user.id} updated with invited_by: {invited_by_user.id}.")
        serializer.save()
    

    return Response({'invited_by': invited_by_user.id, "invited_code":invited_code}, status=status.HTTP_200_OK)

@api_view(['GET'])
def who_was_invited(request):
    """Просмотр приглашенных пользователей"""
    try:
        payload = jwt.decode(request.COOKIES['Authorization'][7:], settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired.")
        return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.DecodeError:
        logger.error("Invalid token.")
        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    if not user_id:
        logger.error("User ID not found in token.")
        return Response({"error": "User ID not found in token."}, status=status.HTTP_400_BAD_REQUEST)
    
    logger.info(f"Fetching users invited by user {user_id}.")
    users = UserProfile.objects.filter(invited_by=user_id)
    
    # users = UserProfile.objects.all()
    serializer = UserSerializer(users, many=True)
    logger.info(f"Found {len(users)} users invited by {user_id}.")
    return Response({'users': serializer.data}, status=status.HTTP_200_OK)

                
                