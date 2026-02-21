export async function getDevices() {
  const res = await fetch("/api/devices");
  if (!res.ok) throw new Error("Failed to fetch devices");
  return res.json();
}

export async function getSummary() {
  const res = await fetch("/api/devices/summary");
  if (!res.ok) throw new Error("Failed to fetch summary");
  return res.json();
}

export async function getDuplicates() {
  const res = await fetch("/api/devices/duplicates");
  if (!res.ok) throw new Error("Failed to fetch duplicates");
  return res.json();
}