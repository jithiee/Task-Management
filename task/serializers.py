from rest_framework import serializers
from .models import Task , CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        error_messages={
            'does_not_exist': 'User with username={value} does not exist.',
            'invalid': 'Invalid username format.'
        }
    )
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'due_date', 'status',
            'completion_report', 'worked_hours', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'completion_report': {'required': False},
            'worked_hours': {'required': False}
        }

    def validate(self, data):
        current_status = self.instance.status if self.instance else None
        
        # Preventing changing status from COMPLETED
        if current_status == 'COMPLETED' and 'status' in data:
            if data['status'] != 'COMPLETED':
                raise serializers.ValidationError({
                    'status': "Cannot change status from COMPLETED"
                })
        
        #  Validate completion requirements
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': "Completion report is required when marking task as completed"
                })
            if not data.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': "Worked hours are required when marking task as completed"
                })
        
        return data
    #Only task assigned to regular users not admins
    def validate_assigned_to(self, value):
        if value.role != 'USER':
            raise serializers.ValidationError(
                "Tasks can only be assigned to regular users not admins"
            )
        return value
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# class TaskSerializer(serializers.ModelSerializer):
#     assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 
#                   'completion_report', 'worked_hours', 'created_at', 'updated_at']
#         read_only_fields = ['created_by' ,'created_at', 'updated_at']
        
# #validate if the COMPLETED can't update the Status 
# def validate(self, data):
#     if self.instance and self.instance.status == Task.STATUS_COMPLETED:
#         if 'status' in data and data['status'] != Task.STATUS_COMPLETED:
#             raise serializers.ValidationError("Cannot change status from COMPLETED")
    
#     if data.get('status') == Task.STATUS_COMPLETED:
#         if not data.get('completion_report'):
#             raise serializers.ValidationError("Completion report is required when marking task as completed")
#         if not data.get('worked_hours'):
#             raise serializers.ValidationError("Worked hours are required when marking task as completed")
    
#     return data



