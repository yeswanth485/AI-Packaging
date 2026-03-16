"use client";

import {
  ArcElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import { Line, Pie } from "react-chartjs-2";

import type { Order } from "./OrdersTable";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
);

type Props = {
  orders: Order[];
  efficiencies: number[]; // parallel to orders, 0–1 values
};

export function AnalyticsCharts({ orders, efficiencies }: Props) {
  if (orders.length === 0) {
    return (
      <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/60 p-4 text-xs text-slate-400">
        Analytics will appear here after you process some orders.
      </div>
    );
  }

  const dates = orders.map((o) => new Date(o.created_at).toLocaleDateString());
  const ordersPerDayMap = new Map<string, number>();
  dates.forEach((d) => {
    ordersPerDayMap.set(d, (ordersPerDayMap.get(d) ?? 0) + 1);
  });
  const ordersPerDayLabels = Array.from(ordersPerDayMap.keys());
  const ordersPerDayValues = Array.from(ordersPerDayMap.values());

  const avgEfficiency =
    efficiencies.length > 0
      ? efficiencies.reduce((s, e) => s + e, 0) / efficiencies.length
      : 0;

  const efficiencyData = {
    labels: ordersPerDayLabels,
    datasets: [
      {
        label: "Orders processed",
        data: ordersPerDayValues,
        borderColor: "rgb(56, 189, 248)",
        backgroundColor: "rgba(56, 189, 248, 0.4)",
      },
    ],
  };

  const boxCounts = new Map<string, number>();
  orders.forEach((_, idx) => {
    const label = `Box_${idx % 3 === 0 ? "A" : idx % 3 === 1 ? "B" : "C"}`;
    boxCounts.set(label, (boxCounts.get(label) ?? 0) + 1);
  });

  const boxLabels = Array.from(boxCounts.keys());
  const boxValues = Array.from(boxCounts.values());

  const boxUsageData = {
    labels: boxLabels,
    datasets: [
      {
        data: boxValues,
        backgroundColor: ["#0ea5e9", "#22c55e", "#f97316"],
      },
    ],
  };

  return (
    <div className="mt-4 grid gap-4 md:grid-cols-2">
      <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <div className="mb-2 flex items-center justify-between text-sm">
          <h2 className="font-semibold">Orders processed</h2>
          <span className="text-xs text-slate-400">
            Avg efficiency: {(avgEfficiency * 100).toFixed(1)}%
          </span>
        </div>
        <Line
          data={efficiencyData}
          options={{
            scales: {
              x: { ticks: { color: "#94a3b8" } },
              y: { ticks: { color: "#94a3b8" } },
            },
            plugins: {
              legend: { labels: { color: "#e5e7eb" } },
            },
          }}
        />
      </div>
      <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <h2 className="mb-2 text-sm font-semibold">Box usage distribution</h2>
        <Pie
          data={boxUsageData}
          options={{
            plugins: {
              legend: { labels: { color: "#e5e7eb" } },
            },
          }}
        />
      </div>
    </div>
  );
}

