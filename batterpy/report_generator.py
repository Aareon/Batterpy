import xml.etree.ElementTree as ET
import subprocess
import pathlib
import tempfile
from loguru import logger
from typing import List, Dict, Optional

def generate_battery_report() -> pathlib.Path:
    """Generate the battery report using a PowerShell script and return the report path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
        report_path = pathlib.Path(temp_file.name)
        logger.info(f"Temporary report path: {report_path}")

    script_path = pathlib.Path(__file__).parent.parent / 'Battery-Check.ps1'
    logger.debug(f"Running {script_path} to generate battery report at {report_path}")
    try:
        subprocess.run(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script_path), '-HideConsole', '-ReportPath', str(report_path)],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Prevent the PowerShell window from opening
        )
        logger.info(f"Battery report generated at {report_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error generating battery report: {e}")
    except FileNotFoundError as e:
        logger.error(f"PowerShell script not found: {e}")
    
    return report_path

def parse_xml(file_path: str) -> Optional[ET.Element]:
    """Load the XML file and return the root element."""
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except Exception as e:
        logger.error(f"Error loading XML file: {e}")
        return None

def extract_text_from_element(element, tag: str, ns: str) -> str:
    """Extract text from a specific tag within an element."""
    child = element.find(f'{ns}{tag}')
    return child.text if child is not None else ""

def get_report_information(root: ET.Element, ns: str) -> Dict[str, str]:
    """Extract report information from the XML."""
    report_info = root.find(f'{ns}ReportInformation')
    if report_info is None:
        return {}
    info = {
        'ReportGuid': extract_text_from_element(report_info, 'ReportGuid', ns),
        'ReportVersion': extract_text_from_element(report_info, 'ReportVersion', ns),
        'ScanTime': extract_text_from_element(report_info, 'ScanTime', ns),
        'LocalScanTime': extract_text_from_element(report_info, 'LocalScanTime', ns),
        'ReportStartTime': extract_text_from_element(report_info, 'ReportStartTime', ns),
        'LocalReportStartTime': extract_text_from_element(report_info, 'LocalReportStartTime', ns),
        'ReportDuration': extract_text_from_element(report_info, 'ReportDuration', ns),
        'UtcOffset': extract_text_from_element(report_info, 'UtcOffset', ns),
    }
    return info

def get_system_information(root: ET.Element, ns: str) -> Dict[str, str]:
    """Extract system information from the XML."""
    system_info = root.find(f'{ns}SystemInformation')
    if system_info is None:
        return {}
    info = {
        'ComputerName': extract_text_from_element(system_info, 'ComputerName', ns),
        'SystemManufacturer': extract_text_from_element(system_info, 'SystemManufacturer', ns),
        'SystemProductName': extract_text_from_element(system_info, 'SystemProductName', ns),
        'BIOSDate': extract_text_from_element(system_info, 'BIOSDate', ns),
        'BIOSVersion': extract_text_from_element(system_info, 'BIOSVersion', ns),
        'OSBuild': extract_text_from_element(system_info, 'OSBuild', ns),
        'PlatformRole': extract_text_from_element(system_info, 'PlatformRole', ns),
        'ConnectedStandby': extract_text_from_element(system_info, 'ConnectedStandby', ns),
    }
    return info

def get_battery_information(root: ET.Element, ns: str) -> List[Dict[str, str]]:
    """Extract battery information from the XML."""
    batteries = root.find(f'{ns}Batteries')
    battery_list = []
    if batteries is None:
        return battery_list
    for battery in batteries.findall(f'{ns}Battery'):
        info = {
            'Id': extract_text_from_element(battery, 'Id', ns),
            'Manufacturer': extract_text_from_element(battery, 'Manufacturer', ns),
            'SerialNumber': extract_text_from_element(battery, 'SerialNumber', ns),
            'ManufactureDate': extract_text_from_element(battery, 'ManufactureDate', ns),
            'Chemistry': extract_text_from_element(battery, 'Chemistry', ns),
            'LongTerm': extract_text_from_element(battery, 'LongTerm', ns),
            'RelativeCapacity': extract_text_from_element(battery, 'RelativeCapacity', ns),
            'DesignCapacity': extract_text_from_element(battery, 'DesignCapacity', ns),
            'FullChargeCapacity': extract_text_from_element(battery, 'FullChargeCapacity', ns),
            'CycleCount': extract_text_from_element(battery, 'CycleCount', ns),
        }
        battery_list.append(info)
    return battery_list

def get_recent_usage(root: ET.Element, ns: str) -> List[Dict[str, str]]:
    """Extract recent usage information from the XML."""
    recent_usage = root.find(f'{ns}RecentUsage')
    usage_list = []
    if recent_usage is None:
        return usage_list
    for entry in recent_usage.findall(f'{ns}UsageEntry'):
        info = {attr: entry.attrib[attr] for attr in entry.attrib}
        usage_list.append(info)
    return usage_list

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
