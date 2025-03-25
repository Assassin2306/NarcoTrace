from django.urls import path
from . import views

urlpatterns = [
    path('flagged_message/', views.flagged_message, name='flagged_message'),  # Change back to underscore
    path('status/', views.status_check, name='status_check'),
    path('all-messages/', views.get_all_messages, name='all_messages'),
    path('batch_delete_messages/', views.batch_delete_messages, name='batch_delete_messages'),
]
