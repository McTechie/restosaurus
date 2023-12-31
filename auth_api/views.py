from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer

    def get_queryset(self):
        group = self.request.query_params.get('group')

        if group:
            return User.objects.filter(groups__name=group.lower())
        else:
            return User.objects.all()


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not (username and password):
            return Response({'message': 'Username and password must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if user:
            return Response({'message': f'User {username} already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # cretae user and assign to customer group
        user = User.objects.create_user(username=username, password=password)
        customer_group, created = Group.objects.get_or_create(name='customer')
        customer_group.user_set.add(user)

        return Response({'message': f'User {username} created'}, status=status.HTTP_201_CREATED)


class AddUserToGroup(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        group = request.data.get('group')

        if not (username and group):
            return Response({'message': 'Username and group must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'message': f'User {username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # check if group exists, if not create it
        group, created = Group.objects.get_or_create(name=group.lower())

        # add user to group
        group.user_set.add(user)

        return Response({'message': f'User {username} added to {group.title()} group'}, status=status.HTTP_200_OK)


class AddUserToDeliveryCrew(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response({'message': 'Username must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'message': f'User {username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # check if group exists, if not create it
        group, created = Group.objects.get_or_create(name='delivery crew')

        # add user to group
        group.user_set.add(user)

        return Response({'message': f'User {username} added to {group.title()} group'}, status=status.HTTP_200_OK)


class RemoveUserFromGroup(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        group = request.data.get('group')

        if not (username and group):
            return Response({'message': 'Username and group must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'message': f'User {username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        group = Group.objects.filter(name=group.lower()).first()

        if not group:
            return Response({'message': f'Group {group} not found'}, status=status.HTTP_404_NOT_FOUND)

        # remove user from group
        group.user_set.remove(user)

        return Response({'message': f'User {username} removed from {group.title()} group'}, status=status.HTTP_200_OK)
