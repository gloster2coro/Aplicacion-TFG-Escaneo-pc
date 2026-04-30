"""
Optidriver Backend API Tests
Covers all REST endpoints under /api prefix.
AI endpoints have a long timeout (>=120s) since GPT-5.2 calls can take 30-90s.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://optidriver-preview.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

# Read backend URL from frontend .env if env var missing
if "REACT_APP_BACKEND_URL" not in os.environ:
    try:
        with open("/app/frontend/.env") as f:
            for line in f:
                if line.startswith("REACT_APP_BACKEND_URL="):
                    BASE_URL = line.split("=", 1)[1].strip().strip('"').rstrip("/")
                    API = f"{BASE_URL}/api"
                    break
    except Exception:
        pass

DEFAULT_TIMEOUT = 30
AI_TIMEOUT = 180


@pytest.fixture(scope="session")
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---------- Root ----------
class TestRoot:
    def test_root(self, client):
        r = client.get(f"{API}/", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert d.get("app") == "Optidriver"
        assert d.get("status") == "online"


# ---------- Hardware ----------
class TestHardware:
    def test_hardware_full(self, client):
        r = client.get(f"{API}/hardware/full", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        for key in ["cpu", "memory", "disks", "gpu", "motherboard"]:
            assert key in d, f"missing {key} in hardware/full"

    def test_hardware_metrics(self, client):
        r = client.get(f"{API}/hardware/metrics", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "cpu" in d or "cpu_percent" in d
        # accept either key shape
        assert any(k in d for k in ["memory", "memory_percent", "ram", "ram_percent"])


# ---------- System ----------
class TestSystem:
    def test_processes(self, client):
        r = client.get(f"{API}/system/processes", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "processes" in d
        assert isinstance(d["processes"], list)

    def test_services(self, client):
        r = client.get(f"{API}/system/services", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "services" in d
        assert isinstance(d["services"], list)

    def test_startup(self, client):
        r = client.get(f"{API}/system/startup", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "startup_apps" in d
        assert isinstance(d["startup_apps"], list)


# ---------- Optimization ----------
class TestOptimize:
    def test_analyze_gaming(self, client):
        r = client.post(f"{API}/optimize/analyze", json={"profile": "gaming"}, timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert isinstance(d, dict)

    def test_apply_creates_restore_and_log(self, client):
        r = client.post(f"{API}/optimize/apply", json={"profile": "gaming", "simulate": True}, timeout=60)
        assert r.status_code == 200
        d = r.json()
        assert d.get("simulated") is True
        assert "auto_restore_point" in d
        assert d["auto_restore_point"]["source"] == "auto_before_optimize"
        assert "processes_affected" in d
        # New iteration2 fields
        assert "comparison" in d, "Expected 'comparison' field in apply response"
        assert "log_id" in d, "Expected 'log_id' field"
        comp = d["comparison"]
        for key in ["cpu_percent", "memory_percent", "disk_percent", "processes_count"]:
            assert key in comp, f"comparison missing {key}"
            cell = comp[key]
            for sub in ["before", "after", "delta", "delta_percent", "improved"]:
                assert sub in cell, f"comparison.{key} missing {sub}"

        # Logs include this run
        logs_r = client.get(f"{API}/optimize/logs", timeout=DEFAULT_TIMEOUT)
        assert logs_r.status_code == 200
        logs = logs_r.json().get("logs", [])
        assert any(l.get("profile") == "gaming" for l in logs)

        # Current profile updated
        cp_r = client.get(f"{API}/optimize/current-profile", timeout=DEFAULT_TIMEOUT)
        assert cp_r.status_code == 200
        assert cp_r.json().get("profile") == "gaming"


# ---------- Drivers ----------
class TestDrivers:
    def test_drivers_list(self, client):
        r = client.get(f"{API}/drivers", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "drivers" in d
        assert isinstance(d["drivers"], list)
        assert len(d["drivers"]) >= 5  # spec says ~10

    def test_drivers_outdated(self, client):
        r = client.get(f"{API}/drivers/outdated", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "drivers" in d
        assert isinstance(d["drivers"], list)

    def test_drivers_update_simulated(self, client):
        r = client.post(
            f"{API}/drivers/update",
            json={"driver_names": ["NVIDIA GeForce RTX 3060"], "simulate": True},
            timeout=60,
        )
        assert r.status_code == 200
        d = r.json()
        assert d.get("simulated") is True
        assert "auto_restore_point" in d
        assert d["auto_restore_point"]["source"] == "auto_before_driver_update"
        assert "successes" in d and "failures" in d


# ---------- Restore Points ----------
class TestRestore:
    def test_create_and_history(self, client):
        r = client.post(f"{API}/restore/create", json={"description": "TEST_manual"}, timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert d.get("description") == "TEST_manual"
        assert "id" in d

        h = client.get(f"{API}/restore/history", timeout=DEFAULT_TIMEOUT)
        assert h.status_code == 200
        items = h.json().get("restore_points", [])
        assert any(i.get("description") == "TEST_manual" for i in items)


# ---------- AI Assistant ----------
class TestAI:
    def test_ai_analyze(self, client):
        r = client.post(
            f"{API}/ai/analyze",
            json={"profile": "gaming", "budget": "medio"},
            timeout=AI_TIMEOUT,
        )
        assert r.status_code == 200, f"AI analyze failed: {r.status_code} {r.text[:300]}"
        d = r.json()
        assert "recommendation" in d
        assert "session_id" in d

    def test_ai_chat(self, client):
        r = client.post(
            f"{API}/ai/chat",
            json={"message": "Qué puedes hacer?", "session_id": None},
            timeout=AI_TIMEOUT,
        )
        assert r.status_code == 200, f"AI chat failed: {r.status_code} {r.text[:300]}"
        d = r.json()
        assert "response" in d
        assert isinstance(d["response"], str) and len(d["response"]) > 0


# ---------- Docs ----------
class TestDocs:
    def test_docs_pdf(self, client):
        r = client.get(f"{API}/docs/pdf", timeout=60)
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("application/pdf")
        # Magic number for PDF
        assert r.content[:4] == b"%PDF"


# ---------- Scheduler (iteration 2) ----------
class TestScheduler:
    _created_rule_id = None

    def test_status_initial(self, client):
        r = client.get(f"{API}/scheduler/status", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        for k in ["enabled", "interval_seconds", "last_applied_profile",
                  "last_triggered_rule_id", "last_event"]:
            assert k in d, f"scheduler/status missing {k}"
        assert isinstance(d["enabled"], bool)
        assert isinstance(d["interval_seconds"], int)

    def test_toggle_on(self, client):
        r = client.post(f"{API}/scheduler/toggle", json={"enabled": True}, timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        assert r.json().get("enabled") is True
        # confirm via status
        s = client.get(f"{API}/scheduler/status", timeout=DEFAULT_TIMEOUT).json()
        assert s["enabled"] is True

    def test_create_rule(self, client):
        payload = {
            "name": "TEST_rule_python",
            "trigger_processes": ["python3", "fakeproc.exe"],
            "profile": "gaming",
            "priority": 10,
        }
        r = client.post(f"{API}/scheduler/rules", json=payload, timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200, r.text
        d = r.json()
        assert "id" in d
        assert d["name"] == "TEST_rule_python"
        assert d["priority"] == 10
        TestScheduler._created_rule_id = d["id"]

    def test_list_rules_sorted(self, client):
        # add a lower priority rule
        low = client.post(f"{API}/scheduler/rules", json={
            "name": "TEST_low_priority",
            "trigger_processes": ["nothing.exe"],
            "profile": "oficina",
            "priority": 1,
        }, timeout=DEFAULT_TIMEOUT).json()
        r = client.get(f"{API}/scheduler/rules", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        rules = r.json().get("rules", [])
        priorities = [x.get("priority", 0) for x in rules]
        assert priorities == sorted(priorities, reverse=True), \
            f"Rules not sorted desc by priority: {priorities}"
        # cleanup low
        client.delete(f"{API}/scheduler/rules/{low['id']}", timeout=DEFAULT_TIMEOUT)

    def test_events_endpoint(self, client):
        r = client.get(f"{API}/scheduler/events", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        assert "events" in d
        assert isinstance(d["events"], list)

    def test_delete_rule(self, client):
        rid = TestScheduler._created_rule_id
        if not rid:
            pytest.skip("No rule created")
        r = client.delete(f"{API}/scheduler/rules/{rid}", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        assert r.json().get("deleted") == 1
        # confirm it's gone
        rules = client.get(f"{API}/scheduler/rules", timeout=DEFAULT_TIMEOUT).json().get("rules", [])
        assert not any(x.get("id") == rid for x in rules)

    def test_toggle_off(self, client):
        r = client.post(f"{API}/scheduler/toggle", json={"enabled": False}, timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        assert r.json().get("enabled") is False


# ---------- Metrics Comparison (iteration 2) ----------
class TestMetricsComparison:
    def test_snapshot(self, client):
        r = client.get(f"{API}/metrics/snapshot", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        for key in ["label", "timestamp", "cpu_percent", "memory_percent",
                    "disk_percent", "processes_count"]:
            assert key in d, f"snapshot missing {key}"
        assert d["label"] == "manual"

    def test_latest_comparison(self, client):
        # Ensure at least one apply happened (TestOptimize ran first)
        r = client.get(f"{API}/metrics/latest-comparison", timeout=DEFAULT_TIMEOUT)
        assert r.status_code == 200
        d = r.json()
        # Either a doc with comparison or {"comparison": None}
        assert "comparison" in d
        if d["comparison"] is not None:
            for key in ["cpu_percent", "memory_percent", "disk_percent", "processes_count"]:
                assert key in d["comparison"]


# ---------- Files existence (iteration 2 packaging) ----------
class TestPackagingFiles:
    def test_packaging_files_exist(self):
        import os.path as op
        required = [
            "/app/launcher.py",
            "/app/build_exe.bat",
            "/app/build_electron.bat",
            "/app/electron/main.js",
            "/app/electron/preload.js",
            "/app/electron/package.json",
            "/app/WINDOWS_VALIDATION_CHECKLIST.md",
        ]
        missing = [p for p in required if not op.exists(p)]
        assert not missing, f"Missing files: {missing}"

    def test_optidriver_modules_importable(self):
        import importlib
        for mod in ["optidriver.scheduler", "optidriver.metrics_compare"]:
            try:
                importlib.import_module(mod)
            except Exception as e:
                pytest.fail(f"Cannot import {mod}: {e}")
