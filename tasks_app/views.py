from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from rest_framework import status

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def test_view(request):
    return Response({"message": "You are connected to the server"})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def _update_existing_task(task, data):
    print(f"""
Before update:
Task title: {task.title}
Task description: {task.description}
Task completed: {task.completed}
Task labels: {[label.name for label in task.labels.all()]}""")
    print(f"New data received: {data}")
    
    serializer = TaskSerializer(task, data=data)
    if serializer.is_valid():
        serializer.save()
        
        print(f"""
After update:
Task title: {task.title}
Task description: {task.description}
Task completed: {task.completed}
Task labels: {[label.name for label in task.labels.all()]}""")
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    # Check if task with same title exists for this user
    existing_task = Task.objects.filter(title=request.data.get('title'), owner=request.user).first()
    
    if existing_task:
        # If task exists, update it using the separate method
        return _update_existing_task(existing_task, request.data)
    
    # If no existing task, create new one
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_label(request):
    serializer = LabelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request):
    task_name = request.data.get('title')
    
    if not task_name:
        return Response({'error': 'Task title is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(title=task_name, owner=request.user)
        task.delete()
        return Response({'message': f'Task "{task_name}" deleted successfully'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_label(request):
    label_name = request.data.get('name')
    
    if not label_name:
        return Response({'error': 'Label name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        label = Label.objects.get(name=label_name, owner=request.user)
        label.delete()
        return Response({'message': f'Label "{label_name}" deleted successfully'}, status=status.HTTP_200_OK)
    except Label.DoesNotExist:
        return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)
