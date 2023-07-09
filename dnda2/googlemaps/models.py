from django.db import models

# Create your models here.
class video(models.Model):
    AreaName = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.AreaName