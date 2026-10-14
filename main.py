import sys; sys.path.insert(0, "src")
import numpy as np, matplotlib.pyplot as plt
from components import load_components
from fmea import DEFAULT_FMEA
from architecture import ARCHITECTURES, propagate
from reliability import analytical, monte_carlo

comps = load_components("data/component_parameters.csv")

print(DEFAULT_FMEA.generate_report())

print("ANALYTICAL FAILURE PROBABILITY")
print(f"{'t (h)':>7}" + "".join(f"{a:>18}" for a in ARCHITECTURES))
for t in (1, 5, 10, 100):
    print(f"{t:>7}" + "".join(f"{analytical(a, comps, t):>18.3e}" for a in ARCHITECTURES))

T, N = 100, 100_000
print(f"\nMONTE CARLO ({N:,} missions of {T} h)")
for a in ARCHITECTURES:
    k, p = monte_carlo(a, comps, T, N)
    print(f"{a:>16}: {k} failures  (MC p={p:.2e}, analytical p={analytical(a, comps, T):.2e})")

print("\nFAILURE PROPAGATION")
for label, f in [("Gen A fails", {"Generator_A"}),
                 ("Gen A fails + Relay B stuck", {"Generator_A", "Relay_B"}),
                 ("Gen A + Relay B + Controller fail", {"Generator_A", "Relay_B", "Controller"})]:
    print(f"\n[{label}]"); print("\n".join("  " + l for l in propagate(f)))

ts = np.linspace(0.1, 100, 200)
for a in ARCHITECTURES:
    plt.semilogy(ts, [analytical(a, comps, t) for t in ts], label=a)
plt.xlabel("Mission time (h)"); plt.ylabel("P(loss of essential power)")
plt.legend(); plt.grid(True, which="both", alpha=.3)
plt.savefig("reliability.png", dpi=150)