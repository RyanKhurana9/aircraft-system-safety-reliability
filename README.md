# Aircraft System Safety & Reliability Framework

A Python framework for analysing redundancy and failure propagation in a
generic aircraft electrical power system, using FMEA, fault trees, and
reliability modelling.

## System under analysis

Generator A/B → Relay A/B → Bus A/B → Essential Bus → Flight-Critical Load,
with an optional battery backup path (Battery + Controller + 2 sensors).

All failure rates are illustrative assumptions (see
`data/component_parameters.csv`), not real aircraft data.

## Architectures compared

| Architecture     | Description                          |
|------------------|---------------------------------------|
| Single           | One generator, no redundancy          |
| Dual             | Two independent generator paths       |
| Dual + Battery   | Dual generators plus battery backup   |

## Methods

- **FMEA** — severity × occurrence × detection → RPN, ranked report
- **Fault tree** — AND/OR gate tree per architecture, exact analytical
  top-event probability
- **Monte Carlo** — 100,000 simulated missions per architecture, sampling
  exponential failure times, cross-checked against the analytical result
- **Failure propagation** — step-by-step trace of how a failure cascades
  (or is contained) through relays/redundancy/battery




## Usage

```bash
pip install -r requirements.txt
python main.py     # prints FMEA report, probability tables, propagation traces, saves reliability.png
pytest              # analytical vs Monte Carlo cross-checks, architecture ordering
```

## Limitations

- Constant failure rate (exponential) model only — no wear-out/bathtub curve
- Assumes component failures are independent; no common-cause failure modelling
- Battery modelled as binary healthy/not — no finite endurance window
- Example failure rates, not validated against real aircraft data

## Possible extensions

- Common-cause failure groups (e.g. shared bus fault)
- Battery endurance / time-limited backup
- Repairable components (MTTR, availability instead of pure reliability)
