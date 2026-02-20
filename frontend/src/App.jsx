import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [duplicates, setDuplicates] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/devices/duplicates")
      .then(res => setDuplicates(res.data));
  }, []);

  if (!duplicates) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Intune Duplicate Device Analytics</h1>

      <div className="cards">
        <Card title="Duplicate Groups" value={duplicates.totalDuplicateGroups} />
        <Card title="Current Page" value={duplicates.currentPage} />
        <Card title="Total Pages" value={duplicates.totalPages} />
      </div>

      <div className="table-section">
        {duplicates.value.map(group => (
          <div key={group.deviceName} className="group">
            <div className="group-header">
              <span>{group.deviceName}</span>
              <span>{group.duplicateCount} devices</span>
              <span className={group.severity}>{group.severity}</span>
              <span>{group.serialMismatch ? "⚠ Serial Mismatch" : "OK"}</span>
            </div>

            <table>
              <thead>
                <tr>
                  <th>IP</th>
                  <th>Compliance</th>
                  <th>OS</th>
                  <th>Encrypted</th>
                  <th>Last Sync</th>
                </tr>
              </thead>
              <tbody>
                {group.devices.map((device, i) => (
                  <tr key={i}>
                    <td>{device.ipAddress}</td>
                    <td>{device.complianceState}</td>
                    <td>{device.operatingSystem}</td>
                    <td>{device.encrypted ? "Yes" : "No"}</td>
                    <td>{device.lastSyncDateTime}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <h2>{value}</h2>
    </div>
  );
}

export default App;