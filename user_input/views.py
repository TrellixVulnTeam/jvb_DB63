from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication 

from .serializers import UserDailyInputSerializer

from .models import UserDailyInput

# https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
class CsrfExemptSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return

class UserDailyInputView(generics.ListCreateAPIView):
	authentication_classes = (CsrfExemptSessionAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = UserDailyInput.objects.all()
	serializer_class = UserDailyInputSerializer