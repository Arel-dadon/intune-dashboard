const API_BASE = "/api/devices";

// 🔹 Core Data
export async function getDevices() {
  const res = await fetch(`${API_BASE}`);
  if (!res.ok) throw new Error("Failed to fetch devices");
  return res.json();
}

export async function getSummary() {
  const res = await fetch(`${API_BASE}/summary`);
  if (!res.ok) throw new Error("Failed to fetch summary");
  return res.json();
}

export async function getDuplicates() {
  const res = await fetch(`${API_BASE}/duplicates`);
  if (!res.ok) throw new Error("Failed to fetch duplicates");
  return res.json();
}

// 🔹 Monitoring Data
export async function getStaleDevices() {
  const res = await fetch(`${API_BASE}/stale`);
  if (!res.ok) throw new Error("Failed to fetch stale devices");
  return res.json();
}

export async function getOSDistribution() {
  const res = await fetch(`${API_BASE}/os-distribution`);
  if (!res.ok) throw new Error("Failed to fetch OS distribution");
  return res.json();
}

export async function getComplianceBreakdown() {
  const res = await fetch(`${API_BASE}/compliance-breakdown`);
  if (!res.ok) throw new Error("Failed to fetch compliance breakdown");
  return res.json();
}

export async function getDeviceHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Failed to fetch device health");
  return res.json();
}