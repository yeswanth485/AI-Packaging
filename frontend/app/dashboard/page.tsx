"use client";

import { useEffect, useState } from "react";

import { Sidebar } from "@/components/Sidebar";
import { AnalyticsCharts } from "@/components/AnalyticsCharts";
import { CsvUpload, type CsvOrderRow } from "@/components/CsvUpload";
import { OrdersTable, type Order } from "@/components/OrdersTable";
import { PredictionPanel } from "@/components/PredictionPanel";
import {
  apiCreateOrder,
  apiGetOrders,
  apiPredictPackaging,
} from "@/lib/api";

export default function DashboardPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [efficiencies, setEfficiencies] = useState<number[]>([]);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [loadingPrediction, setLoadingPrediction] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [predictionError, setPredictionError] = useState<string | null>(null);
  const [lastPrediction, setLastPrediction] = useState<{
    recommended_box: string;
    confidence_score: number;
    efficiency_score: number;
  } | null>(null);

  useEffect(() => {
    const token =
      typeof window !== "undefined" ? localStorage.getItem("token") : null;
    if (!token) {
      return;
    }
    (async () => {
      try {
        setLoadingOrders(true);
        const data = await apiGetOrders();
        setOrders(data);
        setEfficiencies([]);
      } catch (e) {
        const message =
          e instanceof Error ? e.message : "Failed to load orders";
        setError(message);
      } finally {
        setLoadingOrders(false);
      }
    })();
  }, []);

  const handleCsvUpload = async (rows: CsvOrderRow[]) => {
    setError(null);
    setLoadingOrders(true);
    try {
      const created: Order[] = [];
      for (const row of rows) {
        const o = await apiCreateOrder({
          product_name: row.product_name,
          length: row.length,
          width: row.width,
          height: row.height,
          weight: row.weight,
          quantity: row.quantity,
        });
        created.push(o as Order);
      }
      setOrders((prev) => [...created, ...prev]);
    } catch (e) {
      const message =
        e instanceof Error ? e.message : "Failed to create orders from CSV";
      setError(message);
    } finally {
      setLoadingOrders(false);
    }
  };

  const handlePredictLastOrder = async () => {
    if (orders.length === 0) return;
    const latest = orders[0];
    setPredictionError(null);
    setLoadingPrediction(true);
    try {
      const res = await apiPredictPackaging({
        length: latest.length,
        width: latest.width,
        height: latest.height,
        weight: latest.weight,
      });
      setLastPrediction(res);
      setEfficiencies((prev) => [...prev, res.efficiency_score]);
    } catch (e) {
      const message =
        e instanceof Error ? e.message : "Prediction failed";
      setPredictionError(message);
    } finally {
      setLoadingPrediction(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto px-6 py-6">
        <header className="mb-6 flex flex-col justify-between gap-3 md:flex-row md:items-center">
          <div>
            <h1 className="text-xl font-semibold">Dashboard</h1>
            <p className="text-xs text-slate-400">
              Upload orders, run packaging predictions, and monitor efficiency.
            </p>
          </div>
          <button
            onClick={handlePredictLastOrder}
            disabled={orders.length === 0 || loadingPrediction}
            className="inline-flex items-center justify-center rounded-md bg-sky-500 px-3 py-2 text-xs font-medium text-slate-950 transition hover:bg-sky-400 disabled:opacity-60"
          >
            {loadingPrediction
              ? "Running prediction…"
              : "Predict for latest order"}
          </button>
        </header>

        <section className="grid gap-4 md:grid-cols-[minmax(0,2fr)_minmax(0,1.4fr)]">
          <div>
            <CsvUpload onUpload={handleCsvUpload} />
            <OrdersTable orders={orders} />
            {error && (
              <p className="mt-2 text-xs text-red-400">
                {error}
              </p>
            )}
            {loadingOrders && (
              <p className="mt-2 text-xs text-slate-400">
                Syncing orders with API…
              </p>
            )}
          </div>
          <div className="space-y-4">
            <PredictionPanel
              loading={loadingPrediction}
              error={predictionError}
              lastPrediction={lastPrediction}
            />
            <AnalyticsCharts orders={orders} efficiencies={efficiencies} />
          </div>
        </section>
      </main>
    </div>
  );
}

