from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser



class Department(models.Model):
    department = models.CharField(max_length=300)

    def __str__(self):
        return self.department


class Course(models.Model):
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.CharField(max_length=300)

    def __str__(self):
        return self.course
    
class HashTag(models.Model):
    hashtag=models.CharField(max_length=200)
    def __str__(self):
        return self.hashtag
  
class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profile_pic=models.ImageField(null=True,blank=True,upload_to='profile_pics')
    phone_number = models.CharField(unique=True, max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)  # Make department nullable
    status = models.CharField(max_length=20, default="freemium" ,choices=[('admin', 'Admin'), ('premium', 'Premium'),('pending','Pending'), ('freemium', 'Freemium')])

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
#Q&A
class Questions(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question=models.CharField(max_length=2000)
    date=models.DateTimeField(auto_now_add=True)
    hashtags=models.ManyToManyField(HashTag, blank=True)
    def __str__(self):
        return self.question
	
    

    
class Answers(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE, related_name='answers')
    answer=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    verified=models.BooleanField(default=False)
    likes = models.ManyToManyField(CustomUser, related_name='liked_answers', blank=True)
    
    def __str__(self):
        return f'Answer by {self.user} to {self.question}'

    def total_likes(self):
        return self.likes.count()

    def is_liked_by_user(self, user):
        return self.likes.filter(id=user.id).exists()




    


class Replies(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE,related_name='replies')
    reply=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

class SavedQuestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

#News
    
class News(models.Model):
    title=models.CharField(max_length=300)
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    

class NewsComment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    news=models.ForeignKey(News, on_delete=models.CASCADE)
    comment=models.TextField()
    date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment




#pricing

class Pricing(models.Model):
    price=models.IntegerField()
    describtion=models.CharField(max_length=200)
 

#Payment 

class PaymentMethod(models.Model):
    name=models.CharField(max_length=200)
    logo=models.ImageField(upload_to='logos',blank=True,null=True)
    describtion=models.CharField(max_length=200)
    def __str__(self):
    	return self.name

 
class SubmitPayment(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    payment_method=models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    transaction_ref=models.CharField(max_length=150,unique=True)
    reciept=models.ImageField(blank=True,null=True,upload_to='reciepts')
    date=models.DateTimeField(auto_now_add=True)
    
    
    
    

#restrict or make the platform free based on the switch


class PaymentSwitch(models.Model):
    is_on = models.BooleanField(default=False)
    
    
 #advertisement
    
    
 
    
    
				
				
				




    







