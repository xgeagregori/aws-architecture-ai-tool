from diagrams import Diagram
from typing import List, Tuple
import importlib
from references import DIAGRAMS_REFERENCES
from nltk import edit_distance


def find_service_reference(service: str) -> Tuple[str, str]:
    min_distance = 100
    closest_match = "No reference found"
    for category in DIAGRAMS_REFERENCES:
        for reference in DIAGRAMS_REFERENCES[category]:
            dist = edit_distance(service.lower(), reference.lower())
            if dist < min_distance:
                min_distance = dist
                closest_match = f"diagrams.{category}", reference
    return closest_match


def generate_diagram(services_list: List[str]):
    module_references = []
    for service in services_list:
        service_reference = find_service_reference(service)
        module_references.append(service_reference)

    nodes = []
    for reference in module_references:
        module = importlib.import_module(reference[0])
        Node = getattr(module, reference[1])
        nodes.append(Node)

    graph_attr = {
        "bgcolor": "transparent"
    }
    with Diagram("", outformat="png", show=False, filename="/tmp/diagram", direction="TB", graph_attr=graph_attr):
        for index, Node in enumerate(nodes):
            Node(module_references[index][1])

    return "File saved to diagram.png"