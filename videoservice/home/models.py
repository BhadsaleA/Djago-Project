from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
SUBSCRIPTION = (
    ('F','FREE'),
    ('M','MONTHLY'),
    ('Y','YEARLY')
)

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateTimeField(null=True,blank=True)
    subscription_type = models.CharField(max_length=100,choices=SUBSCRIPTION,default='FREE')

class Course(models.Model):
    Course_name = models.CharField(max_length=225)
    Course_description = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='course')
    slug = models.SlugField(blank=True)


    def save(self,*args,** kwargs):
        self.slug = slugify(self.Course_name)
        super(Course,self).save(*args,**kwargs)

    def __str__(self):
        return self.Course_name
    
class CourseModule(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=225)
    course_description = RichTextField()
    video_url = models.URLField(max_length=300)
    can_view = models.BooleanField(default=False)