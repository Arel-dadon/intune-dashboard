import { useEffect, useState, useMemo, useCallback } from "react";
import { getDuplicates, getSummary } from "./services/api";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

function App() {
  const [duplicates, setDuplicates] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const [search, setSearch] = useState("");
  const [sortAsc, setSortAsc] = useState(true);

  // ✅ Stable data loader
  const loadData = useCallback(async () => {
    try {
      const dup = await getDuplicates();
      const sum = await getSummary();
      setDuplicates(dup);
      setSummary(sum);
    } catch (err) {
      console.error("Failed loading data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // ✅ Auto refresh every 30s
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [loadData]);

  // ✅ Filtering + sorting
  const processedDuplicates = useMemo(() => {
    let filtered = duplicates;

    if (severityFilter !== "ALL") {
      filtered = filtered.filter(
        (d) => d.severity === severityFilter
      );
    }

    if (search) {
      filtered = filtered.filter((d) =>
        d.deviceName.toLowerCase().includes(search.toLowerCase())
      );
    }

    return [...filtered].sort((a, b) =>
      sortAsc
        ? a.deviceName.localeCompare(b.deviceName)
        : b.deviceName.localeCompare(a.deviceName)
    );
  }, [duplicates, severityFilter, search, sortAsc]);

  if (loading) {
    return (
      <div style={styles.container}>
        <h2>Loading dashboard...</h2>
      </div>
    );
  }

  const pieData = [
    { name: "Compliant", value: summary?.compliant || 0 },
    { name: "NonCompliant", value: summary?.nonCompliant || 0 },
  ];

  return (
    <div style={styles.container}>
      <h1>Intune Device Dashboard</h1>

      {/* 🔹 Controls */}
      <div style={styles.controls}>
        <input
          type="text"
          placeholder="Search device..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={styles.input}
        />

        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          style={styles.select}
        >
          <option value="ALL">All Severities</option>
          <option value="HIGH">High Only</option>
          <option value="LOW">Low Only</option>
        </select>

        <button
          onClick={() => setSortAsc(!sortAsc)}
          style={styles.button}
        >
          Sort {sortAsc ? "↓" : "↑"}
        </button>
      </div>

      {/* 🔹 Charts */}
      <div style={styles.chartRow}>
        <PieChart width={300} height={250}>
          <Pie
            data={pieData}
            dataKey="value"
            outerRadius={100}
            label
          >
            <Cell fill="#4caf50" />
            <Cell fill="#ff4d4d" />
          </Pie>
          <Tooltip />
        </PieChart>

        <BarChart
          width={400}
          height={250}
          data={processedDuplicates}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="deviceName" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </div>

      {/* 🔹 Table */}
      <table style={styles.table}>
        <thead>
          <tr>
            <th>Device Name</th>
            <th>Count</th>
            <th>Severity</th>
          </tr>
        </thead>
        <tbody>
          {processedDuplicates.map((group) => (
            <tr key={group.deviceName}>
              <td>{group.deviceName}</td>
              <td>{group.count}</td>
              <td
                style={{
                  color:
                    group.severity === "HIGH"
                      ? "#ff4d4d"
                      : "#ffaa00",
                }}
              >
                {group.severity}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const styles = {
  container: {
    padding: "40px",
    backgroundColor: "#0f172a",
    color: "white",
    minHeight: "100vh",
    fontFamily: "Segoe UI",
  },
  controls: {
    display: "flex",
    gap: "15px",
    marginBottom: "30px",
  },
  input: {
    padding: "8px",
  },
  select: {
    padding: "8px",
  },
  button: {
    padding: "8px 12px",
    cursor: "pointer",
  },
  chartRow: {
    display: "flex",
    gap: "50px",
    marginBottom: "40px",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
};

export default App;