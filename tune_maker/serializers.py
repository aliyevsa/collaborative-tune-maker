from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProjectSerializer(ModelSerializer):
    owner = UserSerializer()
    collaborator = UserSerializer()
    
    class Meta:
        model = Project
        fields = ['pk', 'name', 'length', 'owner', 'collaborator']
    
    def create(self, validated_data):
        owner_username = self.initial_data.get('owner')['username']
        collaborator_username = self.initial_data.get('collaborator')['username']

        project = Project(**{**validated_data,
            'owner': User.objects.get(username=owner_username),
            'collaborator': User.objects.get(username=collaborator_username)})
        
        project.save()
        return project
    
    def update(self, instance, validated_data):
        owner_username = self.initial_data.get('owner')['username']
        collaborator_username = self.initial_data.get('collaborator')['username']

        instance.name = validated_data.get('name', instance.name)
        instance.length = validated_data.get('length', instance.length)
        instance.owner = User.objects.get(username=owner_username)
        instance.collaborator = User.objects.get(username=collaborator_username)

        instance.save()
        return instance

class DiscussionSerializer(ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['user', 'project', 'message']

class NotesSerializer(ModelSerializer):
    class Meta:
        model = Notes
        fields = [
            'note_1', 'note_2', 'note_3', 'note_4',
            'note_5', 'note_6', 'note_7', 'note_8',
            'note_9', 'note_10', 'note_11', 'note_12',
            'note_13', 'note_14', 'note_15', 'note_16',
            'note_17', 'note_18', 'note_19', 'note_20',
            'note_21', 'note_22', 'note_23', 'note_24',
        ]

class TuneRowSerializer(ModelSerializer):
    class Meta:
        model = TuneRow
        fields = ['project', 'number', 'notes']
