
from rest_framework import generics , status
from .models import Task
from .serializers import TaskSerializer 
from utils.permissions import IsAdminOrSuperAdmin  ,IsAdminOrTaskOwner 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView 
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend


# Admin / SuperAdmins
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

#Admin/Superadmin/User      
class TaskDetailView(APIView):
    permission_classes = [IsAdminOrTaskOwner]

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)

        # Admins/superAdmins can update all fields
        if request.user.is_admin or request.user.is_superadmin:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Task owner/user can only update status , completion_report , worked_hours
        if task.assigned_to == request.user:
            if set(request.data.keys()) != {'status' , 'completion_report', 'worked_hours'}:
                return Response({
                    "detail": "You can only update the status , completion_report and worked_hours field"
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail": "You do not have permission to update"
        }, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)

        # Only admins and superAdmin can delete
        if request.user.is_admin or request.user.is_superadmin:
            task.delete()
            return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        return Response({
            "detail": "Only Admin or SuperAdmin can delete tasks"
        }, status=status.HTTP_403_FORBIDDEN)
    
# Checking the task is completed or not 
class TaskReportDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return Task.objects.select_related('assigned_to', 'created_by')

    def get_object(self):
        task = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

        if task.status != 'COMPLETED':
            raise NotFound(detail="Task is not completed or doesn't exist")

        self.check_object_permissions(self.request, task)
        return task
    
# View/Filter COMPLETED tasks
class CompletedTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assigned_to', 'created_by']

    def get_queryset(self):
        return Task.objects.filter(
            status='COMPLETED'
        ).select_related('assigned_to', 'created_by')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"detail": "No completed tasks found"},
                status=status.HTTP_200_OK
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




