This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information. My participant ID in the challenge was: CC-VOL1-37.

# How to run this project

## Prerequisites

* Docker

## Commands to run


```bash
git clone https://github.com/Asqiir/relaxdays-hackathon-capacitated-vehicle-routing-problem.git
cd relaxdays-hackathon-capacitated-vehicle-routing-problem
docker build -t cvrp .
docker run cvrp <path_to_graph_as_json>
```

`<path_to_graph_as_json>` can be an absolute or relative path to a json file that contains a graph as shown in the task.


# Idea

The idea was using branch-and-bound. In every iteration (a `Tasse`, don't ask) a decision is taken: either the next package is added to any of the already existing `Fahrt`en or a new one is created.