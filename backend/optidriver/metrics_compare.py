"""
Before/After metrics comparison.
Captures snapshots before and after optimizations to show user the impact.
"""
from datetime import datetime, timezone
from typing import Dict, Any
from optidriver import hardware


def capture_snapshot(label: str = "snapshot") -> Dict[str, Any]:
    """Takes a lightweight metrics snapshot tagged with label."""
    m = hardware.get_realtime_metrics()
    return {
        "label": label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": m["cpu_percent"],
        "memory_percent": m["memory_percent"],
        "memory_used_gb": m["memory_used_gb"],
        "disk_percent": m["disk_percent"],
        "processes_count": m["processes_count"],
    }


def compute_delta(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Computes diff between two snapshots."""
    def delta(key: str, lower_is_better: bool = True):
        b = before.get(key, 0) or 0
        a = after.get(key, 0) or 0
        diff = round(a - b, 2)
        pct = round((diff / b * 100), 2) if b else 0
        improved = (diff < 0) if lower_is_better else (diff > 0)
        return {
            "before": b,
            "after": a,
            "delta": diff,
            "delta_percent": pct,
            "improved": improved,
        }

    return {
        "cpu_percent": delta("cpu_percent"),
        "memory_percent": delta("memory_percent"),
        "memory_used_gb": delta("memory_used_gb"),
        "disk_percent": delta("disk_percent"),
        "processes_count": delta("processes_count"),
    }
