import random
from django.views.generic import ListView
from .models import Question
from django.utils import timezone
from datetime import datetime

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 1  # Show one question at a time

    def get_queryset(self):
        # Check if we need to reset the score
        reset_value = self.request.GET.get('reset')
        
        if reset_value == '1':
            self.reset_score()

        # Get the selected subject or default to 'Medicine'
        selected_subject = self.request.GET.get('subject', 'Medicine')
        
        # Get the block size from the session or default to 5
        block_size = self.request.session.get('block_size', 5)
        
        # Check if the current subject or block size has changed, and reset score if needed
        current_subject = self.request.session.get('current_subject')
        current_block_size = self.request.session.get('block_size')
        
        if selected_subject != current_subject or block_size != current_block_size:
            self.reset_score()  # Reset score when subject or block size changes

        # Step 1: Filter the questions by the selected subject
        questions = Question.objects.filter(subject=selected_subject)

        # Step 2: Get the list of question IDs from the filtered questions
        question_ids = list(questions.values_list('id', flat=True))

        # Step 3: Shuffle and store a random order of questions if subject or block size changed
        if selected_subject != current_subject or block_size != current_block_size:
            random.shuffle(question_ids)
            # Store only the number of question IDs based on the block size (5 or 10)
            self.request.session['random_question_order'] = question_ids[:block_size]
            self.request.session['current_subject'] = selected_subject
            self.request.session['block_size'] = block_size
            self.request.session['start_time'] = timezone.now().isoformat()  # Track start time

        # Retrieve the stored random order of questions
        random_question_ids = self.request.session['random_question_order']
        queryset = Question.objects.filter(id__in=random_question_ids)

        # Manually reorder the queryset based on the stored random question order
        question_dict = {question.id: question for question in queryset}
        ordered_queryset = [question_dict[question_id] for question_id in random_question_ids if question_id in question_dict]

        return ordered_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Question.objects.values_list('subject', flat=True).distinct()
        context['selected_subject'] = self.request.GET.get('subject', 'Medicine')  # Default subject to 'Medicine'
        block_size = self.request.GET.get('block_size')

        # Store the block size in the session when user selects 5 or 10 questions
        if block_size in ['5', '10']:
            # Reset score if block size changes
            if int(block_size) != self.request.session.get('block_size'):
                self.reset_score()
            self.request.session['block_size'] = int(block_size)

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

            # Update the score if the answer is correct
            if context['is_correct']:
                self.request.session['score'] = self.request.session.get('score', 0) + 1
            context['score'] = self.request.session.get('score', 0)
        else:
            context['answered'] = False
            context['score'] = self.request.session.get('score', 0)

        # Track time once the quiz ends
        if not self.get_paginate_by(context['object_list']) or not context['page_obj'].has_next():
            start_time_str = self.request.session.get('start_time')

            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str)
                end_time = timezone.now()
                time_taken = end_time - start_time

                minutes = time_taken.seconds // 60
                seconds = time_taken.seconds % 60
                context['time_taken'] = f"{minutes} minutes {seconds} seconds"

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def reset_score(self):
        self.request.session['score'] = 0
        self.request.session['random_question_order'] = None
        self.request.session['current_subject'] = None
        self.request.session['block_size'] = None
