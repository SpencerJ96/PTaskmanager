from django.urls import path
from . import views

urlpatterns = [
	path("", views.task_list, name="task_list"),
	path("create/", views.task_create, name="task_create"),
	path("all/", views.task_all, name="task_all"),
	path("completed/", views.task_allCompleted, name="task_allCompleted"),
	path("filter/", views.task_filter, name="task_filter"),
	path("delete/<int:task_id>/", views.task_delete, name="task_delete"),
	path("status/<int:task_id>/", views.task_status, name="task_status"),
	path("edit/<int:task_id>/", views.task_edit, name="task_edit"),
	path("register/", views.register, name="register")
	]
