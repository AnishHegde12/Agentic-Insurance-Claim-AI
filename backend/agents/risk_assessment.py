from pydantic import BaseModel, Field
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from ..services.state import State
from ..services.llm_gateway import llm
import yaml
class risk_details(BaseModel):
    risk_score: float = Field(description="the score ranges from 0 to 1.")
    risk_indicator:str=Field(description="The indicator should be from the given levels")
    risk_description: str = Field(description="explain the risk indicators.")
def risk_assessment(state:State):
    normalised_claim= state['normalised_claim']
    rules_path = Path(__file__).resolve().parents[2] / "data" / "rules" / "risk_rules.yaml"
    with open(rules_path, "r",encoding="utf-8") as file:
        data = yaml.safe_load(file)
        rules= data['risk_rules']
        level = data['risk_levels']
    template="""
    You are a risk assessment agent that assess the given insurance claim using the rules provided and provide the following:
    1. Risk score
    2. Risk indicator
    3. Risk explanation
    Calculate the score by adding the points mentioned in the rules for each rule.
    insurance claim: {normalised_claim}\n\n
    rules: {rules}
    level: {level}
    You only need to return the Risk score, Risk indicator,Risk explanation and nothing else.
    """
    prompt= PromptTemplate.from_template(template=template)
    llm1= llm.with_structured_output(risk_details)
    chain= prompt|llm1
    response= chain.invoke({"normalised_claim":normalised_claim, "rules":rules, "level":level})
    return {"risk_score": response.risk_score, "risk_category":response.risk_indicator, "risk_description":response.risk_description}
