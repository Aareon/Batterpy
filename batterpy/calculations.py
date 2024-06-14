from typing import List, Dict

def calculate_battery_health(battery_info: Dict[str, str]) -> float:
    """Calculate the battery health percentage."""
    design_capacity = int(battery_info.get('DesignCapacity', 0))
    full_charge_capacity = int(battery_info.get('FullChargeCapacity', 0))
    if design_capacity == 0:
        return 0.0
    return (full_charge_capacity / design_capacity) * 100

def calculate_battery_degradation(battery_info: Dict[str, str]) -> float:
    """Calculate the battery degradation percentage."""
    design_capacity = int(battery_info.get('DesignCapacity', 0))
    full_charge_capacity = int(battery_info.get('FullChargeCapacity', 0))
    if design_capacity == 0:
        return 0.0
    return ((design_capacity - full_charge_capacity) / design_capacity) * 100

def calculate_cycle_count_over_time(recent_usage: List[Dict[str, str]]) -> List[int]:
    """Calculate the cycle count over time."""
    return [int(entry.get('CycleCount', 0)) for entry in recent_usage]

def calculate_discharge_rate(recent_usage: List[Dict[str, str]]) -> List[float]:
    """Calculate the discharge rate over time."""
    return [int(entry['Discharge']) / int(entry['Duration']) for entry in recent_usage if 'Discharge' in entry and 'Duration' in entry]

def calculate_historical_health(recent_usage: List[Dict[str, str]], design_capacity: int) -> List[float]:
    """Calculate the historical battery health over time."""
    return [(int(entry['FullChargeCapacity']) / design_capacity) * 100 for entry in recent_usage if 'FullChargeCapacity' in entry]

def calculate_average_discharge_rate(recent_usage: List[Dict[str, str]]) -> float:
    """Calculate the average discharge rate."""
    discharge_rates = calculate_discharge_rate(recent_usage)
    return sum(discharge_rates) / len(discharge_rates) if discharge_rates else 0.0

def count_charge_discharge_cycles(recent_usage: List[Dict[str, str]]) -> int:
    """Count the number of charge and discharge cycles."""
    cycles = 0
    last_charge = None
    for entry in recent_usage:
        charge = int(entry.get('ChargeCapacity', 0))
        if last_charge is not None and charge < last_charge:
            cycles += 1
        last_charge = charge
    return cycles

def estimate_time_to_full_charge(current_capacity: int, full_charge_capacity: int, charge_rate: float) -> float:
    """Estimate the time to full charge based on current capacity and charge rate."""
    if charge_rate == 0:
        return float('inf')
    return (full_charge_capacity - current_capacity) / charge_rate

def estimate_time_to_empty(current_capacity: int, discharge_rate: float) -> float:
    """Estimate the time to empty based on current capacity and discharge rate."""
    if discharge_rate == 0:
        return float('inf')
    return current_capacity / discharge_rate

def calculate_energy_consumption(recent_usage: List[Dict[str, str]]) -> List[float]:
    energy_consumption = []
    previous_capacity = None
    
    for entry in recent_usage:
        if previous_capacity is not None:
            consumption = previous_capacity - int(entry['ChargeCapacity'])
            energy_consumption.append(consumption)
        previous_capacity = int(entry['ChargeCapacity'])
    
    return energy_consumption

def calculate_charge_discharge_efficiency(recent_usage: List[Dict[str, str]]) -> List[float]:
    """Calculate the charge/discharge efficiency."""
    efficiency = []
    for entry in recent_usage:
        charge = int(entry.get('ChargeCapacity', 0))
        discharge = int(entry.get('Discharge', 0))
        if charge > 0:
            efficiency.append((charge - discharge) / charge * 100)
    return efficiency
