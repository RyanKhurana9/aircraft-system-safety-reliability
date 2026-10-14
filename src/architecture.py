from fault_tree import Basic as B, AND, OR

def path(side):  # generator -> relay -> bus
    return OR(B(f"Generator_{side}"), B(f"Relay_{side}"), B(f"Bus_{side}"))

def battery_path():  # needs controller + at least one sensor to detect loss and connect
    return OR(B("Battery"), B("Controller"), AND(B("Sensor_A"), B("Sensor_B")))

ARCHITECTURES = {
    "Single":         lambda: path("A"),
    "Dual":           lambda: AND(path("A"), path("B")),
    "Dual + Battery": lambda: AND(path("A"), path("B"), battery_path()),
}

def build(name):
    tree = ARCHITECTURES[name]()   # top event: loss of essential power
    tree.validate()
    return tree

def propagate(failed: set[str]) -> list[str]:
    """Trace how failures propagate to the essential bus (Dual + Battery)."""
    log, ok = [], []
    for s in "AB":
        for c in (f"Generator_{s}", f"Relay_{s}", f"Bus_{s}"):
            if c in failed:
                log.append(f"{c} failed -> path {s} unavailable"); break
        else:
            log.append(f"Path {s} healthy -> essential bus supplied via {s}"); ok.append(s)
    if not ok:
        can_detect = "Controller" not in failed and not {"Sensor_A", "Sensor_B"} <= failed
        if not can_detect:
            log.append("Loss undetected / cannot command battery (controller or both sensors down)")
        elif "Battery" in failed:
            log.append("Battery failed -> no backup")
        else:
            log.append("Controller connects battery -> essential bus supplied by battery"); ok.append("BAT")
    log.append("RESULT: essential load " + ("POWERED" if ok else "LOST"))
    return log