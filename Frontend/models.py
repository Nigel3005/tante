from django.db import models


class contact(models.Model):
    name = models.CharField(max_length=200, default=" ")
    email = models.EmailField(max_length=200, default=" ")
    bericht = models.TextField(max_length=200, default=" ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact"


# declare a new model with a name "GeeksModel"
class GeeksModel(models.Model):

    # fields of the model
    title = models.CharField(max_length = 200)
    description = models.TextField()

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title
