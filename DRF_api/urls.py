from django.urls import path 
from DRF_api import views
from DRF_api import views as user_view
# define the urls
urlpatterns = [
    # path('tasks/', views.tasks),
    # path('tasks/<int:pk>/', views.task_detail),
    path('users/', user_view.UsersView.as_view()),
    path('users/<str:user>', user_view.DeleteView.as_view()),
    path('user/uploadcsv', user_view.MyFileView.as_view()),
    path('user/groupby', user_view.GroupView.as_view()),
    path('user/cleardb', user_view.ClearDBView.as_view())
]