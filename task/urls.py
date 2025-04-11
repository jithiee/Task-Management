from django.urls import path
from .views import TaskListCreateView,TaskDetailView  , TaskReportDetailView ,CompletedTaskListView

urlpatterns = [
    # Admin task management
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
 
    # Task reports (Superadmin/admin only)
    path('tasks/<int:pk>/report/', TaskReportDetailView.as_view(), name='task-report'),
    path('tasks/completed/', CompletedTaskListView.as_view(), name='completed-tasks-list'),

]