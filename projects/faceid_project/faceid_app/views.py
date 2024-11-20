from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
import base64
from django.contrib.auth.decorators import user_passes_test
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status, viewsets
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Visit

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

@admin_required
def check_face(request):
    if request.method == "POST":
        try:
            photo_data = request.POST.get("photo")
            format, imgstr = photo_data.split(';base64,')
            uploaded_photo = ContentFile(base64.b64decode(imgstr), name='uploaded.jpg')

            users = User.objects.exclude(profile_picture__isnull=True).exclude(profile_picture__exact='')

            unknown_image = face_recognition.load_image_file(uploaded_photo)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            for user in users:
                if user.profile_picture:
                    known_image = face_recognition.load_image_file(user.profile_picture.path)
                    known_encodings = face_recognition.face_encodings(known_image)

                    for known_encoding in known_encodings:
                        if face_recognition.compare_faces([known_encoding], unknown_encoding)[0]:
                            # Фиксация времени посещения
                            Visit.objects.create(user=user)
                            return JsonResponse({
                                "status": "success",
                                "message": f"{user.first_name} {user.last_name}, FACE ID подтверждено!"
                            })

            return JsonResponse({
                "status": "error",
                "message": "Не удалось найти, попробуйте еще раз."
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Этого человека нет в Базе Данных: {str(e)}"
            })

    return render(request, 'faceid_app/check_face.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('profile')


@admin_required
def visit_log(request):
    visits = Visit.objects.select_related('user').order_by('-timestamp')
    return render(request, 'faceid_app/visit_log.html', {'visits': visits})
