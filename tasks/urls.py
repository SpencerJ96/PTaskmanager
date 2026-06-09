from django.urls import path #Import paths for routing and views from folder
from . import views

							#Create urlpatterns array - pass in url path, views function and name for reference in templates
urlpatterns = [
	path("", views.task_list, name="task_list"),
	path("create/", views.task_create, name="task_create"),
	path("complete/<int:task_id>/", views.task_complete, name="task_complete"),			#Pass in task id to browser for specific object tasks
	path("delete/<int:task_id>/", views.task_delete, name="task_delete")
]