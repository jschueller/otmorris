import openturns as ot
from openturns.viewer import View
import otmorris

# Number of trajectories
r = 10
# Define experiments in [0,1]^20
# p-levels
p = 5
dim = 20
morris_experiment = otmorris.MorrisExperimentGrid([p] * dim, r)
bounds = ot.Interval(dim) # [0,1]^d
X = morris_experiment.generate()
f = ot.Function(otmorris.MorrisFunction())
Y = f(X)
# Evaluate Elementary effects (ee)
morris = otmorris.Morris(X, Y, bounds)
# Compute mu/sigma
mean = morris.getMeanAbsoluteElementaryEffects()
sigma = morris.getStandardDeviationElementaryEffects()
graph = morris.drawElementaryEffects(0)
View(graph).show()

