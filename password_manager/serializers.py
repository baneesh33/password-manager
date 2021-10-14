from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import UserPasswords,SharedPasswordsDetails
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

        
		user.set_password(validated_data['password'])
		user.save()

		return user


class PasswordSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserPasswords
		fields = ['id', 'password', 'category']

class SharedPasswordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = SharedPasswordsDetails
		# fields = '__all__'
		fields = ['id', 'shared_with_uid', 'password', 'view_perm', 'edit_perm']
		depth = 1
		# read_only = ['password']
