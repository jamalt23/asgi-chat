from django.db import models
from accounts.models import User

class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': { 'username': self.author.username, 'pfp': self.author.pfp },
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
        }

    def __str__(self):
        return f'{self.author.username}: {self.text}'

    @classmethod
    def clear_messages(cls):
        cls.objects.all().delete()

    class Meta:
        ordering = ['timestamp']