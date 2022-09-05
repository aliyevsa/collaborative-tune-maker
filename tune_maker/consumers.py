from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *

class ProjectConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def update_note(self, project_id, row_number, note, operation):
        tune_row = TuneRow.objects.filter(project=project_id).filter(number=row_number).first()
        notes = Notes.objects.get(pk=tune_row.notes.pk)
        
        field_name = 'note_' + str(note + 1)
        
        if operation == 'add':
            setattr(notes, field_name, True)
        elif operation == 'delete':
            setattr(notes, field_name, False)

        notes.save()
    
    @sync_to_async
    def load_notes(self, project_id):
        project = Project.objects.get(pk=project_id)
        tune_rows = TuneRow.objects.filter(project=project)
        tune_rows_notes = []
        for tune_row in tune_rows:
            tune_rows_notes.append(tune_row.notes.get_notes())

        return tune_rows_notes

    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.project_name = 'project_' + str(self.project_id)

        await self.channel_layer.group_add(
            self.project_name,
            self.channel_name,
        )
        await self.accept()
        previous_notes = await self.load_notes(project_id=self.project_id)
        await self.send(text_data=json.dumps({
            'previous_notes': previous_notes,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.project_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        row = text_data_json['row']
        note = text_data_json['note']
        operation = text_data_json['operation']

        await self.update_note(project_id=self.project_id, row_number=row, note=note, operation=operation)
        await self.channel_layer.group_send(
            self.project_name,
            {
                'type': 'project_event',
                'row': row,
                'note': note,
                'operation': operation,
            },
        )

    async def project_event(self, event):
        row = event['row']
        note = event['note']
        operation = event['operation']

        await self.send(text_data=json.dumps({
            'row': row,
            'note': note,
            'operation': operation,
        }))

class DiscussionConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def save_discussion(self, project_id, user, message):
        discussion = Discussion()
        discussion.project = Project.objects.get(pk=project_id)
        discussion.user = User.objects.get(username=user)
        discussion.message = message
        discussion.save()
    
    @sync_to_async
    def load_discussions(self, project_id):
        discussion_list = Discussion.objects.filter(project=project_id)
        discussion_message_list = [discussion.user.username + ': ' + discussion.message for discussion in discussion_list]
        discussions = '\n'.join(discussion_message_list)
        return discussions

    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.discussion_name = 'discussion_' + str(self.project_id)

        await self.channel_layer.group_add(
            self.discussion_name,
            self.channel_name,
        )
        await self.accept()
        previous_discussions = await self.load_discussions(project_id=self.project_id)
        await self.send(text_data=json.dumps({
            'user': False,
            'message': previous_discussions,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.discussion_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        message = text_data_json['message']

        await self.save_discussion(project_id=self.project_id, user=user, message=message)
        await self.channel_layer.group_send(
            self.discussion_name,
            {
                'type': 'discussion_message',
                'user': user,
                'message': message,
            },
        )
    
    async def discussion_message(self, event):
        user = event['user']
        message = event['message']

        await self.send(text_data=json.dumps({
            'user': user,
            'message': message,
        }))
    