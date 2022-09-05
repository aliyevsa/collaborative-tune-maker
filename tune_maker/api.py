from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *

class TuneRowsAPI(generics.ListAPIView):
    serializer_class = TuneRowSerializer

    def get_queryset(self):
        project = self.kwargs['project_id']
        return TuneRow.objects.filter(project=project)

class NotesAPI(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# # For testing only
# class ProjectAPI(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
