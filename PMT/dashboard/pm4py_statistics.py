from django.conf import settings
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.objects.log.importer.xes import importer as xes_importer
from .models import EventLog


def calculate_numeric_statistics(event_log_id, items) -> dict:
    """Function that calculates different statistics available in pm4py"""
    statistics_results = {}
    # Find log file path
    selected_event_log = EventLog.objects.get(pk=event_log_id)
    selected_event_log_file = selected_event_log.event_log_file
    selected_event_log_path = "media/" + str(selected_event_log_file)

    # Import xes file
    event_log_file_object = xes_importer.apply(selected_event_log_path)

    if settings.MEDIAN_CASE_DURATION in items:
        statistics_results["median_case_duration"] = calculate_median_case_duration(
            event_log_file_object
        )

    # Return the dictionary

    return statistics_results


# Different functions of statistics items calculation


def calculate_median_case_duration(log):
    """Function to calculate the median case duration"""

    return case_statistics.get_all_casedurations(
        log,
        parameters={case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"},
    )
