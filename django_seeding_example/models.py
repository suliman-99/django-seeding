from django.db import models
from django.db.models import UniqueConstraint


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


class Father(models.Model):
    name = models.TextField()


class Son(models.Model):
    name = models.TextField()
    father = models.ForeignKey(Father, on_delete=models.CASCADE)


class Mother(models.Model):
    name = models.TextField()


class Daughter(models.Model):
    name = models.TextField()
    father = models.ForeignKey(Father, on_delete=models.CASCADE)
    mother = models.ForeignKey(Mother, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint (
                fields=['name', 'father', 'mother'],
                name='unique_parentage'
            )]


class Grandson(models.Model):
    name = models.TextField()
    parentage = models.ForeignKey(Daughter, on_delete=models.CASCADE)
