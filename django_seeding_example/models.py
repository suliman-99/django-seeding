from django.db import models


class M1(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class M2(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class M3(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class M4(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class M5(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)


class M6(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class M7(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Post(models.Model):
    content = models.TextField()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()


class Parent1(models.Model):
    name = models.TextField()


class Child1(models.Model):
    parent = models.ForeignKey(Parent1, on_delete=models.CASCADE)
    name = models.TextField()
