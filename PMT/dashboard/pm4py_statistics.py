from django.conf import settings
from models import EventLog

from pm4py.statistics.traces.generic.log import case_statistics


def calculate_numeric_statistics(event_log_id, items) -> dict:
    """Function that calculates different statistics available in pm4py"""
    statistics_results = {}
    # Fetch event_log_file
    selected_event_log = EventLog.objects.get(pk=event_log_id)
    selected_event_log_file = selected_event_log.event_log_file
    selected_event_log_path = settings.MEDIA_URL + selected_event_log_file

    # Calculate statistics based of whatever is in the array and put the results in a dictionary

    if settings.MEDIAN_CASE_DURATION in items:
        statistics_results["median_case_duration"] = calculate_median_case_duration(selected_event_log_path)

    # Return the dictionary

    return statistics_results


# Different functions of statistics items calculation

def calculate_median_case_duration(log):
    """Function to calculate the median case duration"""
    return median_case_duration := case_statistics.get_median_case_duration(log,
                                                                            parameters={
                                                                                case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"})
