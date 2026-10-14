import numpy as np
from architecture import build

def analytical(arch, comps, t):
    tree = build(arch)
    q = {n: c.unreliability(t) for n, c in comps.items()}
    return tree.prob(q)

def monte_carlo(arch, comps, t, n=100_000, seed=0):
    rng = np.random.default_rng(seed)
    tree = build(arch)
    # Sample each component's failure time ~ Exp(lambda); failed if time < mission length
    state = {name: rng.exponential(1 / c.failure_rate, n) < t for name, c in comps.items()}
    failures = int(tree.failed(state).sum())
    return failures, failures / n