from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=100)
    summary = models.TextField()

class CourseFeedback(models.Model):
    course = models.CharField(max_length=255, default="Unknown Course")
    rating = models.IntegerField()  # Rating from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.course} - {self.rating}"
