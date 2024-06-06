from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        return Response(status=status.HTTP_401_UNAUTHORIZED)



from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '').lower()
        if '@' in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(username__icontains=keyword)




from rest_framework import permissions
from .models import FriendRequest
from .serializers import FriendRequestSerializer, FriendRequestActionSerializer

class FriendRequestView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user, status='pending')

class FriendRequestActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FriendRequestActionSerializer(data=request.data)
        if serializer.is_valid():
            request_id = serializer.validated_data['request_id']
            action = serializer.validated_data['action']
            try:
                friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
                if action == 'accept':
                    friend_request.status = 'accepted'
                elif action == 'reject':
                    friend_request.status = 'rejected'
                friend_request.save()
                return Response(status=status.HTTP_200_OK)
            except FriendRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(
            received_requests__from_user=self.request.user,
            received_requests__status='accepted'
        ) | User.objects.filter(
            sent_requests__to_user=self.request.user,
            sent_requests__status='accepted'
        )

class PendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')


from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'

class FriendRequestView(generics.ListCreateAPIView):
    ...
    throttle_classes = [FriendRequestThrottle]
    ...
