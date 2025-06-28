from django.db import models

# Create your models here.

class Parent(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.mobile_number})"

class Child(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age_group = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent} - {self.child}"
