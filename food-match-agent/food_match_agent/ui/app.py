"""
app.py — Meal Bridge ✨ FULLY FIXED VERSION
Handles relative imports in your Python files
"""

import streamlit as st
import uuid
import sys
import os
from datetime import datetime
import pandas as pd
import json
from pathlib import Path

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Meal Bridge", layout="wide", page_icon="🍲")

# -------------------- FIX IMPORTS --------------------
# For Windows paths like: C:\Users\siddh\Downloads\devfestdc-main\...
SCRIPT_DIR = Path(__file__).parent.absolute()
PARENT_DIR = SCRIPT_DIR.parent  # food_match_agent folder
PROJECT_ROOT = PARENT_DIR.parent  # food-match-agent folder

# Add BOTH to path (this fixes relative imports)
for path in [str(PARENT_DIR), str(PROJECT_ROOT)]:
    if path not in sys.path:
        sys.path.insert(0, path)

st.sidebar.caption(f"📁 Script: {SCRIPT_DIR.name}")
st.sidebar.caption(f"📁 Parent: {PARENT_DIR.name}")

# Try to import the matching tools
AGENT_AVAILABLE = False
agent_error = None

try:
    # Import as a module (not relative)
    import tools
    import data_loader
    
    # Get the functions
    perform_batch_matching = tools.perform_batch_matching
    load_restaurants = data_loader.load_restaurants
    load_ngos = data_loader.load_ngos
    load_volunteers = data_loader.load_volunteers
    
    AGENT_AVAILABLE = True
    
except Exception as e:
    agent_error = str(e)
    
    with st.sidebar.expander("🔍 Debug Info"):
        st.code(f"Error: {e}")
        st.write("**Python Path:**")
        for p in sys.path[:3]:
            st.caption(p)

# -------------------- THEME & STYLES --------------------
CSS = """
<style>
:root{
  --bg: transparent;
  --glass: rgba(255,255,255,0.65);
  --border: rgba(0,0,0,0.07);
  --text: #0f172a;
  --muted:#475569;
  --brand:#2563eb;
  --accent:#22c55e;
  --warn:#f59e0b;
  --danger:#ef4444;
  --chip: rgba(37,99,235,0.12);
  --chip2: rgba(34,197,94,0.12);
}
@media (prefers-color-scheme: dark) {
  :root{
    --glass: rgba(17,24,39,0.62);
    --border: rgba(255,255,255,0.08);
    --text:#e5e7eb; --muted:#94a3b8;
    --chip: rgba(37,99,235,0.20);
    --chip2: rgba(34,197,94,0.18);
  }
}
.block-container{padding-top:1.1rem; padding-bottom:3rem;}
header[data-testid="stHeader"]{background:transparent;}
footer{visibility:hidden;}

.meal-header{
  border-radius:18px;
  padding:22px 22px 18px 22px;
  border:1px solid var(--border);
  background:
    radial-gradient(1200px 400px at 20% -5%, rgba(37,99,235,0.10), transparent),
    radial-gradient(900px 300px at 85% -10%, rgba(34,197,94,0.12), transparent),
    linear-gradient(135deg, rgba(37,99,235,0.08), rgba(34,197,94,0.06));
}
.meal-title{margin:0; font-size:30px; line-height:1.1;}
.meal-sub{margin:6px 0 0 0; color:var(--muted);}

.card{
  background: var(--glass);
  border:1px solid var(--border);
  border-radius:16px;
  padding:16px;
  margin:10px 0 14px 0;
  backdrop-filter: blur(8px);
}
.card h3{margin:0 0 8px 0; font-size:18px}

.role-chip{
  display:inline-flex; gap:8px; align-items:center;
  padding:6px 10px; border-radius:999px;
  background: var(--chip); border:1px solid var(--border);
  font-size:13px; margin-top:8px;
}
.badge{
  display:inline-block; padding:4px 8px; border-radius:8px;
  border:1px solid var(--border); font-size:12px; color:var(--muted);
}
.badge.waiting{color:#0ea5e9; background:rgba(14,165,233,0.08);}
.badge.success{color:#16a34a; background:rgba(22,163,74,0.08);}
.badge.urgent{color:#dc2626; background:rgba(220,38,38,0.10);}
.badge.assigned{color:#16a34a; background:rgba(22,163,74,0.08);}

.stButton > button, .stDownloadButton > button{
  border-radius:10px !important; padding:0.6rem 0.9rem !important;
  border:1px solid var(--border) !important;
}
.stTextInput input, .stNumberInput input,
.stTextArea textarea, .stSelectbox > div > div{
  border-radius:10px !important;
}

.note{
  border:1px solid var(--border); background:var(--glass);
  border-radius:12px; padding:10px 12px; margin-bottom:8px;
}
.note .time{ color:var(--muted); font-size:12px; }

.assignment-card{
  border:1px solid var(--border); background:var(--glass);
  border-radius:12px; padding:14px; margin-bottom:10px;
  backdrop-filter: blur(6px);
}
.assignment-card h4{margin:0 0 8px 0; font-size:16px;}
.assignment-detail{color:var(--muted); font-size:13px; margin:4px 0;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown(f"""
<div class="meal-header">
  <h1 class="meal-title">🍲 Meal Bridge</h1>
  <p class="meal-sub">A smart bridge between surplus meals and communities in need</p>
</div>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
def _init_state():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if "role" not in st.session_state: st.session_state.role = None
    if "username" not in st.session_state: st.session_state.username = None
    if "volunteers" not in st.session_state: st.session_state.volunteers = []
    if "restaurants" not in st.session_state: st.session_state.restaurants = []
    if "ngos" not in st.session_state: st.session_state.ngos = []
    if "assignments" not in st.session_state: st.session_state.assignments = []
    if "notifications" not in st.session_state:
        st.session_state.notifications = {"volunteer":[], "restaurant":[], "ngo":[]}
_init_state()

# -------------------- USER DB --------------------
USER_DB = {
    "vol1":  {"password": "volpass",  "role": "volunteer"},
    "rest1": {"password": "restpass", "role": "restaurant"},
    "ngo1":  {"password": "ngopass",  "role": "ngo"},
    "admin": {"password": "admin123", "role": "admin"},
}

# -------------------- HELPERS --------------------
def now_iso(): return datetime.utcnow().isoformat()

def push_note(role_key, to_name, msg):
    st.session_state.notifications[role_key].append({"to": to_name, "message": msg, "time": now_iso()})

def card(title:str, render, badge: str|None=None):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    title_html = f"<h3>{title}</h3>"
    if badge:
        title_html += f' <span class="badge {badge}">{badge.title()}</span>'
    st.markdown(title_html, unsafe_allow_html=True)
    render()
    st.markdown('</div>', unsafe_allow_html=True)

def sync_csv_with_session():
    """Write session state data to CSV files"""
    data_dir = PARENT_DIR / "data"
    data_dir.mkdir(exist_ok=True)
    
    try:
        if st.session_state.restaurants:
            rest_df = pd.DataFrame(st.session_state.restaurants)
            rest_df = rest_df.rename(columns={"id": "restaurant_id"})
            rest_df.to_csv(data_dir / "restaurant.csv", index=False)
        
        if st.session_state.ngos:
            ngo_df = pd.DataFrame(st.session_state.ngos)
            ngo_df = ngo_df.rename(columns={"id": "ngo_id"})
            ngo_df.to_csv(data_dir / "ngo.csv", index=False)
        
        if st.session_state.volunteers:
            vol_df = pd.DataFrame(st.session_state.volunteers)
            vol_df = vol_df.rename(columns={"id": "volunteer_id"})
            vol_df.to_csv(data_dir / "volunteer.csv", index=False)
        
        return True
    except Exception as e:
        st.error(f"CSV sync error: {e}")
        return False

def run_matching():
    """Run matching algorithm"""
    if not AGENT_AVAILABLE:
        st.error("❌ Agent not available")
        return None
    
    try:
        if not sync_csv_with_session():
            return None
        
        with st.spinner("🔄 Running matching..."):
            results = perform_batch_matching()
        
        st.session_state.assignments = results
        
        for assignment in results:
            if assignment.get("status") == "assigned":
                rest_name = assignment.get("restaurant")
                push_note("restaurant", rest_name, 
                         f"✅ {assignment['food_item']} matched! Volunteer: {assignment['volunteer']}")
                
                ngo_name = assignment.get("ngo")
                push_note("ngo", ngo_name,
                         f"📦 Incoming: {assignment['quantity']} {assignment['unit']} of {assignment['food_item']}")
                
                vol_name = assignment.get("volunteer")
                push_note("volunteer", vol_name,
                         f"🚗 Pick up {assignment['food_item']} from {rest_name}, deliver to {ngo_name}")
        
        return {"count": len(results), "results": results}
    except Exception as e:
        st.error(f"❌ Matching error: {e}")
        return None

# -------------------- LOGIN --------------------
if not st.session_state.authenticated:
    def login_body():
        role = st.selectbox("Select your role", ["Volunteer", "Restaurant", "NGO", "Admin"])
        c1, c2 = st.columns(2)
        with c1: username = st.text_input("Username")
        with c2: password = st.text_input("Password", type="password")
        
        st.info("💡 vol1/volpass, rest1/restpass, ngo1/ngopass, admin/admin123")
        
        if st.button("Login", use_container_width=True):
            user = USER_DB.get(username)
            if not user or user["password"] != password:
                st.error("Invalid credentials")
            elif user["role"] != role.lower():
                st.error("Role mismatch")
            else:
                st.session_state.username = username
                st.session_state.role = user["role"]
                st.session_state.authenticated = True
                st.rerun()
    card("🔐 Login to Meal Bridge", login_body)

# -------------------- SIDEBAR --------------------
if st.session_state.authenticated:
    with st.sidebar:
        st.markdown(f"""
        <div class="card">
          <div class="role-chip">👤 {st.session_state.username} • {st.session_state.role.title()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if AGENT_AVAILABLE:
            st.success("✅ Agent Ready")
        else:
            st.error("❌ Agent Not Available")
        
        if st.button("Logout", use_container_width=True):
            for k in ["authenticated","role","username"]:
                st.session_state.pop(k, None)
            st.rerun()

# ==================== ADMIN DASHBOARD ====================
if st.session_state.authenticated and st.session_state.role == "admin":
    st.subheader("🎯 Admin Dashboard")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Restaurants", len(st.session_state.restaurants))
    with cols[1]:
        st.metric("NGOs", len(st.session_state.ngos))
    with cols[2]:
        st.metric("Volunteers", len(st.session_state.volunteers))
    with cols[3]:
        assigned = len([a for a in st.session_state.assignments if a.get("status") == "assigned"])
        st.metric("Assignments", assigned)
    
    def coordinator_actions():
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🚀 Run Matching", use_container_width=True, type="primary", disabled=not AGENT_AVAILABLE):
                result = run_matching()
                if result:
                    assigned = len([a for a in result['results'] if a.get('status') == 'assigned'])
                    st.success(f"✅ Complete! {assigned}/{result.get('count', 0)} assignments")
                    st.rerun()
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
    
    card("🎮 Control Center", coordinator_actions)
    
    def show_assignments():
        assignments = [a for a in st.session_state.assignments if a.get("status") == "assigned"]
        if assignments:
            for idx, a in enumerate(assignments[-5:], 1):
                st.markdown(f"""
                <div class="assignment-card">
                    <h4>#{idx} <span class="badge assigned">Assigned</span></h4>
                    <div class="assignment-detail">🍽️ {a.get('restaurant')} → 🏥 {a.get('ngo')}</div>
                    <div class="assignment-detail">📦 {a.get('quantity')} {a.get('unit')} of {a.get('food_item')}</div>
                    <div class="assignment-detail">🚗 {a.get('volunteer')} ({a.get('volunteer_phone')})</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No assignments yet. Add data and run matching.")
    
    card("📋 Recent Assignments", show_assignments)
    
    def show_data():
        tab1, tab2, tab3 = st.tabs(["Restaurants", "NGOs", "Volunteers"])
        with tab1:
            if st.session_state.restaurants:
                st.dataframe(pd.DataFrame(st.session_state.restaurants), use_container_width=True)
            else:
                st.info("No data")
        with tab2:
            if st.session_state.ngos:
                st.dataframe(pd.DataFrame(st.session_state.ngos), use_container_width=True)
            else:
                st.info("No data")
        with tab3:
            if st.session_state.volunteers:
                st.dataframe(pd.DataFrame(st.session_state.volunteers), use_container_width=True)
            else:
                st.info("No data")
    
    card("📊 All Data", show_data)

# ==================== VOLUNTEER DASHBOARD ====================
if st.session_state.authenticated and st.session_state.role == "volunteer":
    cols = st.columns(3)
    with cols[0]:
        my_assignments = [a for a in st.session_state.assignments 
                         if a.get("volunteer") == st.session_state.username and a.get("status") == "assigned"]
        st.metric("Assignments", len(my_assignments))
    with cols[1]:
        my_profile = [v for v in st.session_state.volunteers if v["name"] == st.session_state.username]
        status = my_profile[0]["assigned_status"] if my_profile else "unregistered"
        st.metric("Status", status.title())
    with cols[2]:
        my_notes = [n for n in st.session_state.notifications["volunteer"] if n["to"] == st.session_state.username]
        st.metric("Notifications", len(my_notes))

    def volunteer_form():
        with st.form("volunteer_form"):
            name = st.text_input("Name", value=st.session_state.username)
            phone = st.text_input("Phone")
            area = st.text_input("Area")
            assigned_status = st.selectbox("Status", ["available", "assigned", "unavailable"], index=0)
            c1, c2 = st.columns(2)
            with c1:
                latitude = st.number_input("Latitude", value=38.895100, format="%.6f")
            with c2:
                longitude = st.number_input("Longitude", value=-77.036400, format="%.6f")
            if st.form_submit_button("Save Profile"):
                if name and phone:
                    entry = {
                        "volunteer_id": str(uuid.uuid4())[:8], "name": name, "phone": phone, "area": area,
                        "assigned_status": assigned_status, "latitude": float(latitude),
                        "longitude": float(longitude), "timestamp": now_iso()
                    }
                    st.session_state.volunteers = [v for v in st.session_state.volunteers if v["name"] != name]
                    st.session_state.volunteers.append(entry)
                    st.success("✅ Saved")
                    st.rerun()
                else:
                    st.error("Name and phone required")
    card("🧑‍🤝‍🧑 Volunteer Profile", volunteer_form)

    def volunteer_assignments():
        my_assignments = [a for a in st.session_state.assignments 
                         if a.get("volunteer") == st.session_state.username and a.get("status") == "assigned"]
        if my_assignments:
            for idx, a in enumerate(my_assignments, 1):
                st.markdown(f"""
                <div class="assignment-card">
                    <h4>Assignment #{idx}</h4>
                    <div class="assignment-detail">📍 Pick up: {a.get('restaurant')} ({a.get('restaurant_phone')})</div>
                    <div class="assignment-detail">📦 {a.get('quantity')} {a.get('unit')} of {a.get('food_item')}</div>
                    <div class="assignment-detail">🎯 Deliver to: {a.get('ngo')} ({a.get('ngo_phone')})</div>
                    <div class="assignment-detail">📏 Distance: {a.get('dist_vol_to_rest_km')} km</div>
                    <div class="assignment-detail">🗺️ <a href="{a.get('route_link_vol_to_rest')}" target="_blank">Route</a></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No assignments")
    card("📦 My Assignments", volunteer_assignments)

    def volunteer_notes():
        notes = [n for n in st.session_state.notifications["volunteer"] if n["to"] == st.session_state.username]
        if notes:
            for n in reversed(notes[-5:]):
                st.markdown(f'<div class="note">{n["message"]}<div class="time">{n["time"][:19]}</div></div>', unsafe_allow_html=True)
        else:
            st.write("No notifications")
    card("🔔 Notifications", volunteer_notes)

# ==================== RESTAURANT DASHBOARD ====================
if st.session_state.authenticated and st.session_state.role == "restaurant":
    cols = st.columns(3)
    with cols[0]:
        mine = [r for r in st.session_state.restaurants if r["restaurant_name"] == st.session_state.username]
        st.metric("Posts", len(mine))
    with cols[1]:
        matched = len([a for a in st.session_state.assignments 
                      if a.get("restaurant") == st.session_state.username and a.get("status") == "assigned"])
        st.metric("Matched", matched)
    with cols[2]:
        my_notes = [n for n in st.session_state.notifications["restaurant"] if n["to"] == st.session_state.username]
        st.metric("Notifications", len(my_notes))

    def restaurant_form():
        with st.form("restaurant_form"):
            restaurant_name = st.text_input("Restaurant Name", value=st.session_state.username)
            type_ = st.selectbox("Type", ["Restaurant", "Cafe", "Bakery"])
            address = st.text_input("Address")
            phone = st.text_input("Phone")
            food_item = st.text_input("Food Item")
            c1, c2 = st.columns(2)
            with c1:
                quantity = st.number_input("Quantity", min_value=1, value=10)
            with c2:
                unit = st.selectbox("Unit", ["each", "kg", "packs", "loaves", "liters", "bags"])
            g1, g2 = st.columns(2)
            with g1:
                latitude = st.number_input("Latitude", value=38.891300, format="%.6f")
            with g2:
                longitude = st.number_input("Longitude", value=-77.032500, format="%.6f")
            if st.form_submit_button("Log Availability"):
                if restaurant_name and phone and food_item:
                    entry = {
                        "restaurant_id": str(uuid.uuid4())[:8],
                        "restaurant_name": restaurant_name, "type": type_,
                        "address": address, "phone": phone, "food_item": food_item,
                        "quantity": int(quantity), "unit": unit,
                        "latitude": float(latitude), "longitude": float(longitude),
                        "status": "waiting", "timestamp": now_iso()
                    }
                    st.session_state.restaurants.append(entry)
                    st.success("✅ Logged")
                    st.rerun()
                else:
                    st.error("Fill required fields")
    card("🍽️ Log Surplus Food", restaurant_form)

    def restaurant_status():
        mine = [r for r in st.session_state.restaurants if r["restaurant_name"] == st.session_state.username]
        if mine:
            st.dataframe(pd.DataFrame(mine), use_container_width=True)
        else:
            st.info("No entries")
    card("📊 Your Posts", restaurant_status)

    def restaurant_matches():
        my_matches = [a for a in st.session_state.assignments 
                     if a.get("restaurant") == st.session_state.username and a.get("status") == "assigned"]
        if my_matches:
            for idx, a in enumerate(my_matches, 1):
                st.markdown(f"""
                <div class="assignment-card">
                    <h4>Match #{idx}</h4>
                    <div class="assignment-detail">📦 {a.get('quantity')} {a.get('unit')} of {a.get('food_item')}</div>
                    <div class="assignment-detail">🏥 To: {a.get('ngo')} ({a.get('ngo_type')})</div>
                    <div class="assignment-detail">🚗 Volunteer: {a.get('volunteer')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matches")
    card("🎯 Your Matches", restaurant_matches)

    def restaurant_notes():
        notes = [n for n in st.session_state.notifications["restaurant"] if n["to"] == st.session_state.username]
        if notes:
            for n in reversed(notes[-5:]):
                st.markdown(f'<div class="note">{n["message"]}<div class="time">{n["time"][:19]}</div></div>', unsafe_allow_html=True)
        else:
            st.write("No notifications")
    card("🔔 Notifications", restaurant_notes)

# ==================== NGO DASHBOARD ====================
if st.session_state.authenticated and st.session_state.role == "ngo":
    cols = st.columns(3)
    with cols[0]:
        my_requests = [d for d in st.session_state.ngos if d["ngo_name"] == st.session_state.username]
        total = sum(d["quantity"] for d in my_requests) if my_requests else 0
        st.metric("Requested", total)
    with cols[1]:
        matched = len([a for a in st.session_state.assignments 
                      if a.get("ngo") == st.session_state.username and a.get("status") == "assigned"])
        st.metric("Matched", matched)
    with cols[2]:
        my_notes = [n for n in st.session_state.notifications["ngo"] if n["to"] == st.session_state.username]
        st.metric("Notifications", len(my_notes))

    def ngo_form():
        with st.form("ngo_form"):
            ngo_name = st.text_input("NGO Name", value=st.session_state.username)
            type_ = st.selectbox("Type", ["Homeless Shelter", "Food Pantry", "Community Kitchen"])
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            requested_item = st.text_input("Requested Item (must match exactly!)")
            c1, c2, c3 = st.columns(3)
            with c1:
                quantity = st.number_input("Quantity", min_value=1, value=20)
            with c2:
                unit = st.selectbox("Unit", ["each", "kg", "packs", "loaves", "liters", "bags"])
            with c3:
                priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"], index=1)
            g1, g2 = st.columns(2)
            with g1:
                latitude = st.number_input("Latitude", value=38.889500, format="%.6f")
            with g2:
                longitude = st.number_input("Longitude", value=-77.035300, format="%.6f")
            if st.form_submit_button("Submit Request"):
                if ngo_name and phone and requested_item:
                    entry = {
                        "ngo_id": str(uuid.uuid4())[:8],
                        "ngo_name": ngo_name, "type": type_,
                        "phone": phone, "address": address, "requested_item": requested_item,
                        "quantity": int(quantity), "unit": unit, "priority": priority,
                        "latitude": float(latitude), "longitude": float(longitude),
                        "timestamp": now_iso()
                    }
                    st.session_state.ngos.append(entry)
                    st.success("✅ Recorded")
                    st.rerun()
                else:
                    st.error("Fill required fields")
    card("🏥 Request Food", ngo_form)

    def ngo_matches():
        my_matches = [a for a in st.session_state.assignments 
                     if a.get("ngo") == st.session_state.username and a.get("status") == "assigned"]
        if my_matches:
            for idx, a in enumerate(my_matches, 1):
                st.markdown(f"""
                <div class="assignment-card">
                    <h4>Incoming #{idx}</h4>
                    <div class="assignment-detail">📦 {a.get('quantity')} {a.get('unit')} of {a.get('food_item')}</div>
                    <div class="assignment-detail">🍽️ From: {a.get('restaurant')}</div>
                    <div class="assignment-detail">🚗 Volunteer: {a.get('volunteer')} ({a.get('volunteer_phone')})</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matches")
    card("📦 Incoming", ngo_matches)

    def ngo_notes():
        notes = [n for n in st.session_state.notifications["ngo"] if n["to"] == st.session_state.username]
        if notes:
            for n in reversed(notes[-5:]):
                st.markdown(f'<div class="note">{n["message"]}<div class="time">{n["time"][:19]}</div></div>', unsafe_allow_html=True)
        else:
            st.write("No notifications")
    card("🔔 Notifications", ngo_notes)
