from django.contrib import admin
from django.urls import path, include

#Tell Django the main url file for the tasks app - any request starting with tasks/ should be handled via tasks.urls

urlpatterns = [
    path('admin/', admin.site.urls),
	path("tasks/", include("tasks.urls")),
	path("accounts/", include("django.contrib.auth.urls")),
]
