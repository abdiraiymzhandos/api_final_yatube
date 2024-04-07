from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

User = get_user_model()

# It's a good practice to call get_user_model rather than directly importing the User model,
# especially if you're using a custom user model.
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
    # Defines the main text content of the post. This field is required.
    text = models.TextField(verbose_name="Текст публикации")

    # Automatically sets the publication date to the current date/time when a post is first created.
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    # Establishes a many-to-one relationship with the User model. Each post is authored by a User.
    # This field is required, as each post must have an author.
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name="Автор"
    )

    # An optional field for uploading an image with the post. It can be left blank or null.
    image = models.ImageField(
        upload_to='posts/', 
        null=True, 
        blank=True,
        verbose_name="Изображение"
    )

    # An optional many-to-one relationship to the Group model. A post can belong to a group, but it's not required.
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        related_name='posts', 
        null=True, 
        blank=True, 
        verbose_name="Группа"
    )

    class Meta:
        # Orders posts in reverse chronological order by default.
        ordering = ['-pub_date']

    def __str__(self):
        # Returns a string representation of the Post. Here, we return the first 30 characters of the post's text.
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='unique_following')
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"



