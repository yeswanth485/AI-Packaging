"use client";

import { useState } from "react";

type Props = {
  onUpload: (rows: CsvOrderRow[]) => Promise<void> | void;
};

export type CsvOrderRow = {
  order_id: string;
  product_name: string;
  length: number;
  width: number;
  height: number;
  weight: number;
  quantity: number;
};

export function CsvUpload({ onUpload }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError(null);
    setLoading(true);

    try {
      const text = await file.text();
      const rows = parseCsv(text);
      if (rows.length === 0) {
        setError("No valid rows found in CSV.");
      } else {
        await onUpload(rows);
      }
    } catch (e) {
      console.error(e);
      setError("Failed to parse CSV file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <h2 className="mb-2 text-sm font-semibold">Upload order dataset (CSV)</h2>
      <p className="mb-3 text-xs text-slate-400">
        Columns: order_id, product_name, length, width, height, weight, quantity
      </p>
      <input
        type="file"
        accept=".csv,text/csv"
        onChange={handleFileChange}
        className="text-xs file:mr-3 file:rounded-md file:border-0 file:bg-slate-800 file:px-3 file:py-1.5 file:text-xs file:font-medium file:text-slate-100 hover:file:bg-slate-700"
      />
      {loading && (
        <p className="mt-2 text-xs text-slate-400">Uploading and processing…</p>
      )}
      {error && <p className="mt-2 text-xs text-red-400">{error}</p>}
    </div>
  );
}

function parseCsv(text: string): CsvOrderRow[] {
  const lines = text.split(/\r?\n/).map((l) => l.trim());
  const header = lines[0]?.split(",").map((h) => h.trim().toLowerCase());
  if (!header || header.length < 7) return [];

  const idx = (name: string) => header.indexOf(name);

  const rows: CsvOrderRow[] = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line) continue;
    const parts = line.split(",").map((p) => p.trim());
    if (parts.length < 7) continue;

    try {
      const row: CsvOrderRow = {
        order_id: parts[idx("order_id")] ?? `${i}`,
        product_name: parts[idx("product_name")] ?? "Unknown",
        length: Number(parts[idx("length")]),
        width: Number(parts[idx("width")]),
        height: Number(parts[idx("height")]),
        weight: Number(parts[idx("weight")]),
        quantity: Number(parts[idx("quantity")]),
      };
      if (
        !isFinite(row.length) ||
        !isFinite(row.width) ||
        !isFinite(row.height) ||
        !isFinite(row.weight) ||
        !isFinite(row.quantity)
      ) {
        continue;
      }
      rows.push(row);
    } catch {
      continue;
    }
  }
  return rows;
}

