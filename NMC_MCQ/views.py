import random
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView
from django.utils import timezone
from .models import Question

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 1  # Show one question at a time
    
    

    def get_queryset(self):
        reset_value = self.request.GET.get('reset')
        print(reset_value)
        
        if reset_value == '1':
            self.reset_score()
            
        selected_subject = self.request.GET.get('subject')

        # Step 1: Filter the questions by the selected subject
        if selected_subject:
            questions = Question.objects.filter(subject=selected_subject)
        else:
            questions = Question.objects.all()  # If no subject is selected, return all questions

        # Step 2: Get the list of question IDs from the filtered questions
        question_ids = list(questions.values_list('id', flat=True))

        # Step 3: Reset random order if a new subject is selected or not set in session
        current_subject = self.request.session.get('current_subject')
        if selected_subject != current_subject:
            # Shuffle the question IDs and store them in the session
            random.shuffle(question_ids)
            self.request.session['random_question_order'] = question_ids
            self.request.session['current_subject'] = selected_subject  # Update the current subject in the session
            
            
            # **Store start time as an ISO string**
            self.request.session['start_time'] = timezone.now().isoformat()


        # Step 4: Retrieve the stored randomized question order
        random_question_ids = self.request.session['random_question_order']

        # Step 5: Fetch the questions in the randomized order
        queryset = Question.objects.filter(id__in=random_question_ids)

        # Step 6: Manually reorder the queryset according to the randomized question order stored in the session
        question_dict = {question.id: question for question in queryset}
        ordered_queryset = [question_dict[question_id] for question_id in random_question_ids if question_id in question_dict]

        return ordered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Question.objects.values_list('subject', flat=True).distinct()
        context['selected_subject'] = self.request.GET.get('subject')

        # Shuffle the options for each question
        for question in context['questions']:
            options = [question.option1, question.option2, question.option3, question.option4]
            random.shuffle(options)
            question.shuffled_options = options

        selected_option = self.request.POST.get('selected_option')
        if selected_option:
            current_question = context['questions'][0]  # Only one question due to paginate_by
            correct_option = current_question.correct_option
            context['selected_option'] = selected_option
            context['is_correct'] = (selected_option == correct_option)
            context['answered'] = True

            # Update the score if correct
            if context['is_correct']:
                self.request.session['score'] = self.request.session.get('score', 0) + 1
            context['score'] = self.request.session.get('score', 0)

        else:
            context['answered'] = False
            context['score'] = self.request.session.get('score', 0)  # Retrieve the score
            
     

        # Check if all questions are answered
        if not self.get_paginate_by(context['object_list']) or not context['page_obj'].has_next():
            start_time_str = self.request.session.get('start_time')

            if start_time_str:
                # Convert start time back to a datetime object
                start_time = datetime.fromisoformat(start_time_str)
                end_time = timezone.now()
                time_taken = end_time - start_time

                # Convert time to minutes and seconds
                minutes = time_taken.seconds // 60
                seconds = time_taken.seconds % 60
                context['time_taken'] = f"{minutes} minutes {seconds} seconds"

                
                
        return context

    def post(self, request, *args, **kwargs):
        # Handle the form submission
        return self.get(request, *args, **kwargs)

    def reset_score(self):
        # Optionally, provide a method to reset the score when a new quiz starts
        self.request.session['score'] = 0
        # self.request.session['random_question_order'] = None  # Reset the question order
        # self.request.session['current_subject'] = None  # Reset the current subject
