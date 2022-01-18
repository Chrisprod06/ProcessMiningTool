# Data Handling libraries
from pm4py.objects.log.importer.xes import importer as xes_importer
# Alpha miner imports
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# Process discovery algorithms

# Alpha Miner


def discovery_alpha_miner(logfile, process_model_name):
    """Function to discover a process model using alpha miner"""
    log = xes_importer.apply("/PMT/media/event_logs/" + logfile)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    petri_net_details = {
        "name": process_model_name,
        "net": net,
        "initial_marking": initial_marking,
        "final_marking": final_marking
    }

    return petri_net_details


def petri_net_export_png(petri_net_details):
    """Function to export petri net png in media/exported_pngs"""
    gviz = pn_visualizer.apply(petri_net_details.net, petri_net_details.initial_marking,
                               petri_net_details.final_marking)
    pn_visualizer.save(gviz, output_file_path="/PMT/media/exported_pngs")


def petri_net_export_pnml(petri_net_details, process_model_name):
    """Function to export petri net pnml file in media/process_models"""
    pnml_exporter.apply(petri_net_details.net, petri_net_details.initial_marking, process_model_name + ".pnml")


# Inductive Miner


# Heuristic Miner
