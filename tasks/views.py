from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Task



def task_list(request):
	#Fetches every task from the DB and sorts it so incomplete comes first and higher priority tasks appear before lower
		#Completed is boolean in the modal (0 is false, 1 is true) we are sorting by ascending(the default) so 0 appears at the top 
		#"-" in priority means descending so we sort from bottom up in the model (high, med,low)
	all_tasks = Task.objects.filter(status__in=["notStarted", "inProgress"]).order_by("status", "-priority")
	completed_tasks = Task.objects.filter(status="completed")

	completed =  Task.objects.filter(status="completed").count()
	inProgress = Task.objects.filter(status="inProgress").count()
	notStarted = Task.objects.filter(status="notStarted").count()
	today = timezone.now().date()

	total = notStarted + inProgress + completed
	


	
	completed_offset = 251 - (completed / total * 251) if total > 0 else 251
	inProgress_offset = 251 - (inProgress / total * 251) if total > 0 else 251
	notStarted_offset = 251 - (notStarted / total * 251) if total > 0 else 251


	#Pass pieces of data to the template, what to reference them as first and their actual values second (Context)
	return render(request, "tasks/task_list.html", {
		"all_tasks": all_tasks,
		"completed" : completed,
		"completed_tasks" : completed_tasks,
		"inProgress" : inProgress,
		"notStarted" : notStarted,
		"completed_offset" : completed_offset,
		"inProgress_offset" : inProgress_offset,
		"notStarted_offset" : notStarted_offset,
		"today" : today
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
		category = request.POST.get("category")
		status = request.POST.get("status")
		#Map the form variables to the model variables 
			#If model item was ticketTitle, it would read ticketTitle=title
				#The first variable refers to the model, the second the form input variable
		new_task = Task(title=title, body=body, priority=priority, due_date=due_date, category=category, status=status)
		new_task.save()
	return redirect("/tasks/")

	
def task_status(request, task_id):				    #Task_id comes from button in browswer 
	task = Task.objects.get(id=task_id)				#Fetch task from DB pass in task_id. 
	if task.status == "notStarted":					
		task.status = "inProgress"					#If block for changing task status
	elif task.status == "inProgress":
		task.status = "completed"										
		task.completed_at = timezone.now()	        #Update completed_at
					
	task.save()										#Save to DB
	return redirect("/tasks/")						#Redirect to tasks page



def task_all(request):
	tasks = Task.objects.filter(status__in=["notStarted", "inProgress"])
	return render (request, "tasks/task_all.html", {"all_tasks" : tasks})

def task_allCompleted(request):
	tasks = Task.objects.filter(status="completed")
	return render (request, "tasks/task_allCompleted.html", {"completed_tasks" : tasks})

def task_filter(request):		#Key in URL (HTML) has to match what you're reading in the view. "?category=gym" category is the key value is gym
	taskcategory = request.GET.get("category", "all")  #first GET is Django get method for reading from URL and mapping key-pairs. Second get is python reading the key-pairs
	if taskcategory == "all":
		tasks = Task.objects.filter(status__in=["notStarted", "inProgress"]) #If there is no category selected(all in URL) display not started and in prog tasks
	else:
		tasks = Task.objects.filter(category=taskcategory, status__in=["notStarted", "inProgress"]) # Filter all tasks where the model category matches the taskcategory variable. and status matches
	return render(request, "tasks/partials/task_grid.html", {"all_tasks" : tasks}) #Only returning a fragment of the HTML from HTMX, just drop the task grid without reloading anything else 

def task_delete(request, task_id):
    deleteTask = Task.objects.get(id=task_id)
    deleteTask.delete()
    next_url = request.POST.get("next", "/tasks/") # python .get safely read the value by key (/tasks/completed/ is the value of next in the HTML) fall back to /tasks/ if no "next" key
    return redirect(next_url)

def task_edit(request, task_id):
	editTask = Task.objects.get(id=task_id)
	editTask.title = request.POST.get("title")
	editTask.body = request.POST.get("body")
	editTask.due_date = request.POST.get("due_date")
	editTask.status = request.POST.get("status")
	editTask.category = request.POST.get("category")
	editTask.priority = request.POST.get("priority")
	editTask.save()
	return redirect ("/tasks/")
