from langchain_core.prompts import PromptTemplate
from ..services.state import State
from ..services.llm_gateway import llm

def decision_agent(state: State):
    discrepancy=state['mock_api_list']
    completeness= state['completeness_list']
    risk_indicator= state['risk_category']
    file_paths_len= len(state['file_path_list'])
    template="""
    You are a decision agent who analyse the parameters and inform the user where human review is required or not.
    Parameters:
    1. all mandatory documents - accident_description, claim_form, garage_estimate and vehicle_damage i.e. 4 documents
    2. No discrepancies
    3. risk indicator = LOW
    4. missing fields(completeness)
    Given the required data, if all conditions are met then return "Recommeded_For_Approval" else return "Human_Review_Required".
    number of documents : {file_path_len} \n
    completeness: {completeness}\n
    risk indicator: {risk_indicator}\n
    discrepancy: {discrepancy}
    return only "RECOMMENDED_FOR_APPROVAL" or "Human Review Required". No extra words.
    """
    prompt= PromptTemplate.from_template(template=template)
    chain= prompt|llm
    response= chain.invoke({"discrepancy":discrepancy, "completeness":completeness, "risk_indicator":risk_indicator, "file_path_len":file_paths_len})
    return {"decision":response.content}