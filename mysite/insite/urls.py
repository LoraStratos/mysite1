from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('<question_id>/vote/', vote, name='vote'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', LoginViewMy.as_view(), name='login'),
    path('accounts/<int:pk>', Profile.as_view(), name='profile'),
    path('delete_profile/<int:pk>', UserDelete.as_view(), name='delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('historylist/', HistoryList.as_view(), name='history'),
    path('edit_profile/', EditProfile.as_view(), name='edit')
]