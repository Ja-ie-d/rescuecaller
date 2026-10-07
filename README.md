# 🚨 RescueCall AI — Emergency Report Triage

**RescueCall AI** is a hackathon prototype that organizes simulated emergency calls, groups possible duplicate reports, highlights potentially urgent incidents, and gives a dispatcher a dashboard for human review.

> **Simulation only:** Not connected to 911 or any real dispatch service. Matching and urgency labels are heuristic, may be wrong, and must not be used for real emergencies.

## 🌐 Try the Interactive Live Demo

[![Launch Live Demo](https://img.shields.io/badge/LAUNCH_LIVE_DEMO-Open_Dashboard-dc2626?style=for-the-badge)](https://Ja-ie-d.github.io/RescueCall-AI/)

**[▶ Open RescueCall AI in your browser](https://Ja-ie-d.github.io/RescueCall-AI/)**

Replace `YOUR-USERNAME` with your GitHub username. Enable **Settings → Pages → Deploy from a branch → main → / (root)**. For this no-install GitHub Pages demo, put the **standalone** `index.html` at the repository root. GitHub Pages hosts static HTML and does **not** run `app.py`.

## ✨ Features

- **18 fictional emergency reports** preloaded for demonstration
- **Potential duplicate detection** to group reports about the same incident
- **Urgency indicators** to highlight potentially critical situations
- **Dispatcher controls:** acknowledge, verify, or mark dispatched (simulation)
- **Live dashboard updates** when new fictional reports are added
- **Reset** to restore the original sample data
- **Responsive layout** for desktop and mobile

## 🔁 How It Works

`Receive simulated reports → Detect likely duplicates → Flag possible urgency → Display incident queue → Dispatcher reviews`

## 🎬 Two-Minute Demo

1. Open the **Live Demo** above.
2. Look at the incoming-report, incident, duplicate, and critical counters.
3. Open a crash incident to see multiple caller reports grouped together.
4. Submit another fictional report at the same location and incident type.
5. Watch the report and duplicate counts update.
6. Try **Acknowledge**, **Verify**, and **Mark dispatched**.
7. Press **Reset** to restore the sample data.

## 💻 Run the Python Backend Version Locally (Optional)

If you also include `app.py` and the **backend-compatible** `index.html` from the Python project, run:

```bash
python app.py
```

Then open **http://localhost:8000**. Requires Python 3.9+ and no third-party packages.

The backend version uses a Python standard-library HTTP server and JSON API; the GitHub Pages version is a **separate, standalone HTML/JavaScript demo**. Use the standalone `index.html` for GitHub Pages, rather than the backend-dependent HTML page.

### Backend API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/incidents` | Read incident groups and counts |
| POST | `/api/reports` | Add a simulated report |
| POST | `/api/review` | Update dispatcher review status |
| POST | `/api/reset` | Restore sample reports |

## 🛠 Technology

- **Frontend:** HTML, CSS, JavaScript
- **Standalone demo:** Browser-side simulated incident grouping and interaction
- **Optional backend:** Python standard library and JSON endpoints
- **Matching:** Rule-based heuristics, not a trained machine-learning model
- **Data:** Fictional reports; no real emergency-call integration

## 🚀 Future Improvements

Speech-to-text, semantic similarity models, location normalization, audit trails, role-based access, and rigorous human-reviewed safety evaluation.

---

**Built as a rapid-response hackathon proof of concept.**
