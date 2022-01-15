from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import EventLogForm
from .models import EventLog


# Create your views here.


@login_required(login_url="/accounts/login")
def index(request):
    """Function that renders dashboard homepage"""
    return render(request, "dashboard/index.html")


@login_required(login_url="/accounts/login")
def process_discovery(request):
    """Function for process discovery """
    return render(request, "dashboard/process_discovery.html")


@login_required(login_url="/accounts/login")
def event_logs(request):
    """Function for event logs management"""
    logs = EventLog.objects.all()
    # Initialize dictionary which will hold data to send to template
    context={}
    if request.method == "POST":
        form = EventLogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/event_logs")
    else:
        form = EventLogForm()

    return render(request, "dashboard/event_logs.html", {"form": form, "event_logs": logs})


@login_required(login_url="/accounts/login")
def delete_event_log(request, pk):
    """Function to handle deletion of event logs"""
    if request.method == "POST":
        event_log = EventLog.objects.get(pk=pk)
        event_log.delete()
    return redirect("/event_logs")


@login_required(login_url="/accounts/modify")
def modify_event_log(request, pk):
    """Function to handle modification of event logs"""
    if request.method == "POST":
        event_log = EventLog.objects.get(pk=pk)
        form = EventLogForm(request.POST, request.Files, instance=event_log)
