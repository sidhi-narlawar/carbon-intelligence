from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import SessionLocal, Activity, Supplier

app = FastAPI(
    title="Carbon Intelligence Platform",
    description="Environmental Intelligence and Carbon Accounting Platform",
    version="1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------- EMISSION FACTORS ----------------

EMISSION_FACTORS = {
    "Electricity": {
        "factor": 0.82,
        "unit": "kWh",
        "scope": 2
    },
    "Diesel": {
        "factor": 2.68,
        "unit": "litre",
        "scope": 1
    },
    "Natural Gas": {
        "factor": 1.90,
        "unit": "m3",
        "scope": 1
    },
    "Business Travel": {
        "factor": 0.21,
        "unit": "km",
        "scope": 3
    },
    "Transportation": {
        "factor": 0.15,
        "unit": "km",
        "scope": 3
    }
}


# ---------------- REQUEST MODELS ----------------

class ActivityRequest(BaseModel):
    activity_type: str
    amount: float
    date: str


class SupplierRequest(BaseModel):
    name: str
    category: str
    emissions: float
    carbon_score: float


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Carbon Intelligence Platform is running",
        "login": "/static/login.html"
    }


# ---------------- EMISSION FACTORS ----------------

@app.get("/api/factors")
def get_factors():
    return EMISSION_FACTORS


# ---------------- ACTIVITIES ----------------

@app.post("/api/activities")
def add_activity(data: ActivityRequest):

    if data.activity_type not in EMISSION_FACTORS:
        return {
            "error": "Invalid activity type"
        }

    factor_data = EMISSION_FACTORS[data.activity_type]

    # Carbon calculation
    emissions = data.amount * factor_data["factor"]

    activity = Activity(
        activity_type=data.activity_type,
        amount=data.amount,
        unit=factor_data["unit"],
        scope=factor_data["scope"],
        emission_factor=factor_data["factor"],
        emissions=emissions,
        date=data.date
    )

    db = SessionLocal()

    db.add(activity)
    db.commit()
    db.refresh(activity)

    db.close()

    return {
        "id": activity.id,
        "activity": activity.activity_type,
        "scope": activity.scope,
        "emissions": activity.emissions
    }


@app.get("/api/activities")
def get_activities():

    db = SessionLocal()

    activities = db.query(Activity).all()

    db.close()

    return [
        {
            "id": a.id,
            "activity": a.activity_type,
            "amount": a.amount,
            "unit": a.unit,
            "scope": a.scope,
            "factor": a.emission_factor,
            "emissions": a.emissions,
            "date": a.date
        }
        for a in activities
    ]


# ---------------- DASHBOARD ----------------

@app.get("/api/dashboard")
def dashboard():

    db = SessionLocal()

    activities = db.query(Activity).all()

    db.close()

    scope1 = sum(
        a.emissions for a in activities
        if a.scope == 1
    )

    scope2 = sum(
        a.emissions for a in activities
        if a.scope == 2
    )

    scope3 = sum(
        a.emissions for a in activities
        if a.scope == 3
    )

    total = scope1 + scope2 + scope3

    return {
        "total": round(total, 2),
        "scope1": round(scope1, 2),
        "scope2": round(scope2, 2),
        "scope3": round(scope3, 2),
        "activities": len(activities)
    }


# ---------------- AI / ANOMALY DETECTION ----------------

@app.get("/api/anomalies")
def anomalies():

    db = SessionLocal()

    activities = db.query(Activity).all()

    db.close()

    results = []

    for a in activities:

        # Simple anomaly detection rule
        if (
            a.activity_type == "Electricity"
            and a.amount > 20000
        ):
            results.append({
                "activity": a.activity_type,
                "amount": a.amount,
                "message": "Unusually high electricity consumption detected"
            })

    return results


# ---------------- REDUCTION SCENARIO ----------------

@app.get("/api/scenario")
def scenario(reduction: float):

    db = SessionLocal()

    activities = db.query(Activity).all()

    db.close()

    current = sum(
        a.emissions for a in activities
    )

    reduction_amount = current * (
        reduction / 100
    )

    projected = current - reduction_amount

    return {
        "current_emissions": round(current, 2),
        "reduction_percent": reduction,
        "reduction_amount": round(
            reduction_amount, 2
        ),
        "projected_emissions": round(
            projected, 2
        )
    }


# ---------------- SUPPLIERS ----------------

@app.post("/api/suppliers")
def add_supplier(data: SupplierRequest):

    db = SessionLocal()

    supplier = Supplier(
        name=data.name,
        category=data.category,
        emissions=data.emissions,
        carbon_score=data.carbon_score
    )

    db.add(supplier)

    db.commit()

    db.refresh(supplier)

    db.close()

    return {
        "id": supplier.id,
        "name": supplier.name,
        "category": supplier.category,
        "emissions": supplier.emissions,
        "carbon_score": supplier.carbon_score
    }


@app.get("/api/suppliers")
def get_suppliers():

    db = SessionLocal()

    suppliers = db.query(Supplier).all()

    db.close()

    return [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "emissions": s.emissions,
            "carbon_score": s.carbon_score
        }
        for s in suppliers
    ]