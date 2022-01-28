from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from . import discovery_algorithms
from .forms import EventLogForm, ProcessModelForm, DiscoverProcessModelForm
from .models import EventLog, ProcessModel

from .discovery_algorithms import petri_net_discovery


@login_required(login_url="/accounts/login")
def index(request):
    """Function that renders dashboard homepage"""
    return render(request, "dashboard/index.html")


@login_required(login_url="/accounts/login")
def process_discovery(request):
    """Function for process discovery"""
    process_models = ProcessModel.objects.all()
    template = "dashboard/process_discovery.html"
    redirect_url = "/process_discovery"
    selected_process_model = None
    context = {}
    if request.method == "POST":
        discover_process_form = DiscoverProcessModelForm(request.POST)  # Get form model instance
        if "submitDiscover" in request.POST:  # Discovery algorithms to produce process model file and png
            if discover_process_form.is_valid():
                new_process_model = discover_process_form.save(
                    commit=False)  # create new model instance but don't save it
                # Get user details from form
                logfile = str(new_process_model.process_model_log_name)
                process_model_name = new_process_model.process_model_name
                discovery_algorithm = new_process_model.process_model_algorithm
                # Apply algorithm based on user selection and update model fields
                if discovery_algorithm == settings.ALPHA_MINER:
                    if discovery_algorithms.petri_net_discovery(logfile, process_model_name, settings.ALPHA_MINER):
                        messages.success(request, "Process Model discovered successfully!")
                    else:
                        messages.error(request, "Something went wrong! Please try again.")
                        redirect(redirect_url)
                elif discovery_algorithm == settings.INDUCTIVE_MINER:
                    if discovery_algorithms.petri_net_discovery(logfile, process_model_name, settings.INDUCTIVE_MINER):
                        messages.success(request, "Process Model discovered successfully!")
                    else:
                        messages.error(request, "Something went wrong! Please try again.")
                        redirect(redirect_url)
                new_process_model.process_model_file = "process_models/" + process_model_name + ".pnml"
                new_process_model.process_model_image = "exported_pngs/" + process_model_name + ".png"
                # Save the process model
                new_process_model.save()
                discover_process_form.save_m2m()
                return redirect(redirect_url)
        if "submitRender" in request.POST:  # Get selected process model and return it
            process_model_id = request.POST["process_model_id"]
            selected_process_model = ProcessModel.objects.get(pk=process_model_id)
    else:
        discover_process_form = DiscoverProcessModelForm()
    context["discover_process_form"] = discover_process_form
    context["process_models"] = process_models
    if selected_process_model is not None:
        context["selected_process_model"] = selected_process_model
    return render(request, template, context)


@login_required(login_url="/accounts/login")
def view_process_models(request):
    """Function that renders view processes"""
    redirect_url = "/view_process_models"
    template = "dashboard/view_process_models.html"
    context = {}
    process_models = ProcessModel.objects.all()
    if request.method == "POST":
        form = ProcessModelForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
                messages.success(request, "Process Model added successfully!")
            else:
                messages.error(request, "Something went wrong! Please try again!")
            return redirect(redirect_url)
    else:
        form = ProcessModelForm()
    context["form"] = form
    context["process_models"] = process_models
    return render(request, template, context)


@login_required(login_url="/accounts/login")
def delete_process_model(request, pk):
    """Function to handle deletion of event logs"""
    redirect_url = "/view_process_models"
    if request.method == "POST":
        process_model = ProcessModel.objects.get(pk=pk)
        if process_model is None:
            messages.error(request, "Process Model not found!")
        else:
            process_model.delete()
            messages.success(request, "Process Model deleted successfully!")
    return redirect(redirect_url)


@login_required(login_url="/accounts/login")
def event_logs(request):
    """Function for event logs management"""
    logs = EventLog.objects.all()
    template = "dashboard/event_logs.html"
    context = {}
    if request.method == "POST":
        form = EventLogForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
                messages.success(request, "Event log added successfully!")
            else:
                messages.error(request, "Something went wrong! Please try again.")

            return redirect("/event_logs")
    else:
        form = EventLogForm()

    # Add items to context
    context["form"] = form
    context["event_logs"] = logs
    return render(request, template, context)


@login_required(login_url="/accounts/login")
def delete_event_log(request, pk):
    """Function to handle deletion of event logs"""
    redirect_page = "/event_logs"
    if request.method == "POST":
        event_log = EventLog.objects.get(pk=pk)
        if event_log is None:
            messages.error(request, "Event Log not found!")
        else:
            event_log.delete()
            messages.success(request, "Event Log deleted successfully!")
    return redirect(redirect_page)
