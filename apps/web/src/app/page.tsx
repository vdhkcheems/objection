"use client";

import { useEffect, useState } from "react";

type HealthStatus = "checking" | "connected" | "offline";

type HealthResponse = {
  service: string;
  status: string;
};

type CaseSummary = {
  id: string;
  title: string;
  summary: string;
  status: string;
  charge_count: number;
  witness_count: number;
  evidence_count: number;
};

type CaseOverview = {
  id: string;
  title: string;
  summary: string;
  jurisdiction: string;
  status: string;
  player_roles: string[];
  charges: {
    id: string;
    name: string;
    description: string;
    legal_elements: {
      id: string;
      name: string;
      description: string;
    }[];
  }[];
  witnesses: {
    id: string;
    name: string;
    role: string;
    bio: string;
    statement_count: number;
  }[];
  evidence: {
    id: string;
    title: string;
    type: string;
    description: string;
    admissibility_status: string | null;
  }[];
  timeline: {
    id: string;
    sequence: number;
    timestamp: string;
    description: string;
  }[];
};

type CaseStatus = "loading" | "loaded" | "unavailable";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus>("checking");
  const [serviceName, setServiceName] = useState("objection-api");
  const [caseStatus, setCaseStatus] = useState<CaseStatus>("loading");
  const [caseOverview, setCaseOverview] = useState<CaseOverview | null>(null);

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

  useEffect(() => {
    const controller = new AbortController();

    async function loadCase() {
      try {
        const casesResponse = await fetch(`${apiBaseUrl}/cases`, {
          signal: controller.signal,
        });

        if (!casesResponse.ok) {
          throw new Error("Case list unavailable");
        }

        const cases = (await casesResponse.json()) as CaseSummary[];
        const selectedCase = cases[0];

        if (!selectedCase) {
          throw new Error("No cases available");
        }

        const overviewResponse = await fetch(
          `${apiBaseUrl}/cases/${selectedCase.id}/overview`,
          { signal: controller.signal },
        );

        if (!overviewResponse.ok) {
          throw new Error("Case overview unavailable");
        }

        const overview = (await overviewResponse.json()) as CaseOverview;
        setCaseOverview(overview);
        setCaseStatus("loaded");
      } catch {
        if (!controller.signal.aborted) {
          setCaseStatus("unavailable");
        }
      }
    }

    loadCase();

    return () => controller.abort();
  }, []);

  const statusCopy = {
    checking: "Checking backend",
    connected: "Backend connected",
    offline: "Backend unavailable",
  }[healthStatus];

  const caseStatusCopy = {
    loading: "Loading case file",
    loaded: "Locked case loaded",
    unavailable: "Case file unavailable",
  }[caseStatus];

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
                  Phase 1
                </span>
              </div>

              <div className="grid gap-4 sm:grid-cols-3">
                <CourtSeat
                  title="Jurisdiction"
                  name={caseOverview?.jurisdiction ?? "Awaiting case file"}
                />
                <CourtSeat
                  title="Witnesses"
                  name={
                    caseOverview
                      ? `${caseOverview.witnesses.length} public witnesses`
                      : "Pending"
                  }
                />
                <CourtSeat
                  title="Counsel"
                  name={
                    caseOverview
                      ? caseOverview.player_roles.join(" / ")
                      : "Choose role later"
                  }
                />
              </div>
            </div>

            <div className="mt-10 border-t border-white/20 pt-6">
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#d9c28f]">
                Locked Case File
              </p>
              <p className="mt-3 max-w-2xl text-2xl font-semibold leading-tight sm:text-4xl">
                {caseOverview?.title ?? "The court is waiting for the case file."}
              </p>
              <p className="mt-4 max-w-3xl text-base leading-7 text-white/80">
                {caseOverview?.summary ??
                  "Public case details will appear here once the backend responds."}
              </p>
            </div>
          </section>

          <aside className="grid gap-5">
            <Panel title="Case File">
              <dl className="grid gap-3 text-sm">
                <InfoRow label="Status" value={caseStatusCopy} />
                <InfoRow
                  label="Charges"
                  value={caseOverview ? `${caseOverview.charges.length}` : "-"}
                />
                <InfoRow
                  label="Evidence"
                  value={caseOverview ? `${caseOverview.evidence.length}` : "-"}
                />
                <InfoRow
                  label="Timeline"
                  value={caseOverview ? `${caseOverview.timeline.length}` : "-"}
                />
              </dl>
            </Panel>

            <Panel title="Session Status">
              <dl className="grid gap-3 text-sm">
                <InfoRow label="Frontend" value="Next.js running" />
                <InfoRow label="Backend" value={statusCopy} />
                <InfoRow label="Service" value={serviceName} />
              </dl>
            </Panel>

            <Panel title="Charges">
              {caseOverview ? (
                <div className="space-y-4">
                  {caseOverview.charges.map((charge) => (
                    <section key={charge.id} className="border-b border-[#eadfc9] pb-4 last:border-0 last:pb-0">
                      <h3 className="text-base font-bold text-[#1f2528]">
                        {charge.name}
                      </h3>
                      <p className="mt-2 text-sm leading-6 text-[#3d4548]">
                        {charge.description}
                      </p>
                      <ul className="mt-3 grid gap-2 text-sm text-[#5d6669]">
                        {charge.legal_elements.map((element) => (
                          <li key={element.id}>
                            <strong className="text-[#1f2528]">
                              {element.name}:
                            </strong>{" "}
                            {element.description}
                          </li>
                        ))}
                      </ul>
                    </section>
                  ))}
                </div>
              ) : (
                <EmptyState status={caseStatus} />
              )}
            </Panel>

            <Panel title="Witnesses">
              {caseOverview ? (
                <div className="grid gap-3">
                  {caseOverview.witnesses.map((witness) => (
                    <CompactItem
                      key={witness.id}
                      title={witness.name}
                      meta={`${witness.role} | ${witness.statement_count} public statements`}
                      description={witness.bio}
                    />
                  ))}
                </div>
              ) : (
                <EmptyState status={caseStatus} />
              )}
            </Panel>

            <Panel title="Evidence">
              {caseOverview ? (
                <div className="grid gap-3">
                  {caseOverview.evidence.map((item) => (
                    <CompactItem
                      key={item.id}
                      title={item.title}
                      meta={`${item.type} | ${
                        item.admissibility_status ?? "Admissibility hidden"
                      }`}
                      description={item.description}
                    />
                  ))}
                </div>
              ) : (
                <EmptyState status={caseStatus} />
              )}
            </Panel>

            <Panel title="Timeline">
              {caseOverview ? (
                <ol className="grid gap-3">
                  {caseOverview.timeline.map((event) => (
                    <li
                      key={event.id}
                      className="grid grid-cols-[4.5rem_1fr] gap-3 border-b border-[#eadfc9] pb-3 text-sm last:border-0 last:pb-0"
                    >
                      <span className="font-bold text-[#7b1f2a]">
                        {event.timestamp}
                      </span>
                      <span className="leading-6 text-[#3d4548]">
                        {event.description}
                      </span>
                    </li>
                  ))}
                </ol>
              ) : (
                <EmptyState status={caseStatus} />
              )}
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

function CompactItem({
  title,
  meta,
  description,
}: {
  title: string;
  meta: string;
  description: string;
}) {
  return (
    <article className="border-b border-[#eadfc9] pb-3 last:border-0 last:pb-0">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
        <h3 className="text-base font-bold text-[#1f2528]">{title}</h3>
        <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[#7b1f2a]">
          {meta}
        </p>
      </div>
      <p className="mt-2 text-sm leading-6 text-[#3d4548]">{description}</p>
    </article>
  );
}

function EmptyState({ status }: { status: CaseStatus }) {
  return (
    <p className="text-sm leading-6 text-[#5d6669]">
      {status === "loading"
        ? "Loading public case data."
        : "Public case data is unavailable."}
    </p>
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
