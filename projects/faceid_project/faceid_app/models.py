from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LEVEL_CHOICES = [
        ('Массовый', 'Массовый'),
        ('Любительский', 'Любительский'),
        ('Профессиональный', 'Профессиональный'),
    ]
    
    username = models.CharField(max_length=150, unique=True)  # Добавьте unique=True
    email = models.EmailField(unique=True)
    
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='Массовый',
        blank=True,
        verbose_name="Уровень спорта"
    )
    club = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Клуб"
    )
    coach = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Тренер"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="Фотография профиля"
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title