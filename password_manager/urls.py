from django.urls import path, include

from .views import UserRegister, ManagePasswordsViewset, SharePasswords, PasswordsSharedWithMe
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('passwords', ManagePasswordsViewset, basename='passwords')

urlpatterns = [
	path('signup', UserRegister.as_view()),
	path('', include(router.urls)),
	path('share-password', SharePasswords.as_view()),
	# path('shared-password-me', PasswordsSharedWithMe.as_view()),
	path('shared-password-me/', PasswordsSharedWithMe.as_view()),
	path('shared-password-me/<int:id>', PasswordsSharedWithMe.as_view()),
]
