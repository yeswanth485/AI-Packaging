import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 px-4">
      <div className="max-w-3xl text-center">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-400">
          AI Packaging Automation Platform
        </p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-50 md:text-5xl">
          Optimize every shipment with intelligent packaging decisions.
        </h1>
        <p className="mt-4 text-sm text-slate-300 md:text-base">
          Ingest order data, run ML-powered packaging predictions, and track
          packaging efficiency in a modern SaaS dashboard.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row sm:justify-center">
          <Link
            href="/login"
            className="rounded-full bg-sky-500 px-6 py-2.5 text-sm font-medium text-slate-950 shadow-sm transition hover:bg-sky-400"
          >
            Log in to dashboard
          </Link>
          <Link
            href="/dashboard"
            className="rounded-full border border-slate-600 px-6 py-2.5 text-sm font-medium text-slate-100 transition hover:bg-slate-900/60"
          >
            View demo dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}
