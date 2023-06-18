from django.db import models

# Create your models here.

precedence_choices = (
    (1, "primary"),
    (2, "secondary")
)


class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    phoneNumber = models.PositiveBigIntegerField(null=True)
    email = models.EmailField(null=True)
    linkedId = models.IntegerField(null=True)
    linkPrecedence = models.CharField(
        max_length=16,
        choices=precedence_choices,
        default=1
    )
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)
