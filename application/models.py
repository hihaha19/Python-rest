from django.db import models


class User (models.Model):
    userID = models.IntegerField()
    name = models.CharField(max_length=60)


class Post (models.Model):
    userID = models.IntegerField()
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)

    def __str__(self):
       return str(self.userID) + ' ' + self.title + ' ' + self.body


class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' ' + self.description


