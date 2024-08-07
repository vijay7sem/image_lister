from django.db import models

class Image(models.Model):
    drive_file_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
