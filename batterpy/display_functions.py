from loguru import logger
from typing import Dict, List

def display_report_information(info: Dict[str, str]):
    """Display report information."""
    logger.info("Report Information:")
    for key, value in info.items():
        logger.info(f"  {key}: {value}")

def display_system_information(info: Dict[str, str]):
    """Display system information."""
    logger.info("System Information:")
    for key, value in info.items():
        logger.info(f"  {key}: {value}")

def display_battery_information(batteries: List[Dict[str, str]], calculate_battery_health, calculate_battery_degradation):
    """Display battery information."""
    logger.info("Battery Information:")
    for battery in batteries:
        logger.info("  Battery:")
        for key, value in battery.items():
            logger.info(f"    {key}: {value}")
        health = calculate_battery_health(battery)
        degradation = calculate_battery_degradation(battery)
        logger.info(f"    Health: {health:.2f}%")
        logger.info(f"    Degradation: {degradation:.2f}%")

def display_recent_usage(usage: List[Dict[str, str]]):
    """Display recent usage information."""
    logger.info("Recent Usage:")
    for entry in usage:
        logger.info("  Entry:")
        for key, value in entry.items():
            logger.info(f"    {key}: {value}")
