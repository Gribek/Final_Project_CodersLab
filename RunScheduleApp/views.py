from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views import View
from datetime import datetime
from calendar import HTMLCalendar
from RunScheduleApp.forms import *


# Create your views here.


def get_user(request):
    current_user = request.user
    return current_user


class WorkoutPlanAdd(View):
    def get(self, request):
        form = WorkoutPlanForm()
        return render(request, 'RunScheduleApp/workout_plan_add.html', {'form': form})

    def post(self, request):
        new_workout_plan = WorkoutPlan()
        form = WorkoutPlanForm(request.POST, instance=new_workout_plan)
        if form.is_valid():
            form.instance.owner = get_user(request)
            # if form.instance.is_active == True:
            #     pass TODO(napisać funkcję deaktywującą inne plany)
            form.save()
            return HttpResponse('Dodano plan')
        return render(request, 'RunScheduleApp/workout_plan_add.html', {'form': form})


class WorkoutPlanView(View):
    def get(self, request, id):
        workout_plan = WorkoutPlan.objects.get(pk=id)
        if workout_plan.owner != get_user(request):
            raise PermissionDenied
        return render(request, "RunScheduleApp/workout_plan.html", {'workout_plan': workout_plan})


class DailyTrainingAdd(View):
    def get(self, request, id):
        workout_plan = WorkoutPlan.objects.get(pk=id)
        if workout_plan.owner != get_user(request):
            return HttpResponse('Nie możesz dodać treningu do nie swojego planu!')
        form = DailyTrainingForm(initial={'workout_plan': workout_plan.plan_name})
        return render(request, "RunScheduleApp/daily_training_add.html", {'form': form})

    def post(self, request, id):
        new_training = DailyTraining()
        form = DailyTrainingForm(request.POST, instance=new_training)
        if form.is_valid():
            workout = WorkoutPlan.objects.get(pk=id)
            form.instance.workout_plan = workout
            form.save()
            return redirect(f'/daily_training_add/{id}')
        # return HttpResponse('Not valid')
        return render(request, "RunScheduleApp/daily_training_add.html", {'form': form})


class CurrentWorkoutPlanView(View):
    def get(self, request):
        logged_user = get_user(request)
        if logged_user.is_anonymous == True:
            return redirect('/login')
        if not WorkoutPlan.objects.filter(owner=get_user(request)).filter(is_active=True).exists():
            return render(request, "RunScheduleApp/current_workout_plan.html", {'workout_plan': ''})
        workout_plan = WorkoutPlan.objects.filter(owner=get_user(request)).filter(is_active=True)[0]
        # trainings = workout_plan.dailytraining_set.all().order_by('day')
        # training_dict ={}
        # for training in trainings:
        #     training_dict.update({f'{training.day}': training.name()})
        plan_start_date = workout_plan.date_range.lower
        cal = WorkoutCalendar(workout_plan).formatmonth(plan_start_date.year, plan_start_date.month)
        return render(request, "RunScheduleApp/current_workout_plan.html",
                      {'workout_plan': workout_plan, 'calendar': mark_safe(cal)})


class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workout_plan):
        super(WorkoutCalendar, self).__init__()
        self.workout_plan = workout_plan

    def training_day_dict_get(self):
        self.trainings = self.workout_plan.dailytraining_set.all().order_by('day')
        self.training_dict = {}
        for training in self.trainings:
            self.training_dict.update({f'{training.day.day}': training.name()})
        return self.training_dict

    def formatday(self, day, weekday):
        self.training_dict_days = self.training_day_dict_get()
        """
        Return a day as a table cell.
        """
        if day == self.workout_plan.date_range.lower.day:
            return '<td bgcolor= "green" class="%s">%d</td>' % (self.cssclasses[weekday], day)
        if day == self.workout_plan.date_range.upper.day:
            return '<td bgcolor= "red" class="%s">%d</td>' % (self.cssclasses[weekday], day)
        if str(day) in self.training_dict_days:
            return '<td bgcolor= "pink" class="%s">%d<br>%s</td>' % (self.cssclasses[weekday], day, self.training_dict_days[str(day)])
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], day, day)