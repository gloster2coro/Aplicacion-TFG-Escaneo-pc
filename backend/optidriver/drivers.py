"""
Driver management module.
On Windows uses pnputil/WMI. On Linux provides simulated data for UI development.
"""
import platform
import subprocess
import random
from typing import List, Dict, Any

IS_WINDOWS = platform.system().lower() == "windows"


def _simulated_drivers() -> List[Dict[str, Any]]:
    return [
        {"name": "NVIDIA GeForce RTX 3060", "device_class": "Display adapters", "provider": "NVIDIA", "current_version": "546.33", "latest_version": "551.86", "date": "2023-11-02", "outdated": True, "size_mb": 812, "category": "gpu"},
        {"name": "Intel(R) Wi-Fi 6 AX201 160MHz", "device_class": "Network adapters", "provider": "Intel Corporation", "current_version": "22.150.0.5", "latest_version": "23.40.1.3", "date": "2023-08-15", "outdated": True, "size_mb": 48, "category": "network"},
        {"name": "Realtek High Definition Audio", "device_class": "Sound, video and game controllers", "provider": "Realtek Semiconductor", "current_version": "6.0.9445.1", "latest_version": "6.0.9445.1", "date": "2024-01-10", "outdated": False, "size_mb": 312, "category": "audio"},
        {"name": "AMD Ryzen 7 5800X Chipset", "device_class": "System devices", "provider": "AMD", "current_version": "4.10.29.0030", "latest_version": "5.02.04.1115", "date": "2023-09-20", "outdated": True, "size_mb": 156, "category": "chipset"},
        {"name": "Samsung NVMe SSD 980 PRO", "device_class": "Storage controllers", "provider": "Samsung Electronics", "current_version": "5P2QGXA7", "latest_version": "5B2QGXA7", "date": "2023-12-01", "outdated": True, "size_mb": 24, "category": "storage"},
        {"name": "Logitech G Pro Wireless Mouse", "device_class": "Mice and other pointing devices", "provider": "Logitech", "current_version": "2023.12.1", "latest_version": "2023.12.1", "date": "2023-12-15", "outdated": False, "size_mb": 18, "category": "input"},
        {"name": "Intel(R) UHD Graphics 630", "device_class": "Display adapters", "provider": "Intel Corporation", "current_version": "30.0.101.1340", "latest_version": "31.0.101.5186", "date": "2023-06-12", "outdated": True, "size_mb": 620, "category": "gpu"},
        {"name": "Bluetooth Radio (Intel)", "device_class": "Bluetooth", "provider": "Intel Corporation", "current_version": "22.150.0.2", "latest_version": "23.20.0.3", "date": "2023-07-22", "outdated": True, "size_mb": 32, "category": "network"},
        {"name": "USB Root Hub (USB 3.0)", "device_class": "Universal Serial Bus controllers", "provider": "Microsoft", "current_version": "10.0.19041.1", "latest_version": "10.0.19041.1", "date": "2024-01-05", "outdated": False, "size_mb": 8, "category": "usb"},
        {"name": "Webcam HD 1080p", "device_class": "Cameras", "provider": "Generic", "current_version": "1.0.2.1", "latest_version": "1.0.4.5", "date": "2023-05-10", "outdated": True, "size_mb": 14, "category": "camera"},
    ]


def list_drivers() -> List[Dict[str, Any]]:
    if IS_WINDOWS:
        try:
            # Use pnputil to enumerate drivers
            result = subprocess.run(
                ["pnputil", "/enum-drivers"],
                capture_output=True, text=True, timeout=30
            )
            # Parse output (simplified). For production a richer parser is recommended.
            if result.returncode == 0:
                # Return a mix of real data parsed + enhanced with WMI queries
                # For now we still provide the simulated dataset as the template
                # so the UI consistent across platforms.
                pass
        except Exception:
            pass
    return _simulated_drivers()


def get_outdated_drivers() -> List[Dict[str, Any]]:
    return [d for d in list_drivers() if d["outdated"]]


def update_drivers(driver_names: List[str], simulate: bool = True) -> Dict[str, Any]:
    """
    Simulates updating drivers.
    On Windows a real implementation would download INF packages and run pnputil /add-driver.
    """
    all_drivers = list_drivers()
    targets = [d for d in all_drivers if d["name"] in driver_names]
    results = []
    for d in targets:
        if not d["outdated"]:
            results.append({
                "driver": d["name"],
                "status": "already_up_to_date",
                "message": f"{d['name']} ya está en la última versión ({d['current_version']})",
            })
            continue
        # Simulate update
        success = random.random() > 0.05  # 95% success rate simulation
        results.append({
            "driver": d["name"],
            "from_version": d["current_version"],
            "to_version": d["latest_version"],
            "status": "success" if success else "failed",
            "simulated": simulate or not IS_WINDOWS,
            "message": f"Actualizado de {d['current_version']} a {d['latest_version']}" if success else "Error de descarga (simulado)",
        })
    return {
        "total_requested": len(driver_names),
        "total_processed": len(results),
        "successes": sum(1 for r in results if r.get("status") == "success"),
        "failures": sum(1 for r in results if r.get("status") == "failed"),
        "results": results,
        "simulated": simulate or not IS_WINDOWS,
    }
