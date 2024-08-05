from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=1000, blank=True)
    profile_pic = models.ImageField(upload_to='images', null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_with')

    def add_friend(self, friend):
        self.friends.add(friend)
        friend.friends.add(self)

    def remove_friend(self, friend):
        self.friends.remove(friend)
        friend.friends.remove(self)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def accept(self):
        self.from_user.add_friend(self.to_user)
        self.delete()

    def reject(self):
        self.delete()

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"from {self.from_user} to {self.to_user}"
