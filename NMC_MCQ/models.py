from django.db import models

# Create your models here.


class Question(models.Model):
    # Define your choices for category and subject
    CATEGORY_CHOICES = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        ('category3', 'Category 3'),
    ]
    
    SUBJECT_CHOICES = [
        ('subject1', 'Subject 1'),
        ('subject2', 'Subject 2'),
        ('subject3', 'Subject 3'),
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
