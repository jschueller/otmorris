%feature("docstring") OTMORRIS::MorrisExperimentGrid
"MorrisExperimentGrid builds experiments for the Morris method starting from full p-levels grid experiments.

Parameters
----------
levels : :py:class:`openturns.Indices`
    Number of levels for a regular grid
N : int
    Number of trajectories
bounds : :py:class:`openturns.Interval`, optional
    Bounds of the domain, by default it is defined on :math:`[0,1]^d`.

Examples
--------
>>> import openturns as ot
>>> import otmorris
>>> # Number of trajectories
>>> r = 10
>>> # Define a k-grid level (so delta = 1/(k-1))
>>> k = 5
>>> dim = 3
>>> experiment = otmorris.MorrisExperimentGrid([k] * dim, r)
>>> X = experiment.generate()
"

// ---------------------------------------------------------------------

%feature("docstring") OTMORRIS::MorrisExperimentGrid::getJumpStep
"Get the jump step,  specifying the number of levels for each factor that are increased/decreased for computing the
elementary effects. If not given, it is set to 1 for each factor.

Returns
-------
jumpStep : :py:class:`openturns.Indices`
    Number of levels for each factot that are increased/decreased for computating the EE.
"

// ---------------------------------------------------------------------

%feature("docstring") OTMORRIS::MorrisExperimentGrid::setJumpStep
"Set the jump step,  specifying the number of levels for each factor that are increased/decreased for computing the
elementary effects. If not given, it is set to 1 for each factor.


Parameters
----------
jumpStep : :py:class:`openturns.Indices`
    Number of levels for each factot that are increased/decreased for computating the EE.

Notes
-----
The final jump step contains only integers, so the parameter argument is converted into a list of integer thanks to the
floor operator.
"

// ---------------------------------------------------------------------
