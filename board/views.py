from django.shortcuts import render, redirect
from .models import Category, Task, Success_task
from django.contrib.auth.models import User
# Create your views here.

def home(request):
	if request.user.is_authenticated:
		return redirect("/board/")
	return redirect("/accounts/login/")

def board(request):
	if not request.user.is_authenticated:
		return redirect("/accounts/login/")


	success_task = Success_task.objects.filter(user=request.user)
	all_task = Task.objects.all()
	user_stats = []
	user_success = {}
	user_not_success = {}
	for cat in Category.objects.all():
		success_task_cat = success_task.filter(task__category=cat).distinct()
		all_task_cat = all_task.filter(category=cat)
		if success_task_cat.count() > 0:
			user_success[cat.name] = success_task_cat

		user_not_success[cat.name] = []
		for task in all_task_cat:
			if not task.id in [task.id  for task in success_task_cat]:
				user_not_success[cat.name].append(task)

		if len(user_not_success[cat.name]) == 0:
			del user_not_success[cat.name]


		
		user_stats.append({
			"category": cat.name, 
			"success": success_task_cat.count(), 
			"all":all_task_cat.count(), 
			"percent": int(success_task_cat.count()/all_task_cat.count()*100)
		})

	return render(request, "board.html", {"user_stats": user_stats, "user_success": user_success, "user_not_success": user_not_success})


def rating(request):
	if not request.user.is_authenticated:
		return redirect("/accounts/login/")

	rating = []
	category = False
	if request.GET.get('c') != None:
		category = Category.objects.get(id=request.GET.get('c'))
		
	for usr in User.objects.all():
		if category:
			count = Success_task.objects.filter(task__category=category, user=usr).distinct().count()
		else:
			count = Success_task.objects.filter(user=usr).distinct().count()
		if usr == request.user:
			pos = {"count": count, "user":usr}
		rating.append({"count": count, "user":usr})

	rating.sort(key=lambda x: x["count"], reverse=True)
	pos = rating.index(pos)+1
	for i in range(len(rating)):
		rating[i]["pos"] = i+1

	category_name = "Нет" if not category else category
	return render(request, "rating.html", {"pos": pos, "rating": rating, "category":Category.objects.all(), "category_name": category_name})