# Meal Bridge
Food delivery Agent
# 🍽️ Meal Bridge – AI-Powered Food Redistribution Platform

**DevFestDC 2025 Hackathon Project**  
Team: Rishika Thakre, Mukul Gupta, Anisha Katiyar, Meghna Gupta, Siddhi Rohan  


[![GitHub Repo](https://img.shields.io/badge/Repo-Link-blue)](https://github.com/rishikathakre07/devfestdc)

## Meal Bridge – From Waste to Wonder.
## Together, let’s bridge the gap between surplus and scarcity.


---

## 🌍 Problem Statement
Every day, tons of surplus food from restaurants, events, and households goes to waste while millions of people face hunger and food insecurity.  
Current donation platforms are fragmented, lack **real-time AI-powered matching**, and do not enforce **clear separation of cooked vs. raw food**—a critical requirement for food safety and compliance.

---

## 💡 Our Solution – Meal Bridge
**Meal Bridge** is an AI-powered redistribution platform that connects food donors with NGOs and communities in need.  
We leverage **Google AI Studio, Vertex AI, and Google Maps APIs** to ensure food reaches the right place at the right time.

**Core Features:**
- ✅ Donor portal with **separate sections for cooked & raw food**.  
- ✅ **AI-driven matching** between donors and NGOs based on demand, location, and food type.  
- ✅ **Route optimization** with Google Maps to minimize delivery time and carbon footprint.  
- ✅ **Real-time tracking** and transparency for donors & recipients.  
- ✅ Compliance with food safety guidelines (USDA / FDA).  

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
- **Frontend:** Flutter (mobile), React (web)  
- **Backend:** Node.js / Python (FastAPI)    
- **AI/ML:** Google AI Studio + Vertex AI  

---

## 🚀 Novelty & Differentiation
Meal Bridge stands out from existing food donation apps because of its **novel structure**:
1. **Cooked vs. Raw Food Separation** – avoids unsafe mixing of perishable vs. long-lasting items.  
2. **AI-Enhanced Matching** – demand prediction based on NGO history, demographics, and location.  
3. **Dynamic Route Optimization** – reduces costs, ensures timely delivery, and cuts CO₂ emissions.  
4. **Transparency & Trust** – real-time tracking and donor-recipient feedback loop.  
5. **Global Scalability** – modular architecture that works for small communities and large cities alike.  

---

## 🌱 Community Impact
- Reduces **food waste** and prevents landfill overflow.  
- Provides **meals for vulnerable communities** in real-time.  
- Strengthens NGOs with **data-driven insights**.  
- Directly supports **UN Sustainable Development Goals**:
  - SDG 2: Zero Hunger  
  - SDG 12: Responsible Consumption  
  - SDG 13: Climate Action  

---

## 📂 Repo Structure
devfestdc/
│
├── frontend/ # Flask
├── backend/ # Node.js / FastAPI backend services
├── ai_models/ # AI/ML models for matching & prediction
├── docs/ # Technical docs, design diagrams, proposal
├── datasets/ # Sample datasets (mock NGO & donor data)
├── README.md # Project overview
└── LICENSE
