"use client";

import { useMemo } from "react";

export type Order = {
  id: number;
  product_name: string;
  length: number;
  width: number;
  height: number;
  weight: number;
  quantity: number;
  created_at: string;
};

type Props = {
  orders: Order[];
};

export function OrdersTable({ orders }: Props) {
  const hasOrders = orders.length > 0;

  const totalQty = useMemo(
    () => orders.reduce((sum, o) => sum + o.quantity, 0),
    [orders],
  );

  return (
    <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <div className="mb-3 flex items-center justify-between text-sm">
        <h2 className="font-semibold">Orders</h2>
        <span className="text-xs text-slate-400">
          {orders.length} orders · {totalQty} units
        </span>
      </div>
      {!hasOrders ? (
        <p className="text-xs text-slate-400">
          No orders yet. Upload a CSV or create orders via the API.
        </p>
      ) : (
        <div className="max-h-64 overflow-auto text-xs">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400">
                <th className="px-2 py-1 text-left">Product</th>
                <th className="px-2 py-1 text-left">L×W×H</th>
                <th className="px-2 py-1 text-left">Weight</th>
                <th className="px-2 py-1 text-right">Qty</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((o) => (
                <tr key={o.id} className="border-b border-slate-900/60">
                  <td className="px-2 py-1">{o.product_name}</td>
                  <td className="px-2 py-1 text-slate-300">
                    {o.length} × {o.width} × {o.height}
                  </td>
                  <td className="px-2 py-1 text-slate-300">{o.weight}</td>
                  <td className="px-2 py-1 text-right">{o.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

