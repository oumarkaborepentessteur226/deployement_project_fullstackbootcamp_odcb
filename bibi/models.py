from django.db import models

# Create your models here.
class Document(models.Model):
   nom = models.CharField(max_length=255)
   file = models.FileField(upload_to="pdf")
   description = models.TextField(null=True)

   def __str__(self):
      return self.nom
