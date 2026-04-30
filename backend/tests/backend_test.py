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
