import { STATUSES } from "../statuses";

export default function StatsBar({ stats }) {
  return (
    <dl className="stats">
      <div>
        <dt>Total</dt>
        <dd>{stats.total}</dd>
      </div>
      {STATUSES.map((status) => (
        <div key={status}>
          <dt>{status}</dt>
          <dd>{stats.by_status[status] ?? 0}</dd>
        </div>
      ))}
    </dl>
  );
}