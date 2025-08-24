from django.urls import path, include

urlpatterns = [
    path('', include('journal_app.apps.entries.urls')),
]
