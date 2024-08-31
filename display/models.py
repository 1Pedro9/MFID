from django.db import models

class Member(models.Model):
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    fullname = models.CharField(max_length=100, default="")
    lastname = models.CharField(max_length=100, default="")
    idNr = models.CharField(max_length=13, default="")
    initials = models.CharField(max_length=10, default="")
    title = models.CharField(max_length=10, default="")
    cellNr = models.CharField(max_length=12, default="")
    occupation = models.CharField(max_length=100, default="")
    current_employer = models.CharField(max_length=100, default="")
    joined = models.DateTimeField(auto_now_add=True)
    
class Condition(models.Model):
    condition = models.CharField(max_length=100)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)

class Medication(models.Model):
    medication = models.CharField(max_length=100)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)

class Allergy(models.Model):
    allergie = models.CharField(max_length=100)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)

class Aid(models.Model):
    aid_name = models.CharField(max_length=100)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)

class Dependent(models.Model):
    initials = models.CharField(max_length=5, default="")
    lastname = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    aid = models.ForeignKey(Aid, on_delete=models.CASCADE)
    dependent_code = models.IntegerField(null=True, blank=True)
    is_main = models.BooleanField(default=False)
