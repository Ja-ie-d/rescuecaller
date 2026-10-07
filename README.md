# RescueCall AI — Emergency Report Triage (Simulation)

A **working, local-only hackathon prototype** that groups likely duplicate emergency reports and highlights potentially urgent incidents for human review.

> **Safety:** This is a simulation, **not** a real 911 product. Do not use it for real emergency triage or dispatch. The prioritization and grouping rules are heuristic and can be wrong.

## Run

Requires Python 3.9+; **no pip install needed**.

```bash
python app.py
```

Open **http://localhost:8000** in your browser.

## Live demo (2 minutes)

1. Open the dashboard: 18 preloaded simulated reports are grouped into incidents.
2. Show that multiple crash reports at the same intersection appear as **one incident**.
3. Note that the Union Square medical incident is marked **Critical**.
4. Click **Add report** to simulate a new caller reporting the same crash.
5. Watch the incoming report and duplicate counters update.
6. Click **Acknowledge**, **Verify**, or **Mark dispatched (demo)** to simulate dispatcher review.
7. Click **Reset demo** to restore the starting state.

## Technical flow

`Simulated reports → text/location/time comparison → duplicate groups → keyword severity hints → human review dashboard`

- **Backend:** Python standard-library HTTP server and JSON API.
- **Frontend:** Responsive HTML, CSS, JavaScript; polls every five seconds.
- **Duplicate heuristic:** same incident type + normalized location + within 20 minutes + basic text similarity. Groups may be inaccurate and must be verified.
- **Severity heuristic:** predefined keywords, not trained AI or clinically validated triage.
- **Data:** 18 fictional reports, stored in memory. All changes reset when server restarts.

## API

- `GET /api/incidents` — incident groups and counts
- `POST /api/reports` — create simulated report (`description`, `location`, `kind`)
- `POST /api/review` — update review status (`id`, `status`)
- `POST /api/reset` — restore initial simulated reports

## Next steps for a real research prototype

Add speech-to-text, sentence embeddings, geocoding, calibrated uncertainty, audit trails, authentication, and human validation using appropriately governed data. A production emergency response tool would require extensive safety testing, operational approval, and integration with dispatch systems.
