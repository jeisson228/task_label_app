from rest_framework import serializers
from .models import Task, Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name'] #I guess the id is not a 
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    completed = serializers.BooleanField(required=True)
    labels = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all(),
        many=True,
        required=False,
        allow_empty=True
    )

    def update(self, instance, validated_data):
        # Handle labels separately
        labels = validated_data.pop('labels', None)
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Clear all labels if labels is None or empty list
        if labels is not None:
            instance.labels.set(labels)
        else:
            instance.labels.clear()
            
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['labels']:
            representation['labels'] = []
        return representation

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'labels']
        read_only_fields = ['id'] 