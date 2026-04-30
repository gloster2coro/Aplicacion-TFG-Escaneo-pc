"""
System restore point management.
On Windows uses PowerShell Checkpoint-Computer. On Linux records logically to DB.
"""
import platform
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any

IS_WINDOWS = platform.system().lower() == "windows"


def create_restore_point(description: str, point_type: str = "MODIFY_SETTINGS") -> Dict[str, Any]:
    """
    Creates a system restore point.
    point_type: APPLICATION_INSTALL, APPLICATION_UNINSTALL, DEVICE_DRIVER_INSTALL, MODIFY_SETTINGS, CANCELLED_OPERATION
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    if IS_WINDOWS:
        try:
            # Enable system restore first (requires admin)
            subprocess.run(
                ["powershell", "-Command", "Enable-ComputerRestore -Drive 'C:\\'"],
                capture_output=True, timeout=30
            )
            result = subprocess.run(
                [
                    "powershell", "-Command",
                    f"Checkpoint-Computer -Description '{description}' -RestorePointType '{point_type}'"
                ],
                capture_output=True, text=True, timeout=60
            )
            return {
                "success": result.returncode == 0,
                "description": description,
                "point_type": point_type,
                "timestamp": timestamp,
                "output": result.stdout or result.stderr,
                "simulated": False,
                "command": f"Checkpoint-Computer -Description '{description}' -RestorePointType '{point_type}'",
            }
        except Exception as e:
            return {
                "success": False,
                "description": description,
                "point_type": point_type,
                "timestamp": timestamp,
                "error": str(e),
                "simulated": False,
            }

    # Simulated for non-Windows environment
    return {
        "success": True,
        "description": description,
        "point_type": point_type,
        "timestamp": timestamp,
        "simulated": True,
        "command": f"Checkpoint-Computer -Description '{description}' -RestorePointType '{point_type}'",
        "note": "Simulado. Requiere Windows con permisos admin para ejecutarse realmente.",
    }
