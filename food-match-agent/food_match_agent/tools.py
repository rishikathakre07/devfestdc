import os
import json
from datetime import datetime
from math import radians, sin, cos, atan2, sqrt
from typing import Dict, Any, List, Tuple, Optional

from .data_loader import load_restaurants, load_ngos, load_volunteers

LOGS_PATH = os.path.join(os.path.dirname(__file__), "logs", "logs.json")

# --- Distance helpers ---
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def maps_link(origin_lat, origin_lng, dest_lat, dest_lng) -> str:
    return f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}"

# ---- Core matching (single donation) ----
def _match_one_donation(donation: Dict[str, Any],
                        ngos_df,
                        volunteers_df) -> Dict[str, Any]:
    """
    donation keys expected:
      restaurant_id, restaurant_name, phone, food_item, quantity, unit, latitude, longitude
    """
    food_item = str(donation["food_item"]).strip().lower()
    qty = float(donation["quantity"])
    unit = donation["unit"]

    # filter NGOs requesting this exact item (string match, case-insensitive)
    ngo_candidates = ngos_df[ngos_df["requested_item"].str.strip().str.lower() == food_item].copy()
    if ngo_candidates.empty:
        return {
            "status": "no_ngo_requesting_item",
            "restaurant": donation["restaurant_name"],
            "food_item": donation["food_item"],
            "quantity": qty,
            "unit": unit,
            "timestamp": datetime.utcnow().isoformat()
        }

    # sort by priority rank, then distance
    ngo_candidates["distance_km"] = ngo_candidates.apply(
        lambda r: haversine_km(donation["latitude"], donation["longitude"], r["latitude"], r["longitude"]),
        axis=1
    )
    ngo_candidates = ngo_candidates.sort_values(["priority_rank", "distance_km"])

    # pick top NGO that still benefits (we're not doing multi-split in MVP)
    ngo_best = ngo_candidates.iloc[0].to_dict()

    # pick nearest available volunteer
    avail = volunteers_df[volunteers_df["available"]].copy()
    if avail.empty:
        return {
            "status": "no_volunteer_available",
            "restaurant": donation["restaurant_name"],
            "ngo": ngo_best["ngo_name"],
            "food_item": donation["food_item"],
            "quantity": qty,
            "unit": unit,
            "timestamp": datetime.utcnow().isoformat()
        }

    avail["vol_dist_km"] = avail.apply(
        lambda r: haversine_km(donation["latitude"], donation["longitude"], r["latitude"], r["longitude"]),
        axis=1
    )
    vol_best = avail.sort_values("vol_dist_km").iloc[0].to_dict()

    # prepare assignment
    assignment = {
        "status": "assigned",
        "timestamp": datetime.utcnow().isoformat(),

        # restaurant
        "restaurant_id": donation["restaurant_id"],
        "restaurant": donation["restaurant_name"],
        "restaurant_phone": donation["phone"],
        "restaurant_address": donation["address"],
        "restaurant_lat": donation["latitude"],
        "restaurant_lng": donation["longitude"],

        # item
        "food_item": donation["food_item"],
        "quantity": qty,
        "unit": unit,

        # ngo
        "ngo_id": ngo_best["ngo_id"],
        "ngo": ngo_best["ngo_name"],
        "ngo_type": ngo_best["type"],
        "ngo_phone": ngo_best["phone"],
        "ngo_address": ngo_best["address"],
        "ngo_lat": float(ngo_best["latitude"]),
        "ngo_lng": float(ngo_best["longitude"]),
        "ngo_priority": ngo_best["priority"],
        "dist_rest_ngo_km": round(float(ngo_best["distance_km"]), 2),
        "route_link_rest_to_ngo": maps_link(donation["latitude"], donation["longitude"], float(ngo_best["latitude"]), float(ngo_best["longitude"])),

        # volunteer
        "volunteer_id": vol_best["volunteer_id"],
        "volunteer": vol_best["name"],
        "volunteer_phone": vol_best["phone"],
        "volunteer_area": vol_best.get("area", ""),
        "vol_lat": float(vol_best["latitude"]),
        "vol_lng": float(vol_best["longitude"]),
        "dist_vol_to_rest_km": round(float(vol_best["vol_dist_km"]), 2),
        "route_link_vol_to_rest": maps_link(float(vol_best["latitude"]), float(vol_best["longitude"]), donation["latitude"], donation["longitude"])
    }

    # mark volunteer as busy in the in-memory frame so we don't reuse within this batch run
    volunteers_df.loc[volunteers_df["volunteer_id"] == vol_best["volunteer_id"], "available"] = False
    volunteers_df.loc[volunteers_df["volunteer_id"] == vol_best["volunteer_id"], "assigned_status"] = "assigned"

    return assignment

# ---- Batch matching for all restaurants (used by agent) ----
def perform_batch_matching() -> List[Dict[str, Any]]:
    restaurants = load_restaurants()
    ngos = load_ngos()
    volunteers = load_volunteers()

    results: List[Dict[str, Any]] = []
    for _, row in restaurants.iterrows():
        donation = {
            "restaurant_id": row["restaurant_id"],
            "restaurant_name": row["restaurant_name"],
            "address": row["address"],
            "phone": row["phone"],
            "food_item": row["food_item"],
            "quantity": row["quantity"],
            "unit": row["unit"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        }
        result = _match_one_donation(donation, ngos, volunteers)
        results.append(result)

    # persist logs (append-friendly array)
    os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)
    try:
        if os.path.exists(LOGS_PATH):
            with open(LOGS_PATH, "r") as f:
                old = json.load(f)
        else:
            old = []
    except Exception:
        old = []

    old.extend(results)
    with open(LOGS_PATH, "w") as f:
        json.dump(old, f, indent=2)

    return results
