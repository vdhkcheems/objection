"use client";

import { useEffect, useState } from "react";

type HealthStatus = "checking" | "connected" | "offline";

type HealthResponse = {
  service: string;
  status: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus>("checking");
  const [serviceName, setServiceName] = useState("objection-api");

  useEffect(() => {
    const controller = new AbortController();

    async function checkBackend() {
      try {
        const response = await fetch(`${apiBaseUrl}/health`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error("Health check failed");
        }

        const payload = (await response.json()) as HealthResponse;
        setServiceName(payload.service);
        setHealthStatus(payload.status === "ok" ? "connected" : "offline");
      } catch {
        if (!controller.signal.aborted) {
          setHealthStatus("offline");
        }
      }
    }

    checkBackend();

    return () => controller.abort();
  }, []);

  const statusCopy = {
    checking: "Checking backend",
    connected: "Backend connected",
    offline: "Backend unavailable",
  }[healthStatus];

  return (
    <main className="min-h-screen bg-[#f5f2eb] text-[#1f2528]">
      <section className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-5 py-5 sm:px-8 lg:px-10">
        <header className="flex items-center justify-between border-b border-[#c9b99b] pb-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#7b1f2a]">
              Courtroom Strategy
            </p>
            <h1 className="mt-1 text-3xl font-bold tracking-normal text-[#15191b] sm:text-5xl">
              Objection!
            </h1>
          </div>
          <div
            className="flex items-center gap-2 rounded-sm border border-[#c9b99b] bg-white px-3 py-2 text-sm font-medium shadow-sm"
            aria-live="polite"
          >
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                healthStatus === "connected"
                  ? "bg-[#2f7d4f]"
                  : healthStatus === "checking"
                    ? "bg-[#b88727]"
                    : "bg-[#9b2f36]"
              }`}
            />
            {statusCopy}
          </div>
        </header>

        <div className="grid flex-1 gap-5 py-5 lg:grid-cols-[1.1fr_0.9fr]">
          <section className="flex min-h-[520px] flex-col justify-between rounded-sm border border-[#b7a783] bg-[#252b2e] p-5 text-white shadow-xl sm:p-8">
            <div>
              <div className="mb-8 flex items-center justify-between border-b border-white/20 pb-4">
                <span className="text-sm font-medium uppercase tracking-[0.16em] text-[#d9c28f]">
                  Superior Court
                </span>
                <span className="rounded-sm bg-[#7b1f2a] px-3 py-1 text-sm font-semibold">
                  Phase 0
                </span>
              </div>

              <div className="grid gap-4 sm:grid-cols-3">
                <CourtSeat title="Judge" name="Awaiting session" />
                <CourtSeat title="Witness" name="No witness called" />
                <CourtSeat title="Counsel" name="Choose role later" />
              </div>
            </div>

            <div className="mt-10 border-t border-white/20 pt-6">
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#d9c28f]">
                Current Objective
              </p>
              <p className="mt-3 max-w-2xl text-2xl font-semibold leading-tight sm:text-4xl">
                Establish the foundation: web shell online, API reachable, facts
                still locked away.
              </p>
            </div>
          </section>

          <aside className="grid gap-5">
            <Panel title="Case File">
              <dl className="grid gap-3 text-sm">
                <InfoRow label="Demo case" value="Not loaded" />
                <InfoRow label="Evidence" value="Pending Phase 1" />
                <InfoRow label="Witnesses" value="Pending Phase 1" />
              </dl>
            </Panel>

            <Panel title="Session Status">
              <dl className="grid gap-3 text-sm">
                <InfoRow label="Frontend" value="Next.js running" />
                <InfoRow label="Backend" value={statusCopy} />
                <InfoRow label="Service" value={serviceName} />
              </dl>
            </Panel>

            <Panel title="Transcript">
              <div className="space-y-3 text-sm leading-6 text-[#3d4548]">
                <p>
                  <strong>Clerk:</strong> The court recognizes a new project
                  foundation.
                </p>
                <p>
                  <strong>Judge:</strong> Proceed when the backend connection is
                  confirmed.
                </p>
              </div>
            </Panel>
          </aside>
        </div>
      </section>
    </main>
  );
}

function CourtSeat({ title, name }: { title: string; name: string }) {
  return (
    <div className="min-h-36 rounded-sm border border-white/15 bg-white/8 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#d9c28f]">
        {title}
      </p>
      <p className="mt-4 text-lg font-semibold">{name}</p>
    </div>
  );
}

function Panel({
  title,
  children,
}: Readonly<{
  title: string;
  children: React.ReactNode;
}>) {
  return (
    <section className="rounded-sm border border-[#c9b99b] bg-white p-5 shadow-sm">
      <h2 className="text-sm font-bold uppercase tracking-[0.16em] text-[#7b1f2a]">
        {title}
      </h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-[#eadfc9] pb-2 last:border-0 last:pb-0">
      <dt className="font-medium text-[#5d6669]">{label}</dt>
      <dd className="text-right font-semibold text-[#1f2528]">{value}</dd>
    </div>
  );
}
