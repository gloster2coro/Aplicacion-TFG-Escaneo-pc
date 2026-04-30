"""
Hardware detection module.
Uses psutil (cross-platform) and wmi/platform on Windows.
On Linux (dev environment) some Windows-specific queries return simulated data.
"""
import platform
import psutil
import socket
from typing import Dict, List, Any

IS_WINDOWS = platform.system().lower() == "windows"


def _safe(fn, default):
    try:
        return fn()
    except Exception:
        return default


def get_cpu_info() -> Dict[str, Any]:
    freq = psutil.cpu_freq()
    return {
        "name": platform.processor() or "Unknown CPU",
        "architecture": platform.machine(),
        "physical_cores": psutil.cpu_count(logical=False) or 0,
        "logical_cores": psutil.cpu_count(logical=True) or 0,
        "max_frequency_mhz": round(freq.max, 2) if freq else 0,
        "current_frequency_mhz": round(freq.current, 2) if freq else 0,
    }


def get_memory_info() -> Dict[str, Any]:
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "percent": mem.percent,
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_gb": round(swap.used / (1024**3), 2),
    }


def get_disk_info() -> List[Dict[str, Any]]:
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "filesystem": part.fstype,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent": usage.percent,
            })
        except PermissionError:
            continue
    return disks


def get_gpu_info() -> List[Dict[str, Any]]:
    """Best-effort GPU detection. Real data available on Windows via WMI."""
    if IS_WINDOWS:
        try:
            import wmi  # type: ignore
            c = wmi.WMI()
            gpus = []
            for gpu in c.Win32_VideoController():
                gpus.append({
                    "name": gpu.Name,
                    "driver_version": gpu.DriverVersion,
                    "memory_mb": round(int(gpu.AdapterRAM or 0) / (1024**2), 0) if gpu.AdapterRAM else 0,
                    "resolution": f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}" if gpu.CurrentHorizontalResolution else "N/A",
                })
            return gpus
        except Exception:
            pass
    # Simulated GPU info for non-Windows environments
    return [{
        "name": "NVIDIA GeForce RTX 3060 (simulado)",
        "driver_version": "546.33",
        "memory_mb": 12288,
        "resolution": "1920x1080",
        "note": "Datos simulados - se mostrarán datos reales al ejecutar en Windows",
    }]


def get_motherboard_info() -> Dict[str, Any]:
    if IS_WINDOWS:
        try:
            import wmi  # type: ignore
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                return {
                    "manufacturer": board.Manufacturer,
                    "product": board.Product,
                    "serial": board.SerialNumber,
                    "version": board.Version,
                }
        except Exception:
            pass
    return {
        "manufacturer": "ASUS (simulado)",
        "product": "ROG STRIX B550-F",
        "serial": "N/A",
        "version": "1.0",
        "note": "Datos simulados - se mostrarán datos reales al ejecutar en Windows",
    }


def get_system_info() -> Dict[str, Any]:
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "is_windows": IS_WINDOWS,
    }


def get_full_hardware_report() -> Dict[str, Any]:
    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "gpu": get_gpu_info(),
        "motherboard": get_motherboard_info(),
    }


def get_realtime_metrics() -> Dict[str, Any]:
    """Lightweight metrics for frequent polling."""
    mem = psutil.virtual_memory()
    disk_total = 0
    disk_used = 0
    for part in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(part.mountpoint)
            disk_total += u.total
            disk_used += u.used
        except PermissionError:
            continue
    disk_percent = (disk_used / disk_total * 100) if disk_total else 0
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "cpu_per_core": psutil.cpu_percent(interval=0.1, percpu=True),
        "memory_percent": mem.percent,
        "memory_used_gb": round(mem.used / (1024**3), 2),
        "memory_total_gb": round(mem.total / (1024**3), 2),
        "disk_percent": round(disk_percent, 1),
        "disk_used_gb": round(disk_used / (1024**3), 2),
        "disk_total_gb": round(disk_total / (1024**3), 2),
        "processes_count": len(psutil.pids()),
    }
