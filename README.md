# 🚨 RescueCall AI

**Emergency Report Triage & Duplicate Detection — Interactive Hackathon Demo**

RescueCall AI is a simulated emergency response dashboard designed to help dispatchers review high volumes of incoming reports. It groups potentially duplicate reports, highlights potentially life-threatening incidents, and keeps a human dispatcher in control of decisions.

## 🔴 Try the Live Demo

[![Launch Live Demo](https://img.shields.io/badge/LAUNCH_LIVE_DEMO-RescueCall_AI-E53935?style=for-the-badge)](https://ja-ie-d.github.io/rescuecaller/)

**👉 [Open the interactive RescueCall AI dashboard](https://ja-ie-d.github.io/rescuecaller/)**

## ✨ Features

- **Simulated emergency reports:** Explore an initial set of 18 sample reports.
- **Potential duplicate grouping:** Reports about the same incident can be grouped for review.
- **Priority indicators:** Highlights reports that may involve serious danger.
- **Dispatcher controls:** Acknowledge, verify, and mark incidents as dispatched in the demo.
- **Interactive dashboard:** Add simulated reports and watch incident counts update.

## 🔄 How It Works

1. **Receive:** A simulated caller report enters the dashboard.
2. **Analyze:** The system checks the report type, location, and urgency keywords.
3. **Group:** Reports with matching incident details are flagged as potential duplicates.
4. **Prioritize:** Potentially urgent cases appear higher in the incident queue.
5. **Review:** A dispatcher verifies the information and chooses the next action.

## 🧪 Example

Seven reports describing the same vehicle collision may appear as one incident with six potential duplicates, rather than seven unrelated emergencies. The dispatcher can expand the incident to review each report.

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** GitHub Pages
- **Prototype logic:** Rule-based duplicate grouping and urgency keyword matching
- **Data:** Simulated emergency reports

This standalone demo does not require a server, API key, or database.

## 💻 Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Ja-ie-d/rescuecaller.git
   ```
2. Open the repository folder.
3. Open `index.html` in your browser.

Alternatively, use the [live demo](https://ja-ie-d.github.io/rescuecaller/).

## 🎯 Hackathon Goal

Demonstrate how a lightweight triage interface can reduce repetitive information and help dispatchers review potentially critical emergencies more efficiently during a surge in calls.

## ⚠️ Safety & Limitations

**This is a hackathon simulation, not a real 911 service.** It does not contact emergency responders, connect to live emergency systems, or make real dispatch decisions. Duplicate detection and priority labels are heuristic and can be wrong. A trained human must verify reports and decide on appropriate actions. No claims of operational reliability or real-world response-time improvements are made.

## 🔗 Project Links

- **Live demo:** https://ja-ie-d.github.io/rescuecaller/
- **GitHub repository:** https://github.com/Ja-ie-d/rescuecaller
