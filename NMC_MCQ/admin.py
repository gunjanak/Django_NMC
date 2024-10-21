from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('question', 'subject')
    
    
admin.site.register(Question,QuestionAdmin)