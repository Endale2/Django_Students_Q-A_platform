# views.py
from django.db.models import Count,Q,F,Sum, ExpressionWrapper,IntegerField
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView
from .models import*
from django.utils import timezone
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import*
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from functools import wraps
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test




# Custom test function to check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.status == 'admin'

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class MainDashboard(View):
    def get(self, request):
        # Gathering data for the dashboard
        total_users = CustomUser.objects.count()
        premium_users = CustomUser.objects.filter(status='premium').count()
        freemium_users = CustomUser.objects.filter(status='freemium').count()

        total_questions = Questions.objects.count()
        total_answers = Answers.objects.count()

        recent_activities = [
            {"activity": "New question added by John Doe", "time": "2 hours ago"},
            {"activity": "Jane Doe upgraded to Premium", "time": "1 day ago"},
            {"activity": "New answer by Alex Smith", "time": "3 days ago"},
        ]

        context = {
            'total_users': total_users,
            'premium_users': premium_users,
            'freemium_users': freemium_users,
            'total_questions': total_questions,
            'total_answers': total_answers,
            'recent_activities': recent_activities,
        }

        return render(request, 'dashboard/dashboard.html', context)


def payment_switch_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        payment_switch = PaymentSwitch.objects.first()  # Assuming there's only one switch
        if payment_switch.is_on:
            user = request.user
            if user.is_authenticated:
                # Check user status and redirect accordingly
                if user.status == 'freemium':
                    return redirect('pricing')
                elif user.status == 'pending':
                    return redirect('pending')
                elif user.status in ['premium', 'admin']:
                    return view_func(request, *args, **kwargs)
            else:
                # Redirect not authenticated users to login page
                return redirect("login")
        else:
            # Allow access without restriction when switch is off
            return view_func(request, *args, **kwargs)

    return _wrapped_view



# User Authentication


def alpha(request):
    user = request.user
    if user.is_authenticated:
        return redirect('questions')
    return render(request, 'base/landing.html')

@login_required
def search_view(request):
    query = request.GET.get('q')
    if query:
        # Perform search across multiple models
        question_results = Questions.objects.filter(Q(question__icontains=query))
        
        news_results = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
        # Combine results
        all_results = list(question_results) +  list(news_results)
        
        # Create a list of dictionaries containing result objects and their class names
        results_with_class_names = [{'result': result, 'class_name': result.__class__.__name__} for result in all_results]
        
        # Pagination
        paginator = Paginator(results_with_class_names, 10)  # 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'query': query,
            'results': page_obj,
        }
        return render(request, 'base/search_results.html', context)
    else:
        return render(request, 'base/search_results.html', {'query': query})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'base/profile.html'

    def get(self, request):
        user = request.user
        departments=Department.objects.all()
        return render(request, self.template_name, {'user': user, 'departments':departments})

    def post(self, request):
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department_id = request.POST.get('department')
        
        # Update first name and last name
        user.first_name = first_name
        user.last_name = last_name
        if department_id:
            department = Department.objects.get(pk=department_id)  # Get Department instance
            user.department = department
        
        # Check if profile picture is uploaded
        if 'profile_pic' in request.FILES:
            # Delete previous profile picture if exists
            if user.profile_pic:
                user.profile_pic.delete()
            # Save new profile picture
            user.profile_pic = request.FILES['profile_pic']
        
        # Check if password change is requested
        password = request.POST.get('password')
        if password:
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                user.set_password(password)
                update_session_auth_hash(request, user)  # Important!
        
        user.save()
        return redirect('profile')
 # Redirect to the profile page


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        departments = Department.objects.all()
        return render(request, 'base/registration.html', {'form': form, 'departments': departments})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Form is not valid, re-render the registration page with error messages
            departments = Department.objects.all()
            return render(request, 'base/registration.html', {'form': form, 'departments': departments})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'base/login.html', {'form': form, 'error_message': None})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract the phone number and password
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            
            # Perform custom validation for the phone number
            if not phone_number.startswith('+251') or len(phone_number) != 13:
                error_message = "Please enter a valid phone number in the format +251XXXXXXXXX."
                return render(request, 'base/login.html', {'form': form, 'error_message': error_message})
            
            # Authenticate the user
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('questions')  # Redirect to home page after successful login
            else:
                # Display error message for incorrect phone number or password
                error_message = "Incorrect phone number or password."
                return render(request, 'base/login.html', {'form': form, 'error_message': error_message})
        
        return render(request, 'base/login.html', {'form': form, 'error_message': None})

@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('landingpage')

@method_decorator(login_required, name='dispatch')
class QuestionsListView(View):
    def get(self, request):
        nav="qa"
        my_questions=Questions.objects.filter(user=request.user).order_by('-date')[:5]
        department = request.user.department 
        courses = Course.objects.filter(department=department)
        questions = Questions.objects.filter(department=department).order_by('-date')
        
        paginator = Paginator(questions, 10)  
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        
        form = QuestionForm()
        return render(request, 'questions/questions_list.html', {'my_questions':my_questions,'questions': questions, 'form': form, 'courses': courses, 'nav':nav})
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user
            question.department = request.user.department  # Assign the user's department
            question.save()
            return redirect('questions')  # Redirect after successful form submission
        
        return redirect('questions')
    
@method_decorator(login_required, name='dispatch')  
class TopQuestionsListView(View):
  

    def get(self,request):
        nav="qa"
        my_questions=Questions.objects.filter(user=request.user).order_by('-date')[:5]
        department = request.user.department 
        courses = Course.objects.filter(department=department)
        questions = Questions.objects.filter(department=department).annotate(num_answers=Count('answers')).order_by('-num_answers','-date')
        # Pagination
        paginator = Paginator(questions, 10)  
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        form = QuestionForm()

        return render(request, 'questions/top_questions_list.html',  {'my_questions':my_questions,'questions': questions, 'form': form, 'courses': courses, 'nav':nav})
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user
            question.department = request.user.department  # Assign the user's department
            question.save()
            return redirect('questions')  # Redirect after successful form submission
        
        return redirect('questions')
    
@method_decorator(login_required, name='dispatch')
class QuestionByCourseView(View):
    def get(self, request, course_id):
        nav="qa"
        my_questions=Questions.objects.filter(user=request.user).order_by('-date')[:5]
        course = Course.objects.get(id=course_id)
        courses=Course.objects.exclude(id=course_id)
        courses1=Course.objects.all() #courses list for ask question form dropdown
        questions = Questions.objects.filter(course=course).order_by('-date')
        form = QuestionForm()
        paginator = Paginator(questions, 10)  # Show 10 questions per page
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        
        return render(request, 'questions/question_by_course.html', {'my_questions':my_questions,'course': course, 'questions': questions,'courses':courses ,'courses1':courses1,'form':form,'nav':nav})
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user
            question.department = request.user.department  # Assign the user's department
            question.save()
            return redirect('questions')  # Redirect after successful form submission
        
        return redirect('questions')
    



@method_decorator(payment_switch_required, name='dispatch')
class QuestionDetailView(View):
    def get(self, request, pk):
        nav = 'qa'
        courses=Course.objects.filter(department=request.user.department)
        question = Questions.objects.get(pk=pk)
        related_questions=Questions.objects.filter(department=request.user.department,course=question.course).exclude(pk=pk).order_by('-date')[:10]
        answers = Answers.objects.filter(question=question).annotate(
    num_likes=Count('likes'),
    num_replies=Count('replies')
).annotate(
    total_likes_and_replies=ExpressionWrapper(
        F('num_likes') + F('num_replies'), 
        output_field=IntegerField()
    )
).order_by('-total_likes_and_replies','num_likes', '-date')

        paginator = Paginator(answers, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Check if the current user has saved the question
        is_saved = SavedQuestion.objects.filter(user=request.user, question=question).exists()
        num_saved_users = SavedQuestion.objects.filter(question=question).count()

        return render(request, 'questions/question_detail.html', {
            'question': question,
            'page_obj': page_obj,
            'is_saved': is_saved,
            'num_saved_users': num_saved_users,
            'nav': nav,
            'related_questions':related_questions,
            'courses':courses,
        })

    def post(self, request, pk):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user
            question.department = request.user.department  # Assign the user's department
            question.save()
            return redirect('questions')
        question = Questions.objects.get(pk=pk)
        #delete current question
        delete_question = request.POST.get('delete_question')
        if delete_question:
            if question.user == request.user:
                question.delete()
                return HttpResponseRedirect(reverse('questions'))
            else:
                # Handle unauthorized deletion
                return HttpResponseForbidden()
        
        
        answers_content = request.POST.get("answer")
        is_saved = request.POST.get('is_saved')

        # Toggle saved status for the question
        if is_saved == 'true':
            SavedQuestion.objects.create(user=request.user, question=question)
        elif is_saved == 'false':
            SavedQuestion.objects.filter(user=request.user, question=question).delete()
            
            
        # Handle like/unlike functionality

        answer_id = request.POST.get('answer_id')
        is_liked = request.POST.get('is_liked')

        if answer_id and is_liked is not None:
            answer = get_object_or_404(Answers, pk=answer_id)
            if is_liked == 'true':
                answer.likes.add(request.user)
            else:
                answer.likes.remove(request.user)
            return HttpResponseRedirect(reverse('question-detail', args=[pk]))
        # Handle replying to answers
        reply_content = request.POST.get("reply")
        if reply_content:  # Check if there is any reply content
            answer_id = request.POST.get("answer_id")
            answer = get_object_or_404(Answers, id=answer_id)
            reply = Replies.objects.create(
                user=request.user,
                answer=answer,
                reply=reply_content,
                date=timezone.now()
            )
            return HttpResponseRedirect(reverse('question-detail', args=[pk]))
        
        

        # Handle deletion of answers
        delete_answer_id = request.POST.get('delete_answer_id')
        if delete_answer_id:
            answer_to_delete = get_object_or_404(Answers, pk=delete_answer_id)
            if answer_to_delete.user == request.user:
                answer_to_delete.delete()
                return HttpResponseRedirect(reverse('question-detail', args=[pk]))
            else:
                # Handle unauthorized deletion
                return HttpResponseForbidden()

        # Handle deletion of replies
        delete_reply_id = request.POST.get('delete_reply_id')
        if delete_reply_id:
            reply_to_delete = get_object_or_404(Replies, pk=delete_reply_id)
            if reply_to_delete.user == request.user:
                reply_to_delete.delete()
                return HttpResponseRedirect(reverse('question-detail', args=[pk]))
            else:
                # Handle unauthorized deletion
                return HttpResponseForbidden()

        # Create a new answer if content is provided
        if answers_content:
            answer = Answers.objects.create(
                user=request.user,
                question=question,
                answer=answers_content,
                date=timezone.now()
            )
            return HttpResponseRedirect(reverse('question-detail', args=[pk]))
        else:
            messages.error(request, 'Answer content is required.')
            return redirect('question-detail', pk=pk)



@method_decorator(payment_switch_required, name='dispatch')
class SavedQuestionsView(View):
    def get(self,request):
        nav="saved"
        my_questions=Questions.objects.filter(user=request.user).order_by('-date')[:5]
        questions=SavedQuestion.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(questions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'questions/saved_questions.html',{'my_questions':my_questions,'questions':questions,'nav':nav,'page_obj':page_obj,})


@method_decorator(login_required, name='dispatch')  
class MyQuestionsView(View):
    def get(self,request):
        saved_questions=SavedQuestion.objects.filter(user=request.user).order_by('-date')[:5]
        questions=Questions.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(questions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'questions/my_questions.html',{'saved_questions':saved_questions,'questions':questions,'page_obj':page_obj,})
     

@method_decorator(login_required, name='dispatch')
class NewsListView(View):
    def get(self, request):
        nav="news"
        news = News.objects.annotate(comment_count=Count('newscomment'))
    
        return render(request, 'news/news.html', {'news': news,'nav':nav})
    
    
@method_decorator(login_required, name='dispatch')
class NewsDetailView(View):
    def get(self, request, pk):
        news = News.objects.get(pk=pk)
        news_list=News.objects.exclude(pk=pk)
        nav = "news"
        return render(request, 'news/news_detail.html', {'news': news, 'nav': nav,'news_list':news_list})

    def post(self, request, pk):
        news = News.objects.get(pk=pk)
        comment_text = request.POST.get('comment')
        comment_id = request.POST.get('comment_id')  # Get the comment_id from POST data
        if comment_text:
            # Assuming you have a logged-in user accessing this page
            user = request.user
            # Create a new comment associated with the news item
            NewsComment.objects.create(user=user, news=news, comment=comment_text)
        elif comment_id:  # Check if a comment deletion request was made
            comment = NewsComment.objects.get(pk=comment_id)
            if comment.user == request.user:
                comment.delete()
        # Redirect back to the news detail page after adding or deleting the comment
        return redirect('news-detail', pk=pk)
        


@method_decorator(login_required, name='dispatch')
class PricingView(View):
    def get(self,request):
        return render (request,'base/pricing.html')
    
@method_decorator(login_required, name='dispatch')    
class PendingView(View):
    
    def get(self,request):
        return render(request,'base/pending.html')
    
    
@method_decorator(login_required, name='dispatch')
class  SubmitPayment(View):
    def get(self,request):
        return render(request,'base/payment.html')