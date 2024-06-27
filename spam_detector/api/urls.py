from django.urls import path
from .views import RegisterView, CustomAuthToken, MarkSpamView, SearchByNameView, SearchByPhoneNumberView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('mark-spam/', MarkSpamView.as_view(), name='mark_spam'),
    path('search/name/', SearchByNameView.as_view(), name='search_name'),
    path('search/phone/', SearchByPhoneNumberView.as_view(), name='search_phone'),
]
