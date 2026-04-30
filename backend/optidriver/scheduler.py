"""
Auto-scheduler: monitors running processes and applies profiles based on rules.
Rules are stored in MongoDB: collection 'scheduler_rules'.
Example rule: when 'steam.exe' runs -> apply profile 'gaming'.
"""
import asyncio
import psutil
from typing import Dict, Any, List, Set


def get_running_process_names() -> Set[str]:
    names = set()
    for proc in psutil.process_iter(['name']):
        try:
            n = (proc.info.get('name') or "").lower()
            if n:
                names.add(n)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return names


class SchedulerEngine:
    """Polls process list and fires matching rules."""

    def __init__(self, db):
        self.db = db
        self.enabled = False
        self.interval_seconds = 15
        self._task = None
        self._last_applied_profile = None
        self._last_triggered_rule_id = None
        self._last_event = None

    async def start(self):
        if self._task and not self._task.done():
            return
        self.enabled = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self.enabled = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "interval_seconds": self.interval_seconds,
            "last_applied_profile": self._last_applied_profile,
            "last_triggered_rule_id": self._last_triggered_rule_id,
            "last_event": self._last_event,
        }

    async def _loop(self):
        while self.enabled:
            try:
                await self._tick()
            except Exception as e:
                self._last_event = {"error": str(e)}
            await asyncio.sleep(self.interval_seconds)

    async def _tick(self):
        """Check rules against running processes."""
        rules = await self.db.scheduler_rules.find(
            {"enabled": True}, {"_id": 0}
        ).sort("priority", -1).to_list(100)

        if not rules:
            return

        running = get_running_process_names()

        for rule in rules:
            triggers = [t.lower() for t in rule.get("trigger_processes", [])]
            if any(t in running for t in triggers):
                profile = rule.get("profile")
                # Avoid re-applying same profile repeatedly
                if profile == self._last_applied_profile and rule["id"] == self._last_triggered_rule_id:
                    return
                # Fire the event (lazy import to avoid circular)
                from optidriver import optimizer
                result = optimizer.apply_optimizations(profile, simulate=True)
                self._last_applied_profile = profile
                self._last_triggered_rule_id = rule["id"]
                self._last_event = {
                    "rule_id": rule["id"],
                    "rule_name": rule.get("name"),
                    "profile": profile,
                    "trigger_matched": [t for t in triggers if t in running],
                    "processes_affected": result["processes_affected"],
                    "simulated": result["simulated"],
                }
                await self.db.scheduler_events.insert_one({**self._last_event, "_id": rule["id"] + "_" + str(asyncio.get_event_loop().time())}.copy())
                return

        # No rules matched - clear "last applied" so it can retrigger later
        self._last_applied_profile = None
        self._last_triggered_rule_id = None


_engine = None


def get_engine(db):
    global _engine
    if _engine is None:
        _engine = SchedulerEngine(db)
    return _engine
