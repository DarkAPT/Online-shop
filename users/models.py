from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True, verbose_name='Аватарка')

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем объект, чтобы получить путь к изображению

        if self.image:
            # Открываем изображение
            img = Image.open(self.image.path)

            # Задаем желаемые размеры
            target_size = (300, 300)

            # Сохраняем соотношение сторон
            img.thumbnail(target_size, Image.LANCZOS)
            img.save(self.image.path)
