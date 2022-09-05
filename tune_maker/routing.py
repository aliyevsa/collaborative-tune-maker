from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'project_socket/(?P<project_id>\w+)/$', consumers.ProjectConsumer.as_asgi()),
    re_path(r'discussion_socket/(?P<project_id>\w+)/$', consumers.DiscussionConsumer.as_asgi()),
]
