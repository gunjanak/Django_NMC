from django.db import models

# Create your models here.


class Question(models.Model):
    # Define your choices for category and subject
    CATEGORY_CHOICES = [
        ('MBBS', 'MBBS'),
        ('BDS', 'BDS'),
        ('MS', 'MS'),
    ]
    
    SUBJECT_CHOICES = [
        ('Surgery', 'Surgery'),
        ('Medicine', 'Medicine'),
        ('Gyane', 'Gyane'),
    ]

    # Fields for the Question model
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    correct_option = models.TextField()  # This could be validated later to ensure it matches one of the options
    
    # Choices fields
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)

    def __str__(self):
        return self.question
