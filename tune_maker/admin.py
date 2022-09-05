from django.contrib import admin
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'length', 'owner', 'collaborator')

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'message')

class NotesAdmin(admin.ModelAdmin):
    list_display = (
        'note_1', 'note_2', 'note_3', 'note_4',
        'note_5', 'note_6', 'note_7', 'note_8',
        'note_9', 'note_10', 'note_11', 'note_12',
        'note_13', 'note_14', 'note_15', 'note_16',
        'note_17', 'note_18', 'note_19', 'note_20',
        'note_21', 'note_22', 'note_23', 'note_24',
    )

class TuneRowAdmin(admin.ModelAdmin):
    list_display = ('number', 'notes')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(TuneRow, TuneRowAdmin)
