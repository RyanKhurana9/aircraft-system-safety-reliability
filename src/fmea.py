from dataclasses import dataclass

@dataclass
class FailureMode:
    component: str; mode: str; cause: str; effect: str
    severity: int; occurrence: int; detection: int; mitigation: str
    @property
    def rpn(self): return self.severity * self.occurrence * self.detection

class FMEA:
    def __init__(self, modes): self.modes = modes

    def calculate_rpn(self):
        return sorted(((m, m.rpn) for m in self.modes), key=lambda x: -x[1])

    def high_risk_failures(self, threshold=60):
        return [m for m, r in self.calculate_rpn() if r >= threshold]

    def generate_report(self, threshold=60):
        lines = ["HIGH PRIORITY FAILURE MODES", ""]
        for i, m in enumerate(self.high_risk_failures(threshold), 1):
            lines += [f"{i}. {m.component}: {m.mode}",
                      f"   Cause: {m.cause}", f"   Effect: {m.effect}",
                      f"   Severity: {m.severity}  Occurrence: {m.occurrence}  "
                      f"Detection: {m.detection}  RPN: {m.rpn}",
                      f"   Mitigation: {m.mitigation}", ""]
        return "\n".join(lines)

FM = FailureMode
DEFAULT_FMEA = FMEA([
    FM("Generator_A", "Loss of output", "Bearing/winding failure", "Bus A unpowered; Gen B carries load", 8, 4, 2, "Redundant Generator B"),
    FM("Generator_B", "Loss of output", "Bearing/winding failure", "Bus B unpowered; Gen A carries load", 8, 4, 2, "Redundant Generator A"),
    FM("Relay_A", "Stuck open", "Contact welding/coil failure", "Path A unavailable; redundancy reduced", 8, 3, 6, "Periodic relay health test"),
    FM("Relay_B", "Stuck open", "Contact welding/coil failure", "Path B unavailable; redundancy reduced", 8, 3, 6, "Periodic relay health test"),
    FM("Bus_A", "Short/open circuit", "Insulation breakdown", "Path A lost", 9, 2, 3, "Bus protection, isolation"),
    FM("Bus_B", "Short/open circuit", "Insulation breakdown", "Path B lost", 9, 2, 3, "Bus protection, isolation"),
    FM("Battery", "Fails to supply", "Cell degradation", "No backup on dual loss", 7, 3, 7, "Scheduled capacity checks"),
    FM("Controller", "Fails to switch", "Software/hardware fault", "Battery not connected on dual loss", 9, 2, 5, "Watchdog, dual-lane design"),
    FM("Sensor_A", "Erroneous/no reading", "Drift or open circuit", "Degraded loss detection", 6, 3, 4, "Cross-check with Sensor B"),
    FM("Sensor_B", "Erroneous/no reading", "Drift or open circuit", "Degraded loss detection", 6, 3, 4, "Cross-check with Sensor A"),
])