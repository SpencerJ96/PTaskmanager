from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Task



def task_list(request):
	#Fetches every task from the DB and sorts it so incomplete comes first and higher priority tasks appear before lower
		#Completed is boolean in the modal (0 is false, 1 is true) we are sorting by ascending(the default) so 0 appears at the top 
		#"-" in priority means descending so we sort from bottom up in the model (high, med,low)
	all_tasks = Task.objects.all().order_by("completed", "-priority")	 	
	#Stores the time 
	today = timezone.now().date()
	#Todays date minus 7 days 
	week_ago = timezone.now() - timedelta(days=7)

	#Filter all tasks that are marked as false and give the number.
	remaining = Task.objects.filter(completed=False).count()
	
	#Filter all tasks that have a "completed" property value of true
		#Get the Complete at value from the tasks. 
			#Is the completed at value greater or equal to the value from "week_ago"
			#E.G TODAYS DATE = 14
			#	 Completed At = 7 
			#	 Week_ago = 14 - 7 = 7 
			# Is completed at greater or equal to a week ago? Yes its equal, include it.
	completed_this_week = Task.objects.filter(completed=True, completed_at__gte=week_ago).count()
	#Is the completed false, is the due date property less than Today
	#Today = 10
	#Due date is 4 
	#due date is less than today, inclue it
	overdue = Task.objects.filter(completed=False, due_date__lt=today).count()

	total_ever = Task.objects.count()
	total_incomplete = Task.objects.filter(completed=False).count()


	#Ternary Operators (Yoda Speak) read it backwards
		#251 is the stroke of the circle 
			#completed this week divided by remaining tasks multiplied by 251 to give us the offset px fill circles
			#True condition on left, false condition on right. Look for the "if"
	completed_offset = 251 - (completed_this_week / remaining * 251) if remaining > 0 else 251
	overdue_offset = (overdue / remaining * 251 ) if remaining > 0 else 0


	#Pass six pieces of data to the template, what to reference them as first and their actual values second
	return render(request, "tasks/task_list.html", {
		"all_tasks": all_tasks,
		"remaining" : remaining,
		"completed_this_week" : completed_this_week,
		"overdue" : overdue,
		"completed_offset" : completed_offset,
		"overdue_offset" : overdue_offset

	})
 

	
def task_create(request):
	#Map a variable to each field in the form
	#Square brackets are the HTML element names of the form.
	#"Take whatever is in the 'BODY'/'TITLE input field and map it to this variable
	if request.method == "POST":
		title = request.POST["title"]
		body = request.POST.get("body", "")
		priority = request.POST.get("priority", "medium")
		due_date = request.POST.get("due_date") or None
		#Map the form variables to the model variables 
			#If model item was ticketTitle, it would read ticketTitle=title
				#The first variable refers to the model, the second the form input variable
		new_task = Task(title=title, body=body, priority=priority, due_date=due_date)
		new_task.save()
	return redirect("/tasks/")

	
def task_complete(request, task_id):				#Task_id comes from button in browswer 
	task = Task.objects.get(id=task_id)				#Fetch task from DB pass in task_id. 
	task.completed = True							#Update completed field
	task.completed_at = timezone.now()				#Update completed_at
	task.save()										#Save to DB
	return redirect("/tasks/")						#Redirect to tasks page

def task_delete(request, task_id):
	deleteTask = Task.objects.get(id=task_id)
	deleteTask.delete()
	return redirect("/tasks/")

