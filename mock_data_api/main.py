from fastapi import FastAPI, HTTPException
from mock_data.policies import POLICIES
from mock_data.customers import CUSTOMERS
from mock_data.vehicles import VEHICLES
from mock_data.claim_history import CLAIM_HISTORY
from mock_data.garages import GARAGES
from mock_data.repair_costs import REPAIR_COSTS

app = FastAPI(title="Mock Insurance Core APIs")

def get_or_404(data, key, label):
    if key not in data:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return data[key]

@app.get("/insurance/policy/{policy_id}")
def policy(policy_id: str):
    return get_or_404(POLICIES, policy_id, "Policy")

@app.get("/insurance/customer/{customer_id}")
def customer(customer_id: str):
    return get_or_404(CUSTOMERS, customer_id, "Customer")

@app.get("/insurance/vehicle/{vehicle_id}")
def vehicle(vehicle_id: str):
    return get_or_404(VEHICLES, vehicle_id, "Vehicle")

@app.get("/insurance/claims/history/{customer_id}")
def claims(customer_id: str):
    return {"customer_id": customer_id, "previous_claims": CLAIM_HISTORY.get(customer_id, [])}

@app.get("/insurance/garage/{garage_id}")
def garage(garage_id: str):
    return get_or_404(GARAGES, garage_id, "Garage")

@app.get("/insurance/repair-cost/{vehicle_model}/{part_name}")
def repair_cost(vehicle_model: str, part_name: str):
    model = REPAIR_COSTS.get(vehicle_model)
    if not model or part_name not in model:
        raise HTTPException(status_code=404, detail="Reference repair cost not found")
    return {"vehicle_model": vehicle_model, "part_name": part_name, "reference_cost": model[part_name]}
