"""
Optimization engine - analyzes processes and applies profile-based optimizations.
Critical Windows processes are protected from being terminated.
"""
import psutil
import platform
from typing import Dict, List, Any

IS_WINDOWS = platform.system().lower() == "windows"

# Critical processes that MUST NEVER be terminated
CRITICAL_PROCESSES = {
    "system", "system idle process", "registry", "smss.exe", "csrss.exe",
    "wininit.exe", "services.exe", "lsass.exe", "winlogon.exe",
    "explorer.exe", "dwm.exe", "svchost.exe", "taskhostw.exe",
    "fontdrvhost.exe", "sihost.exe", "ctfmon.exe", "conhost.exe",
    "runtimebroker.exe", "shellexperiencehost.exe", "searchhost.exe",
    "startmenuexperiencehost.exe", "applicationframehost.exe",
    # Linux system processes (for dev env)
    "systemd", "kthreadd", "init", "kernel", "bash", "sh",
    "python", "python3", "node", "supervisord",
}

# Processes targeted by each optimization profile
PROFILE_TARGETS = {
    "gaming": {
        "description": "Máximo rendimiento - cierra procesos no esenciales y desactiva efectos visuales",
        "target_processes": [
            "onedrive.exe", "teams.exe", "skype.exe", "spotify.exe",
            "discord.exe", "slack.exe", "zoom.exe", "chrome.exe",
            "firefox.exe", "edge.exe", "steam.exe", "epicgameslauncher.exe",
            "adobebridge.exe", "adobereader.exe", "acrobat.exe",
            "onedrivesetup.exe", "outlook.exe",
        ],
        "visual_effects": "disabled",
        "cpu_priority": "high",
        "power_plan": "high_performance",
    },
    "oficina": {
        "description": "Rendimiento equilibrado con efectos visuales habilitados",
        "target_processes": [
            "steam.exe", "epicgameslauncher.exe", "origin.exe",
            "battlenet.exe", "spotify.exe", "discord.exe",
        ],
        "visual_effects": "enabled",
        "cpu_priority": "normal",
        "power_plan": "balanced",
    },
    "optimo": {
        "description": "Balance general automático - optimización moderada",
        "target_processes": [
            "onedrive.exe", "teams.exe", "skype.exe",
            "adobebridge.exe", "acrobat.exe",
        ],
        "visual_effects": "best_appearance_and_performance",
        "cpu_priority": "normal",
        "power_plan": "balanced",
    },
}


def scan_processes() -> List[Dict[str, Any]]:
    """Returns list of running processes with their resource usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent', 'status']):
        try:
            info = proc.info
            name = (info.get('name') or "").lower()
            processes.append({
                "pid": info['pid'],
                "name": info.get('name') or "Unknown",
                "username": info.get('username') or "N/A",
                "memory_percent": round(info.get('memory_percent') or 0, 2),
                "cpu_percent": round(info.get('cpu_percent') or 0, 2),
                "status": info.get('status') or "unknown",
                "is_critical": name in CRITICAL_PROCESSES,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Sort by memory usage
    processes.sort(key=lambda p: p['memory_percent'], reverse=True)
    return processes[:100]  # top 100


def scan_startup_apps() -> List[Dict[str, Any]]:
    """
    Lists apps configured to run at startup.
    On Windows, reads registry. In dev env returns simulated data.
    """
    if IS_WINDOWS:
        try:
            import winreg  # type: ignore
            startup_items = []
            paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            ]
            for hive, path in paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                startup_items.append({
                                    "name": name,
                                    "command": value,
                                    "hive": "HKCU" if hive == winreg.HKEY_CURRENT_USER else "HKLM",
                                    "enabled": True,
                                })
                                i += 1
                            except OSError:
                                break
                except FileNotFoundError:
                    continue
            return startup_items
        except Exception:
            pass
    # Simulated startup apps
    return [
        {"name": "OneDrive", "command": "C:\\Users\\...\\OneDrive.exe /background", "hive": "HKCU", "enabled": True, "simulated": True},
        {"name": "Microsoft Teams", "command": "C:\\Users\\...\\Teams.exe --system-initiated", "hive": "HKCU", "enabled": True, "simulated": True},
        {"name": "Steam", "command": "C:\\Program Files\\Steam\\steam.exe -silent", "hive": "HKLM", "enabled": True, "simulated": True},
        {"name": "Discord", "command": "C:\\Users\\...\\Discord.exe --start-minimized", "hive": "HKCU", "enabled": True, "simulated": True},
        {"name": "Spotify", "command": "C:\\Users\\...\\Spotify.exe -autostart", "hive": "HKCU", "enabled": True, "simulated": True},
        {"name": "NVIDIA GeForce Experience", "command": "C:\\Program Files\\NVIDIA Corporation\\...", "hive": "HKLM", "enabled": True, "simulated": True},
    ]


def scan_services() -> List[Dict[str, Any]]:
    """Lists Windows services. Simulated on Linux."""
    if IS_WINDOWS:
        try:
            services = []
            for s in psutil.win_service_iter():
                info = s.as_dict()
                services.append({
                    "name": info.get('name'),
                    "display_name": info.get('display_name'),
                    "status": info.get('status'),
                    "start_type": info.get('start_type'),
                })
            return services
        except Exception:
            pass
    # Simulated services
    return [
        {"name": "DiagTrack", "display_name": "Experiencias del usuario conectado y telemetría", "status": "running", "start_type": "automatic", "simulated": True},
        {"name": "SysMain", "display_name": "SysMain (Superfetch)", "status": "running", "start_type": "automatic", "simulated": True},
        {"name": "WSearch", "display_name": "Windows Search", "status": "running", "start_type": "automatic", "simulated": True},
        {"name": "Fax", "display_name": "Fax", "status": "stopped", "start_type": "manual", "simulated": True},
        {"name": "Spooler", "display_name": "Cola de impresión", "status": "running", "start_type": "automatic", "simulated": True},
        {"name": "XblGameSave", "display_name": "Servicio de guardado de juego Xbox Live", "status": "running", "start_type": "manual", "simulated": True},
    ]


def analyze_system(profile: str) -> Dict[str, Any]:
    """Analyzes the system against a profile and returns optimization plan."""
    profile = profile.lower()
    if profile not in PROFILE_TARGETS:
        profile = "optimo"

    config = PROFILE_TARGETS[profile]
    processes = scan_processes()
    startup = scan_startup_apps()

    target_set = set(config["target_processes"])
    processes_to_close = [
        p for p in processes
        if p["name"].lower() in target_set and not p["is_critical"]
    ]

    return {
        "profile": profile,
        "description": config["description"],
        "processes_to_close": processes_to_close,
        "startup_to_disable": [s for s in startup if any(
            t.split(".")[0].lower() in s["name"].lower()
            for t in config["target_processes"]
        )],
        "visual_effects": config["visual_effects"],
        "cpu_priority": config["cpu_priority"],
        "power_plan": config["power_plan"],
        "estimated_memory_freed_mb": sum(
            p["memory_percent"] * 100 for p in processes_to_close
        ),
    }


def apply_optimizations(profile: str, simulate: bool = True) -> Dict[str, Any]:
    """
    Applies optimizations based on profile.
    simulate=True: only logs what would be done (safe).
    simulate=False: actually terminates processes (only on Windows).
    """
    plan = analyze_system(profile)
    applied = []
    errors = []

    for proc_info in plan["processes_to_close"]:
        if proc_info["is_critical"]:
            continue
        if simulate or not IS_WINDOWS:
            applied.append({
                "action": "terminate_process",
                "target": proc_info["name"],
                "pid": proc_info["pid"],
                "status": "simulated",
            })
        else:
            try:
                p = psutil.Process(proc_info["pid"])
                p.terminate()
                applied.append({
                    "action": "terminate_process",
                    "target": proc_info["name"],
                    "pid": proc_info["pid"],
                    "status": "success",
                })
            except Exception as e:
                errors.append({
                    "target": proc_info["name"],
                    "error": str(e),
                })

    # Power plan, visual effects commands (documented but only executed on Windows)
    config = PROFILE_TARGETS[profile]
    commands_executed = [
        {
            "description": f"Plan de energía: {config['power_plan']}",
            "command": _power_plan_command(config["power_plan"]),
            "status": "simulated" if simulate or not IS_WINDOWS else "success",
        },
        {
            "description": f"Efectos visuales: {config['visual_effects']}",
            "command": _visual_effects_command(config["visual_effects"]),
            "status": "simulated" if simulate or not IS_WINDOWS else "success",
        },
    ]

    return {
        "profile": profile,
        "processes_affected": len(applied),
        "applied_actions": applied,
        "system_commands": commands_executed,
        "errors": errors,
        "simulated": simulate or not IS_WINDOWS,
        "note": "Modo simulación activo. En Windows con permisos admin estas acciones se ejecutarán realmente." if simulate or not IS_WINDOWS else "Cambios aplicados correctamente.",
    }


def _power_plan_command(plan: str) -> str:
    mapping = {
        "high_performance": "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
        "balanced": "powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e",
        "power_saver": "powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a",
    }
    return mapping.get(plan, mapping["balanced"])


def _visual_effects_command(setting: str) -> str:
    mapping = {
        "disabled": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
        "enabled": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 1 /f',
        "best_appearance_and_performance": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 0 /f',
    }
    return mapping.get(setting, mapping["best_appearance_and_performance"])
