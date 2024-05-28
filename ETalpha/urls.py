"""
URL configuration for ETalpha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from alpha.views import*
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',alpha, name="landingpage"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('search/', search_view, name='search'),
    path('pricing/',PricingView.as_view(),name="pricing"),
    path('pending/',PendingView.as_view(), name="pending"),
#q&a
    path('questions/', QuestionsListView.as_view(), name='questions'),
    path('questions/top/', TopQuestionsListView.as_view(), name='top_questions_list'),
    path('questions/bycourse/<int:course_id>/', QuestionByCourseView.as_view(), name='questions-by-course'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/saved',SavedQuestionsView.as_view(), name="saved-questions"),
    path('questions/my-questions',MyQuestionsView.as_view(), name="my-questions"),

#news
path('news/', NewsListView.as_view(), name='news'),
path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

#auth
    path('register/', RegistrationView.as_view(), name="registration"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', custom_logout_view, name='logout'),
    
#dashboard
path('dashboard/',MainDashboard.as_view(), name="dashboard"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
