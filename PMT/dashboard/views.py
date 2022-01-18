from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import EventLogForm, ProcessModelForm, DiscoverProcessModelForm, RenderProcessModelForm
from .models import EventLog, ProcessModel


@login_required(login_url="/accounts/login")
def index(request):
    """Function that renders dashboard homepage"""
    return render(request, "dashboard/index.html")


@login_required(login_url="/accounts/login")
def process_discovery(request):
    """Function for process discovery"""
    if request.method == "POST":
        discover_process_form = DiscoverProcessModelForm(request.POST)
        render_process_form = RenderProcessModelForm(request.POST)
        if "submitDiscover" in request.POST:
            if discover_process_form.is_valid():
                discover_process_form.save()
                return redirect("/process_discovery")
        if "submitRender" in request.POST:
            if render_process_form.is_valid():
                render_process_form.save()
                return redirect("/process_discovery")
    else:
        discover_process_form = DiscoverProcessModelForm()
        render_process_form = RenderProcessModelForm()

    return render(request, "dashboard/process_discovery.html", {"discover_process_form": discover_process_form,
                                                                "render_process_form": render_process_form})


@login_required(login_url="/accounts/login")
def view_process_models(request):
    """Function that renders view processes"""
    process_models = ProcessModel.objects.all()
    if request.method == "POST":
        form = ProcessModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/view_process_models")
    else:
        form = ProcessModelForm()
    return render(request, "dashboard/view_process_models.html", {"form": form, "process_models": process_models})


@login_required(login_url="/accounts/login")
def delete_process_model(request, pk):
    """Function to handle deletion of event logs"""
    if request.method == "POST":
        process_model = ProcessModel.objects.get(pk=pk)
        process_model.delete()
    return redirect("/view_process_models")


@login_required(login_url="/accounts/login")
def event_logs(request):
    """Function for event logs management"""
    logs = EventLog.objects.all()
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
