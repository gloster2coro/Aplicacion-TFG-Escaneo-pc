import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API,
  headers: { "Content-Type": "application/json" },
  timeout: 60000,
});

// Hardware
export const getHardwareFull = () => api.get("/hardware/full").then(r => r.data);
export const getHardwareMetrics = () => api.get("/hardware/metrics").then(r => r.data);

// System
export const getProcesses = () => api.get("/system/processes").then(r => r.data);
export const getServices = () => api.get("/system/services").then(r => r.data);
export const getStartup = () => api.get("/system/startup").then(r => r.data);

// Optimize
export const analyzeProfile = (profile) =>
  api.post("/optimize/analyze", { profile }).then(r => r.data);
export const applyOptimization = (profile, simulate = true) =>
  api.post("/optimize/apply", { profile, simulate }).then(r => r.data);
export const getOptimizeLogs = () => api.get("/optimize/logs").then(r => r.data);
export const getCurrentProfile = () => api.get("/optimize/current-profile").then(r => r.data);

// Drivers
export const getDrivers = () => api.get("/drivers").then(r => r.data);
export const getOutdatedDrivers = () => api.get("/drivers/outdated").then(r => r.data);
export const updateDrivers = (driverNames, simulate = true) =>
  api.post("/drivers/update", { driver_names: driverNames, simulate }).then(r => r.data);

// Restore
export const createRestorePoint = (description, pointType = "MODIFY_SETTINGS") =>
  api.post("/restore/create", { description, point_type: pointType }).then(r => r.data);
export const getRestoreHistory = () => api.get("/restore/history").then(r => r.data);

// AI
export const aiAnalyze = (profile, budget = "medio", sessionId = null) =>
  api.post("/ai/analyze", { profile, budget, session_id: sessionId }).then(r => r.data);
export const aiChat = (message, sessionId = null, includeHardware = false) =>
  api.post("/ai/chat", { message, session_id: sessionId, include_hardware: includeHardware }).then(r => r.data);
export const getAISessions = () => api.get("/ai/sessions").then(r => r.data);

export const getDocsPdfUrl = () => `${API}/docs/pdf`;

// Scheduler
export const getSchedulerStatus = () => api.get("/scheduler/status").then(r => r.data);
export const toggleScheduler = (enabled, intervalSeconds = null) =>
  api.post("/scheduler/toggle", { enabled, interval_seconds: intervalSeconds }).then(r => r.data);
export const getSchedulerRules = () => api.get("/scheduler/rules").then(r => r.data);
export const createSchedulerRule = (rule) =>
  api.post("/scheduler/rules", rule).then(r => r.data);
export const deleteSchedulerRule = (ruleId) =>
  api.delete(`/scheduler/rules/${ruleId}`).then(r => r.data);
export const getSchedulerEvents = () => api.get("/scheduler/events").then(r => r.data);

// Metrics
export const getLatestComparison = () => api.get("/metrics/latest-comparison").then(r => r.data);
export const getMetricsSnapshot = () => api.get("/metrics/snapshot").then(r => r.data);
