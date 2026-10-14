import sys; sys.path.insert(0, "src")
from component import load_components
from reliability import analytical, monte_carlo

comps = load_components("data/component_parameters.csv")

def test_ordering():
    s, d, b = (analytical(a, comps, 10) for a in ("Single", "Dual", "Dual + Battery"))
    assert s > d > b

def test_mc_matches_analytical():
    k, p = monte_carlo("Single", comps, 100, 200_000)
    assert abs(p - analytical("Single", comps, 100)) < 3e-3