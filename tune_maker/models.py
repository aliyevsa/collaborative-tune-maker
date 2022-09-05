from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, default='New Project')
    length = models.IntegerField(null=False, blank=False, default=16)
    owner = models.ForeignKey(User, related_name='project_owner', null=False, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(User, related_name='project_collaborator', null=True, blank=True, on_delete=models.SET_NULL)

class Discussion(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=True)

class Notes(models.Model):
    note_1 = models.BooleanField(default=False)
    note_2 = models.BooleanField(default=False)
    note_3 = models.BooleanField(default=False)
    note_4 = models.BooleanField(default=False)
    note_5 = models.BooleanField(default=False)
    note_6 = models.BooleanField(default=False)
    note_7 = models.BooleanField(default=False)
    note_8 = models.BooleanField(default=False)
    note_9 = models.BooleanField(default=False)
    note_10 = models.BooleanField(default=False)
    note_11 = models.BooleanField(default=False)
    note_12 = models.BooleanField(default=False)
    note_13 = models.BooleanField(default=False)
    note_14 = models.BooleanField(default=False)
    note_15 = models.BooleanField(default=False)
    note_16 = models.BooleanField(default=False)
    note_17 = models.BooleanField(default=False)
    note_18 = models.BooleanField(default=False)
    note_19 = models.BooleanField(default=False)
    note_20 = models.BooleanField(default=False)
    note_21 = models.BooleanField(default=False)
    note_22 = models.BooleanField(default=False)
    note_23 = models.BooleanField(default=False)
    note_24 = models.BooleanField(default=False)

    def get_notes(self):
        'Returns boolean values for each note as a list.'
        return [
            self.note_1, self.note_2, self.note_3, self.note_4, 
            self.note_5, self.note_6, self.note_7, self.note_8,
            self.note_9, self.note_10, self.note_11, self.note_12, 
            self.note_13, self.note_14, self.note_15, self.note_16,
            self.note_17, self.note_18, self.note_19, self.note_20, 
            self.note_21, self.note_22, self.note_23, self.note_24,
        ]

class TuneRow(models.Model):
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE)
    number = models.IntegerField(null=False, blank=False, default=0)
    notes = models.ForeignKey(Notes, null=False, on_delete=models.CASCADE)
