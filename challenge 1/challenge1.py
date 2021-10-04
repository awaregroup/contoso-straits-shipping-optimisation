from typing import List
from azure.quantum import Workspace
from azure.quantum.optimization import ParallelTempering
from azure.quantum.optimization import Problem, ProblemType, Term

workspace = Workspace (
    subscription_id = "",
    resource_group = "",
    name = "",
    location = ""
    )

#create your list of terms
terms: List[Term] = []

#create your problem
problem = Problem()

#Solve your problem
solver=ParallelTempering()

