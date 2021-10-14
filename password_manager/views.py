from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError, PermissionDenied
from .serializers import UserSerializer, PasswordSerializer, SharedPasswordsSerializer
from .models import UserPasswords, SharedPasswordsDetails

class UserRegister(generics.GenericAPIView, mixins.CreateModelMixin):
	serializer_class = UserSerializer
	permission_classes = []

	def post(self, request):
		return self.create(request)

class ManagePasswordsViewset(viewsets.ModelViewSet):
	serializer_class = PasswordSerializer
	queryset = UserPasswords.objects.all()
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
 		if self.request.user.is_superuser:
 			return UserPasswords.objects.all()
 		return UserPasswords.objects.filter(uid=self.request.user)

	def perform_create(self, serializer):
		serializer.save(uid = self.request.user)

class SharePasswords(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
	serializer_class = SharedPasswordsSerializer
	permission_classes = [IsAuthenticated]
	
	lookup_field = 'id'

	def get_queryset(self):
 		if self.request.user.is_superuser:
 			return SharedPasswordsDetails.objects.all()
 		return SharedPasswordsDetails.objects.filter(uid=self.request.user)

	def get(self, request, id=None):
		print('get worked', id)
		if id:
			return self.retrieve(request, id)
		else:
			return self.list(request)
	def post(self, request):
		return self.create(request)

	def perform_create(self, serializer):
		request = self.request
		data = request.data
		print(request.data)

		if request.user.pk == data['shared_with_uid']:
			raise ValidationError('You can\'t share with yourself.')
		serializer.save(uid=self.request.user)

	def put(self, request, id=None):
		return self.update(request,id)


class PasswordsSharedWithMe(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
	serializer_class = SharedPasswordsSerializer
	permission_classes = [IsAuthenticated]

	lookup_field = 'id'

	def get_queryset(self):
		print(self.request.data)
		if self.request.user.is_superuser:
				return SharedPasswordsDetails.objects.all()
		return SharedPasswordsDetails.objects.filter(shared_with_uid=self.request.user, view_perm=True)

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)

	def put(self, request, id=None):
		data = SharedPasswordsDetails.objects.filter(pk=id, edit_perm=True).count()
		if data:
			return self.update(request,id)
		else:
			raise PermissionDenied
			# raise ValidationError('Permission Denied.')
