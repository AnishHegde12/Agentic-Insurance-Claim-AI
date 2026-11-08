from langgraph.prebuilt import create_agent, tool, tool_node
from typing import List
from ..services.llm_gateway import llm
from pydantic import BaseModel, Field
from ..services.state import State
import requests

@tool
def policy_data(policy_id:str):
    """
    This tool is used to fetch the policy data of specific policy
    """
    response= requests.get(f"http://localhost:8000/insurance/policy/{policy_id}")
    return response
@tool
def vehicle_data(vehicle_id:str):
    """
    This tool is used to fetch the vehicle data of specific vehicle
    """
    response= requests.get(f"http://localhost:8000/insurance/vehicle/{vehicle_id}")
    return response
@tool
def customer_data(customer_id:str):
    """
    This tool is used to fetch the customer data of specific customer
    """
    response= requests.get(f"http://localhost:8000/insurance/customer/{customer_id}")
    return response
@tool
def claim_history(customer_id:str):
    """
    This tool is used to fetch the claim history of the customer
    """
    response= requests.get(f"http://localhost:8000/insurance/claims/history/{customer_id}")
    return response
@tool
def garage_data(garage_id:str):
    """
    This tool is used to fetch the garage data of garage
    """
    response= requests.get(f"http://localhost:8000/insurance/garage/{garage_id}")
    return response
@tool
def repair_cost(vehicle_model:str, part_name:str):
    """
    This tool is used to fetch the repair cost of the vehicle part
    """
    response= requests.get(f"http://localhost:8000/insurance/repair-cost/{vehicle_model}/{part_name}")
    return response

class Data_List(BaseModel):
    discrepancies: List[str] = Field(description="List of the fields that are do not match with the extracted data.If the data is missing on either side or any 1 side then it is also a mismatch. if the field key is present and value is NA or similar to NA then it is not a mismatch. If there are no discrepancies, return an empty list.")
def mock_data_validation_agent(state:State):
    normalised_data= state['extracted_data']
    system_prompt=f"""
    You are a data validator who validates the data retrieved by the api against the normalised extracted data from the relevant documents.
    normalised extracted data: {normalised_data}
    \n
    for Policy Validation Check:
    1.Policy exists
    2.Policy is active
    3.Accident occurred within policy period
    4.Required coverage exists

    for vehicle validation:
    1. compare the register number in claim and retrieved from api.
    2. Validate:
    i. Registration number
    ii. Vehicle make
    iii.Vehicle model
    iv.Registered owner

    for Customer/Driver Validation Check:
    1. Customer identity
    2. Driver information
    3. Driving licence status

    for Claim-History Validation:
    1.Retrieve previous claims and determine:
    2. Number of previous claims
    3. Recent claims
    4. Repeated damage patterns
    5. Previous claim amounts

    for Damage Consistency Validation validate:
    compare accident description, image analysis and garage estimation from claim and then compare with garage estimation from api.

    for repair cost validation:
        Compare the garage estimate against reference prices.
        flag it when the difference exceeds the configured threshold.
    
        list if any discrepancy present.
    """
    tools= [policy_data, garage_data, vehicle_data, customer_data, claim_history, repair_cost]
    agent= create_agent(
        model= llm, tools=tools, response_format=Data_List
    )
    response=agent.invoke({"messages":[{"role":"user", "content":system_prompt}]})
    list= response['structured_response']
    return {"mock_api_list":list.discrepancies}