from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import discovery_algorithms
from .forms import EventLogForm, ProcessModelForm, DiscoverProcessModelForm
from .models import EventLog, ProcessModel

from .discovery_algorithms import discovery_alpha_miner


@login_required(login_url="/accounts/login")
def index(request):
    """Function that renders dashboard homepage"""
    return render(request, "dashboard/index.html")


@login_required(login_url="/accounts/login")
def process_discovery(request):
    """Function for process discovery"""
    process_models = ProcessModel.objects.all()
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
                if discovery_algorithm == "alpha_miner":
                    discovery_algorithms.discovery_alpha_miner(logfile, process_model_name)
                    new_process_model.process_model_file = "process_models/" + process_model_name + ".pnml"
                    new_process_model.process_model_image = "exported_pngs/" + process_model_name + ".png"
                elif discovery_algorithm == "inductive_miner":
                    pass
                elif discovery_algorithm == "heuristic_miner":
                    pass

                # Save the process model
                new_process_model.save()
                discover_process_form.save_m2m()

                return redirect("/process_discovery")
        if "submitRender" in request.POST:  # Get selected process model and return it
            process_model_id = request.POST["process_model_id"]
            selected_process_model = ProcessModel.objects.get(pk=process_model_id)
            return render(request, "dashboard/process_discovery.html", {"discover_process_form": discover_process_form,
                                                                        "process_models": process_models,
                                                                        "selected_process_model": selected_process_model})
    else:
        discover_process_form = DiscoverProcessModelForm()

    return render(request, "dashboard/process_discovery.html", {"discover_process_form": discover_process_form,
                                                                "process_models": process_models})


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
