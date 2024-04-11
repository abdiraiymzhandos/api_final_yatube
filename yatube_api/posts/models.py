from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название группы")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание группы")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(verbose_name="Текст публикации")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to='posts/', 
        null=True, 
        blank=True,
        verbose_name="Изображение"
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        related_name='posts', 
        null=True, 
        blank=True, 
        verbose_name="Группа"
    )

    # class Meta:
    #     ordering = ['-pub_date']

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='unique_following')
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"
