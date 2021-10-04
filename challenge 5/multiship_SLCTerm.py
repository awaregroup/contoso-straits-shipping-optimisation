from azure.quantum.optimization import (
    SlcTerm,
    Term,
    Problem,
    ProblemType,
    SubstochasticMonteCarlo,
)
from azure.quantum import Workspace
from azure.quantum.target.solvers import RangeSchedule
import numpy as np


def visualize_result(result, containers, ships):
    nb_ships = len(ships)
    try:
        config = result["configuration"]
        config = list(config.values())
        for ship, sub_config in enumerate(np.array_split(config, nb_ships)):
            shipWeight = 0
            for c, b in enumerate(sub_config):
                shipWeight = shipWeight + b * containers[c]
            print(
                f"Ship {ships[ship]}: \t"
                + "|".join(f"{b*containers[c]}" for c, b in enumerate(sub_config))
                + " - "
                + str(shipWeight)
            )
    except:
        print("No Configuration")
    try:
        print("Cost: {}".format(result["cost"]))
    except:
        print("No Cost")
    try:
        print("Parameters: {}".format(result["parameters"]))
    except:
        print("No Parameter")


def solve_problem(problem, s):
    try:
        # Optimize the problem
        Job = s.submit(problem)
        Job.wait_until_completed()
        duration = Job.details.end_execution_time - Job.details.begin_execution_time
        if Job.details.status == "Succeeded":
            visualize_result(Job.get_results(), container_weights * len(ships), ships)
            print("Execution duration: ", duration)
        else:
            print("\rJob ID", Job.id, "failed")
    except BaseException as e:
        print(e)

def calculate_equal_distribution(container_weights, num_ships):
    total_weight=0
    for c in range (len(container_weights)):
        total_weight += container_weights[c]
    eq_dis = total_weight /num_ships
    return eq_dis

def define_cost_terms(container_weights, num_ships, num_containers, eq_dis):
    terms = []
    
    return terms

def define_penalty_terms(container_weights, num_ships, num_containers):
    terms = []
    
    return terms

def main(container_weights, ships):
    # Copy the settings for your workspace below
    workspace = Workspace(
        subscription_id="",
        resource_group="",
        name="",
        location="",
    )

    num_ships = len(ships)
    num_containers = len(container_weights)

    eq_dis = calculate_equal_distribution(container_weights, num_ships)

    terms = define_cost_terms(container_weights, num_ships, num_containers, eq_dis) + define_penalty_terms(container_weights, num_ships, num_containers)


    num_terms = len(terms)
    problemName = f"Balancing {num_containers} containers between {num_ships} ships ({num_terms:,} terms)"
    problem = Problem(name=problemName, problem_type=ProblemType.pubo, terms=terms)
    solver = SubstochasticMonteCarlo(
        workspace,
        step_limit=1000,
        target_population=64,
        beta=RangeSchedule("linear", 0.1, 5),
        seed=42,
    )
    solve_problem(problem, solver)


if __name__ == "__main__":

    container_weights = [
        3,
        8,
        3,
        4,
        1,
        5,
        2,
        2,
        7,
        9,
        5,
        4,
        8,
        9,
        4,
        6,
        8,
        7,
        6,
        2,
        2,
        9,
        4,
        6,
        3,
        8,
        5,
        7,
        2,
        4,
        9,
        4,
    ]
    ships = ["A", "B", "C", "D", "E"]
    main(container_weights, ships)
