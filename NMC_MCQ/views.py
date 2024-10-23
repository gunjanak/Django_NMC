import random

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.decorators import action
from rest_framework import viewsets

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny



from django.views.generic import ListView
from django.utils import timezone
from django.contrib.auth.models import User


from .models import Question
from .serializers import QuestionSerializer,RegisterSerializer

from datetime import datetime


#Logout view (Blacklisting tokens)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated)
    def post(self,request,*args,**kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
#Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    
    #List all unique subjects
    @action(detail=False,methods=['get'],url_path='subjects')
    def list_subjects(self,request):
        subjects = Question.objects.values_list('subject',flat=True).distinct()
        return Response(subjects)
    
    #Get all questions for a specific subject
    @action(detail=False,methods=['get'],url_path='(?P<subject>[^/.]+)')
    def get_questions_by_subject(self,request,subject=None):
        questions = Question.objects.filter(subject=subject)
        serializer = self.get_serializer(questions,many=True)
        return Response(serializer.data)
    
    
    #Get x number of questions for a specific subject
    @action(detail=False,methods=['get'],url_path='(?P<subject>[^/.]+)/(?P<num>\d+)')
    def get_limited_questions_by_subject(self,request,subject=None,num=None):
        try:
            num = int(num)
            questions = Question.objects.filter(subject=subject)[:num]
            serializer = self.get_serializer(questions,many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error':"Invalid number format"},
                            status=status.HTTP_400_BAD_REQUEST)
            
    
    
    
    
    
# class QuestionListView(ListView):
#     model = Question
#     template_name = 'questions/question_list.html'
#     context_object_name = 'questions'
#     paginate_by = 1  # Show one question at a time

#     def get_queryset(self):
#         reset_value = self.request.GET.get('reset')
        
#         if reset_value == '1':
#             self.reset_score()

#         selected_subject = self.request.GET.get('subject', 'Medicine')
#         block_size = self.request.session.get('block_size', 5)
#         current_subject = self.request.session.get('current_subject')
#         current_block_size = self.request.session.get('block_size')
        
#         if selected_subject != current_subject or block_size != current_block_size:
#             self.reset_score()

#         questions = Question.objects.filter(subject=selected_subject)
#         question_ids = list(questions.values_list('id', flat=True))

#         if selected_subject != current_subject or block_size != current_block_size:
#             random.shuffle(question_ids)
#             self.request.session['random_question_order'] = question_ids[:block_size]
#             self.request.session['current_subject'] = selected_subject
#             self.request.session['block_size'] = block_size
#             self.request.session['start_time'] = timezone.now().isoformat()

#         random_question_ids = self.request.session['random_question_order']
#         queryset = Question.objects.filter(id__in=random_question_ids)
#         question_dict = {question.id: question for question in queryset}
#         ordered_queryset = [question_dict[question_id] for question_id in random_question_ids if question_id in question_dict]

#         return ordered_queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['subjects'] = Question.objects.values_list('subject', flat=True).distinct()
#         context['selected_subject'] = self.request.GET.get('subject', 'Medicine')
#         block_size = self.request.GET.get('block_size')

#         if block_size in ['5', '10']:
#             if int(block_size) != self.request.session.get('block_size'):
#                 self.reset_score()
#             self.request.session['block_size'] = int(block_size)

#         for question in context['questions']:
#             options = [question.option1, question.option2, question.option3, question.option4]
#             random.shuffle(options)
#             question.shuffled_options = options

#         selected_option = self.request.POST.get('selected_option')
#         if selected_option:
#             current_question = context['questions'][0]
#             correct_option = current_question.correct_option
#             context['selected_option'] = selected_option
#             context['is_correct'] = (selected_option == correct_option)
#             context['answered'] = True

#             if context['is_correct']:
#                 self.request.session['score'] = self.request.session.get('score', 0) + 1
#             else:
#                 # Track incorrectly answered questions
#                 incorrect_answers = self.request.session.get('incorrect_answers', [])
#                 incorrect_answers.append({
#                     'question': current_question.question,
#                     'your_answer': selected_option,
#                     'correct_answer': correct_option
#                 })
#                 self.request.session['incorrect_answers'] = incorrect_answers

#             context['score'] = self.request.session.get('score', 0)
#         else:
#             context['answered'] = False
#             context['score'] = self.request.session.get('score', 0)

#         if not self.get_paginate_by(context['object_list']) or not context['page_obj'].has_next():
#             start_time_str = self.request.session.get('start_time')

#             if start_time_str:
#                 start_time = datetime.fromisoformat(start_time_str)
#                 end_time = timezone.now()
#                 time_taken = end_time - start_time

#                 minutes = time_taken.seconds // 60
#                 seconds = time_taken.seconds % 60
#                 context['time_taken'] = f"{minutes} minutes {seconds} seconds"

#                 # Add incorrect answers to the context
#                 context['incorrect_answers'] = self.request.session.get('incorrect_answers', [])

#         return context

#     def post(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)

#     def reset_score(self):
#         self.request.session['score'] = 0
#         self.request.session['random_question_order'] = None
#         self.request.session['current_subject'] = None
#         self.request.session['block_size'] = None
#         self.request.session['incorrect_answers'] = []  # Clear incorrect answers



