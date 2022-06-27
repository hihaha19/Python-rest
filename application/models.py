from django.db import models

class Post (models.Model):
    userID = models.IntegerField()
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)

    def __str__(self):
       return str(self.userID) + ' ' + self.title + ' ' + self.body


