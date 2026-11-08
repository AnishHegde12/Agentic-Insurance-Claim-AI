import yaml
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from typing import List
from ..services.llm_gateway import llm
from pydantic import BaseModel, Field
from ..services.state import State
class Completeness(BaseModel):
    missing_fields: List[str] = Field(description="List of the fields that are missing from the claim data")
def completeness_agent(state:State):
    extracted_data= state['extracted_data']
    rules_path = Path(__file__).resolve().parents[2] / "data" / "rules" / "claim_rules.yaml"
    with open(rules_path, "r",encoding="utf-8") as file:
        data = yaml.safe_load(file)
    mandatory_fields= data['mandatory_fields']
    prompt_template="""
    You are a completeness agent who is expert in checking the completeness of the data collected from all the relevant documents against the mandatory fields of the claim rules.
    Your task is to check whether the provided data have all the mandatory fields.
    extracted_data: {extracted_data}\n
    rules:{mandatory_fields}
    """
    template= PromptTemplate.from_template(prompt_template)
    structured_llm= llm.with_structured_output(Completeness)
    chain = template|structured_llm
    response = chain.invoke({"extracted_data":extracted_data,"mandatory_fields":mandatory_fields })
    return {"completeness_list":response.missing_fields}