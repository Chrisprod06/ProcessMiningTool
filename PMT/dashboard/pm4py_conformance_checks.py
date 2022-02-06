import os

from django.conf import settings

from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri_net.importer import importer as pnml_importer

from .models import EventLog


def perform_conformance_checks(
        conformance_checks, process_model_name, event_log_name
) -> dict:
    """Function to handle conformance checks"""
    conformance_checks_results = {}
    if settings.TOKEN_REPLAY in conformance_checks:
        conformance_checks_results["token_replay_result"] = token_replay_check(
            process_model_name, event_log_name
        )
    return conformance_checks_results


def token_replay_check(process_model, event_log) -> list:
    """Function to perform token base replay conformance check"""
    # Import process model
    process_model_file = process_model.process_model_file
    net, initial_marking, final_marking = pnml_importer.apply(process_model_file)
    # Import event log
    selected_event_log = EventLog.objects.get(pk=event_log.event_log_id)
    selected_event_log_file = selected_event_log.event_log_file
    selected_event_log_path = "media/" + str(selected_event_log_file)

    # Import xes file
    event_log_file_object = xes_importer.apply(selected_event_log_path)
    return token_replay.apply(
        event_log_file_object, net, initial_marking, final_marking
    )
