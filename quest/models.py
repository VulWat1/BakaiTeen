from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField("Роли", max_length=10, choices=ROLE_CHOICES, default='parent')

    # если это ребенок – указываем его родителя
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # Монеты ребёнка
    money = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Task(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    reward = models.PositiveIntegerField(default=0)  # монеты награды

    is_completed = models.BooleanField(default=False)        # ребёнок отметил "выполнено"
    is_confirmed = models.BooleanField(default=False)        # родитель подтвердил

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.child.username}"
    
    class Meta: 
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

class ExchangeRequest(models.Model):
    child = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # монеты, которые хочет вывести
    
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запрос {self.child.username}: {self.amount} монет"

    class Meta: 
        verbose_name = "Вывод"
        verbose_name_plural = "Выводы"
