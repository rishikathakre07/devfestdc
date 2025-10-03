# 🍽️ Meal Bridge – AI-Powered Food Redistribution Platform

**DevFestDC 2025 Hackathon Project**  
Team: Rishika Thakre, Mukul Gupta, Anisha Katiyar, Meghna Gupta, Siddhi Rohan  

[![GitHub Repo](https://img.shields.io/badge/Repo-Link-blue)](https://github.com/rishikathakre07/devfestdc)

---

## ✨ Vision
**Meal Bridge – From Waste to Wonder.**  
Together, let’s bridge the gap between surplus and scarcity.

---

## 🌍 Problem Statement
Every day, tons of surplus food from restaurants, fast food joints, cafeterias, and bakeries goes to waste, while millions of people at shelters, food banks, and homeless communities face hunger and food insecurity.  
Current donation systems are fragmented, lack **real-time matching**, and often don’t enforce **clear separation of cooked vs. raw food**, which is critical for safety and compliance.

---

## 💡 Our Solution
**Meal Bridge** is an **AI-powered redistribution platform** that connects food donors (restaurants, fast food outlets, cafeterias, events) with NGOs and shelters serving vulnerable communities. It also assigns volunteers automatically for pickup and delivery.

### Core Features
- ✅ Donor portal with **separate handling for cooked & raw food**.  
- ✅ **AI-driven matching** between donors and NGOs based on demand, food type, and location.  
- ✅ Volunteers chosen by **proximity to donor** for faster logistics.  
- ✅ **Google Maps integration** for optimized routing (volunteer → restaurant → NGO).  
- ✅ **Real-time JSON logs + web UI** for transparency and accountability.  

---

## 🖥️ Agent & UI

### Agent Matching in Action
<img width="2962" height="1640" alt="image" src="https://github.com/user-attachments/assets/c038bc7e-dc8a-44db-9830-cd0a5d46c41e" />

### Delivery Management UI

#### Orders Placed
<img width="1280" height="827" alt="image" src="https://github.com/user-attachments/assets/22fa66a1-a141-408f-b260-0292409dec5d" />

#### Order Details
<img width="554" height="664" alt="image" src="https://github.com/user-attachments/assets/f06c4643-7a1f-427f-b789-8082ff6326f7" />

#### Food Tracking
<img width="1280" height="827" alt="image" src="https://github.com/user-attachments/assets/f9ab275c-e427-4f1c-a1d4-4c025da2b5b3" />

---

## 🔬 Technical Architecture

**Tech Stack**
- **Data:** CSV-based donor, NGO, and volunteer tables (with location + phone numbers)  
- **Agent:** Google ADK Agent to perform matching and generate structured logs  
- **Backend:** Python + Flask providing REST endpoints  
- **Frontend:** Web UI displaying matches with NGO, donor, volunteer info, and Google Maps links  
- **Integration:** Assignments visible at `/` (UI) and `/api/assignments` (JSON API)  

---
## Flowchart

```
+----------------+
|     Start      |
+----------------+
        |
        v
+----------------+
|  Food Surplus  |
| (Donors log    |
|   details)     |
+----------------+
        |
        v
+----------------+
|  Meal Bridge   |
|   Platform     |
| (Data Ingestion)|
+----------------+
        |
        v
+----------------+
|  AI/ML Module  |
| (Demand Forecast,|
|   Matching,     |
|   Route Opt.)   |
+----------------+
        |
        v
+----------------+
| Platform Notifies|
| Recipient NGO  |
+----------------+
        |
        v
+------------------+
| Recipient Confirms? |
+------------------+
    | Yes  /   \ No
    v      /     \
+----------------+  +----------------+
| Generate Route |  |  Refine AI     |
|  (Google Maps) |  |   Models       |
+----------------+  +----------------+
        |                  ^
        v                  |
+----------------+         |
| Logistics Pick |---------+
|   Up Donation  |
+----------------+
        |
        v
+----------------+
| Logistics Deliver|
|  to Recipient  |
+----------------+
        |
        v
+----------------+
| Recipient      |
|  Distributes   |
|     Food       |
+----------------+
        |
        v
+----------------+
|  Community     |
|     Impact     |
| (Reduced Waste,|
|   SDG Goals)   |
+----------------+
        |
        v
+----------------+
|       End      |
+----------------+
```
## 🔬 Technical Architecture

### Tech Stack
- **Data**: CSV-based donor/NGO/volunteer tables (with location + contact).
- **Agent**: Google ADK Agent executes matching logic and generates structured logs.
- **Backend**: Python (Flask) serving REST endpoints.
- **Frontend**: Web UI rendering assignments with cards, priorities, phone numbers, and Google
Maps route links.
- **Integration**: All assignments visible live via / (UI) or /api/assignments.

---

## 🚀 Novelty & Differentiation
Meal Bridge goes beyond typical donation apps by introducing:

1. **Cooked vs. Raw Food Separation** – safer for shelters and NGOs.  
2. **AI-Enhanced Matching** – demand prediction and priority handling.  
3. **Route Optimization** – volunteers and donors paired using Google Maps routing.  
4. **Transparency** – real-time JSON logs + UI cards for all parties.  
5. **Hackathon-Ready Pipeline** – CSV → AI Agent → Flask UI in one working demo.  

---

## 🌱 Community Impact
- Prevents **waste of surplus food** from restaurants and cafeterias.  
- Provides **timely meals to shelters and homeless communities**.  
- Empowers NGOs with **data-driven coordination**.  
- Aligns with UN Sustainable Development Goals:  
  - **SDG 2:** Zero Hunger  
  - **SDG 12:** Responsible Consumption  
  - **SDG 13:** Climate Action  

---


