# Data Handling libraries
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
# Alpha miner imports
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

from .models import EventLog


# Process discovery algorithms

# Alpha Miner


def discovery_alpha_miner(event_log_name, process_model_name):
    """Function to discover a process model using alpha miner"""
    event_log = None
    event_log_path = None
    log = None

    event_log = EventLog.objects.get(event_log_name=event_log_name)
    event_log_path = event_log.event_log_file
    log = xes_importer.apply("media/"+str(event_log_path))

    if event_log is None or event_log_path is None or log is None:
        return False
    else:
        # Need to add more controls
        net, initial_marking, final_marking = alpha_miner.apply(log)
        gviz = pn_visualizer.apply(net, initial_marking, final_marking)
        pn_visualizer.save(gviz, output_file_path="media/exported_pngs/" + process_model_name +
                                                  ".png")
        pnml_exporter.apply(net, initial_marking, "media/process_models/" + process_model_name + ".pnml")
        return True

# Inductive Miner


# Heuristic Miner
