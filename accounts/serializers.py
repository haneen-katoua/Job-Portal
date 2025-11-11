from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_type = instance.user.user_type

        if user_type == 'job_seeker':
            for field in ['company_name', 'company_website', 'logo', 'address']:
                data.pop(field, None)
        elif user_type == 'recruiter':
            for field in ['cv', 'skills', 'experience', 'education', 'linkedin']:
                data.pop(field, None)
        return data