from diagrams import Diagram
from typing import Tuple
import importlib
from references import DIAGRAMS_REFERENCES
from nltk import edit_distance

architecture = "S3, Lambda, DynamoDB, Glue, Athena, SageMaker, QuickSight"

architecture_list = architecture.split(", ")
architecture_list_lowercase = [service.lower()
                               for service in architecture_list]


def find_service_reference(service: str) -> Tuple[str, str]:
    min_distance = 100
    closest_match = "No reference found"
    for category in DIAGRAMS_REFERENCES:
        for reference in DIAGRAMS_REFERENCES[category]:
            dist = edit_distance(service, reference.lower())
            if dist < min_distance:
                min_distance = dist
                closest_match = f"diagrams.{category}", reference
    return closest_match


module_references = []
for service in architecture_list_lowercase:
    service_reference = find_service_reference(service)
    module_references.append(service_reference)

nodes = []
for reference in module_references:
    print(reference)
    module = importlib.import_module(reference[0])
    Node = getattr(module, reference[1])
    nodes.append(Node)

graph_attr = {
    # "bgcolor": "transparent"
}
with Diagram("", show=False, filename="test", direction="TB", graph_attr=graph_attr):
    for index, Node in enumerate(nodes[:-1]):
        Node(module_references[index][1])