from django.db import models
from django.utils import timezone

class Patient(models.Model):
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=50,null=True)
    
    class Meta:
        db_table = 'patient_table'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Counselor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,null=True)
    specialization = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = 'counselor_table'
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.specialization}"
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_icon = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
class Session(models.Model):
    fullname = models.CharField(max_length=250,blank=True)
    email = models.EmailField(max_length=250)
    phonenumber = models.CharField(max_length=250,blank=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    counselor_id = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    session_number = models.CharField(max_length=250)
    content = models.TextField()
    remark = models.CharField(max_length=200,default=0)
    reccomendation = models.CharField(max_length=250,blank=True)
    session_time = models.CharField(max_length=250)
    session_date = models.CharField(max_length=250)
    status = models.CharField(default=0,max_length=200)

    def __str__(self):
        return f"{self.fullname} - {self.session_number} - {self.status}"

    class Meta:
        db_table = 'session_table'
    

class Message(models.Model):
    sender_patient = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.CASCADE, related_name="sent_messages_patient")
    sender_counselor = models.ForeignKey('Counselor', null=True, blank=True, on_delete=models.CASCADE, related_name="sent_messages_counselor")
    receiver_patient = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.CASCADE, related_name="received_messages_patient")
    receiver_counselor = models.ForeignKey('Counselor', null=True, blank=True, on_delete=models.CASCADE, related_name="received_messages_counselor")
    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_table'

    def __str__(self):
        sender = self.sender_patient if self.sender_patient else self.sender_counselor
        receiver = self.receiver_patient if self.receiver_patient else self.receiver_counselor
        return f"{sender} -> {receiver}: {self.content}"
