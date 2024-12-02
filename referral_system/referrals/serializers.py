from rest_framework import serializers
from .models import UserProfile, VerificationCodes

class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = ['id', 'username', 'phone_number', 'invited_code', 'invited_by']
        
class VerificationCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCodes
        fields = "__all__"