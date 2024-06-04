from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.
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