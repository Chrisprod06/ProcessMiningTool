from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import discovery_algorithms, pm4py_statistics
from .forms import (
    DiscoverProcessModelForm,
    EventLogForm,
    ProcessModelForm,
    SelectProcessModelForm,
    SelectEventLogForm,
)
from .models import EventLog, ProcessModel


@login_required(login_url="/accounts/login")
def index(request):
    """Function that renders dashboard homepage"""
    template = "dashboard/index.html"
    redirect_url = "/process_discovery"
    context = {}
    selected_process_model = None
    discover_process_form = DiscoverProcessModelForm()
    select_process_model_form = SelectProcessModelForm()
    upload_event_log_form = EventLogForm()
    upload_process_model_form = ProcessModelForm()
    select_event_log_form = SelectEventLogForm()
    if request.method == "POST":
        if (
                "submitDiscover" in request.POST
        ):  # Discovery algorithms to produce process model file and png
            discover_process_form = DiscoverProcessModelForm(
                request.POST
            )  # Get form model instance
            if discover_process_form.is_valid():
                new_process_model = discover_process_form.save(
                    commit=False
                )  # create new model instance but don't save it
                # Get user details from form
                logfile = str(new_process_model.process_model_log_name)
                process_model_name = new_process_model.process_model_name
                discovery_algorithm = new_process_model.process_model_algorithm
                # Apply algorithm based on user selection and update model fields
                if discovery_algorithm == settings.ALPHA_MINER:
                    if discovery_algorithms.petri_net_discovery(
                            logfile, process_model_name, settings.ALPHA_MINER
                    ):
                        messages.success(
                            request, "Process Model discovered successfully!"
                        )
                    else:
                        messages.error(
                            request, "Something went wrong! Please try again."
                        )
                        redirect(redirect_url)
                elif discovery_algorithm == settings.INDUCTIVE_MINER:
                    if discovery_algorithms.petri_net_discovery(
                            logfile, process_model_name, settings.INDUCTIVE_MINER
                    ):
                        messages.success(
                            request, "Process Model discovered successfully!"
                        )
                    else:
                        messages.error(
                            request, "Something went wrong! Please try again."
                        )
                        redirect(redirect_url)
                new_process_model.process_model_file = (
                        "process_models/" + process_model_name + ".pnml"
                )
                new_process_model.process_model_image = (
                        "exported_pngs/" + process_model_name + ".png"
                )
                # Save the process model
                new_process_model.save()
                discover_process_form.save_m2m()
                return redirect(redirect_url)
        if "submitVisualize" in request.POST:  # Get selected process model and return it
            select_process_model_form = SelectProcessModelForm(request.POST)
            if select_process_model_form.is_valid():
                selected_process_model = select_process_model_form.cleaned_data.get(
                    "process_model"
                )
                selected_process_model_id = selected_process_model.process_model_id
                return redirect("view_process_models/visualize/" + str(selected_process_model_id))
        if "submitUploadEventLog" in request.POST:
            upload_event_log_form = EventLogForm(request.POST, request.FILES)
            if upload_event_log_form.is_valid():
                if upload_event_log_form.save():
                    messages.success(request, "Event log added successfully!")
                else:
                    messages.error(request, "Something went wrong! Please try again.")
                return redirect("index")
        if "submitUploadProcessModel" in request.POST:
            upload_process_model_form = ProcessModelForm(request.POST, request.FILES)
            if upload_process_model_form.is_valid():
                if upload_process_model_form.save():
                    messages.success(request, "Process Model added successfully!")
                else:
                    messages.error(request, "Something went wrong! Please try again!")
                return redirect("")
        if "submitSelectEventLog" in request.POST:
            select_event_log_form = SelectEventLogForm(request.POST)
            if select_event_log_form.is_valid():
                selected_event_log = select_event_log_form.cleaned_data.get("event_log")
                selected_event_log_id = selected_event_log.event_log_id
                return redirect("view_statistics/performance_dashboard/" + str(selected_event_log_id))

    context["discover_process_form"] = discover_process_form
    context["select_process_model_form"] = select_process_model_form
    context["upload_event_log_form"] = upload_event_log_form
    context["upload_process_model_form"] = upload_process_model_form
    context["select_event_log_form"] = select_event_log_form

    return render(request, template, context)


@login_required(login_url="/accounts/login")
def view_process_models(request):
    """Function that renders view processes"""
    redirect_url = "/view_process_models"
    template = "dashboard/view_process_models.html"
    context = {}
    process_models = ProcessModel.objects.all()

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
def view_event_logs(request):
    """Function for event logs management"""
    logs = EventLog.objects.all()
    template = "dashboard/view_event_logs.html"
    context = {"event_logs": logs}

    # Add items to context
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


@login_required(login_url="/accounts/login")
def view_performance_dashboard(request, pk):
    """Function to calculate and present performance dashboard"""
    template = "dashboard/view_performance_dashboard.html"
    return render(request, template)


@login_required(login_url="/accounts/login")
def visualize_process_model(request, pk):
    """Function to handle process models visualization"""
    template = "dashboard/visualize_process_model.html"
    return render(request, template)
