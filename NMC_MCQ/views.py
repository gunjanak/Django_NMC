
from django.views.generic import ListView
from .models import Question


class QuestionListView(ListView):
    model = Question
    template_name = 'NMC_MCQ/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        # Get the subject from query parameters
        selected_subject = self.request.GET.get('subject')
        
        # Filter the queryset based on the selected subject
        if selected_subject:
            return Question.objects.filter(subject=selected_subject)
        return Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all distinct subjects for the dropdown
        context['subjects'] = Question.objects.values_list('subject', flat=True).distinct()
        
        # Add the selected subject for the template
        context['selected_subject'] = self.request.GET.get('subject')
        return context
