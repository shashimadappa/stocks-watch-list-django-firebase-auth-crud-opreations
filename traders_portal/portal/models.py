# models.py

from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Company(models.Model):
    company_name = models.CharField(max_length=100, blank=False)
    symbol = models.CharField(max_length=30, blank=False)
    scripcode = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.company_name

class WatchList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.company.company_name}"
