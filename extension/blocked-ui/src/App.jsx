import { useEffect, useMemo, useState } from "react";

const API_BASE = "http://localhost:8000";

// Convert a date in a string into a date object.
function formatDate(dateString) {
    if (!dateString) {
        return "Unknown";
    }

    const date = new Date(dateString);
    if (Number.isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleDateString();
}

function buildRecommendations(company) {
    const recommendations = [];

    // Get score, rating and reports of a company.
    const score = company?.trust_score ?? 0;
    const rating = (company?.rating ?? "").toLowerCase();
    const reports = company?.reports ?? [];

    // Single out major reports.
    const majorReports = reports.filter(
        (report) => String(report.severity || "").toLowerCase() === "major"
    );

    // Give recommendations based on severity of the security flaw.
    if (rating === "critical") {
        recommendations.push(
            "Do not enter passwords, payment details, or recovery codes here."
        );
    }

    if (rating === "poor") {
        recommendations.push(
            "Avoid downloads, sign-ins, and actions that grant access to your personal information on computer."
        );
    }

    // Give recommendations based how many reports the company has.
    if (majorReports.length > 0) {
        recommendations.push(
            `This company has ${majorReports.length} major report(s) linked to it. Please review them before trusting trusting this site with sensitive information.`
        );
    }

    // Give recommendations based on the trust score.
    if (score < 40) {
        recommendations.push(
            "If you must continue visiting this site later, use a seperate trusted device and do not reuse passwords."
        );
    } else if (score < 70) {
        recommendations.push(
            "Be cautious with acconut recovery, downloads, and payment actions on this site."
        );
    } else {
        recommendations.push(
            "Continue following normal online safety procedures."
        );
    }

    return recommendations;
}

export default function App() {
    // Get the details of the current tab.
    const params = new URLSearchParams(window.location.search);
    const domain = params.get("domain") || "";
    const urlRating = params.get("rating") || "";

    // Set up details of the current company.
    const [company, setCompany] = useState(null);
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;

        async function loadCompany() {
            // No domain.
            if (!domain) {
                setLoading(false);
                setError("No domain provided");
                return;
            }

            setLoading(true);
            setError("");
            
            // Attempt to find the company's details with it's domain and reports.
            try {
                const response = await fetch(
                    `${API_BASE}/companies?domain=${encodeURIComponent(domain)}`
                );

                if (!response.ok) {
                    throw new Error(`Back-end returned ${response.status}.`);
                }

                const data = await response.json();
                
                const reportsResponse = await fetch(
                    `${API_BASE}/reports?company_id=${data.id}`
                );
                
                let reportsData = [];

                if (!reportsResponse.ok) {
                    throw new Error(`Back-end returned ${response.status}.`);
                }
                
                if (reportsResponse.ok) {
                    reportsData = await reportsResponse.json();

                    if (!Array.isArray(reportsData)) {
                        reportsData = reportsData ? [reportsData] : [];
                    }
                } else if (reportsResponse.status !== 400) {
                    throw new Error(`Reports lookup failed with ${reportsResponse.status}.`);
                }

                // If the process wasn't cancelled.
                if (!cancelled) {
                    setCompany(data);
                    setReports(reportsData);
                    setLoading(false);
                }
            } catch (error) {
                if (!cancelled) {
                    setError(error.message);
                    setLoading(false);
                }
            }
        }

        loadCompany();

        return () => {
            cancelled = true;
        };
    }, [domain]);

    // Get the company's information.
    const rating = (company?.rating || urlRating || "unknown").toLowerCase();
    const score = company?.trust_score ?? "--";

    const recommendations = useMemo(() => buildRecommendations(company, reports), [company, reports]);

    // Give the user a reason for the site blocking.
    const blockReason =
    rating === "critical"
        ? "This page was blocked automatically because WebTrust classified it as unsafe."
        : "This page was blocked because it is considered risky by WebTrust."

    return (
        <div className="page">
            <div className="card">
                <div className="badge">Site Blocked</div>

                <h1>WebTrust Blocked This Page</h1>
                <p className="lead">{blockReason}</p>
                
                {/*
                    Information about the company.
                */}
                <div className="grid">
                    <div className="info">
                        <span className="label">Name</span>
                        <span className="value">{company?.name || "Unknown"}</span>
                    </div>

                    <div className="info">
                        <span className="label">Domain</span>
                        <span className="value">{domain || "Unknown"}</span>
                    </div>

                    <div className="info">
                        <span className="label">Trust Score</span>
                        <span className="value">{score}</span>
                    </div>

                    <div className="info">
                        <span className="label">Rating</span>
                        <span className={`pill ${rating}`}>
                            {(company?.rating || urlRating || "Unknown").toString()}
                        </span>
                    </div>
                </div>
                
                {/*
                    Information about why the site was blocked.
                */}
                <div className="section">
                    <h2>Why It Was Blocked</h2>
                    <p>
                        WebTrust marked this site as unsafe based on its security measures, evidence of security breaches, and trust score.
                    </p>
                </div>

                <div className="section">
                    <h2>Linked Reports</h2>

                    {loading && <p>Loading report history...</p>}
                    {error && <p className="error">{error}</p>}

                    {!loading && !error && reports.length === 0 && (
                        <p>No public reports were found for this company.</p>
                    )}

                    {/*
                    Information about a company's reports.
                    */}
                    <div className="reports">
                        {reports.map((report) => (
                            <article key={report.id} className="report">
                                <div className="report-top">
                                    <strong>{report.title}</strong>
                                    <span className={`severity ${String(report.severity || "").toLowerCase()}`}>
                                        {report.severity}
                                    </span>
                                </div>

                                <div className="meta">
                                    <span>{formatDate(report.report_date)}</span>
                                    <span>{report.source}</span>
                                </div>

                                <p>{report.description}</p>
                            </article>
                        ))}
                    </div>
                </div>
                
                {/*
                    Recommendations on how to stay safe shile browsing the internet.
                */}
                <div className="section">
                    <h2>How To Stay Safe While Browsing</h2>

                    <ul className="tips">
                        {recommendations.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
                
                <div className="actions">
                    <button className="back" onClick={() => window.history.back()}>
                        Go back
                    </button>
                </div>

            </div>
        </div>
    );
}