from ..services.llm_gateway import llm
from ..services.state import State
import json
from langchain_core.messages import HumanMessage
def normalise_agent(state:State):
    extracted_data= state['extracted_data']
    image= state['image_base64']
    prompt_template=f"""
    You are a normalisation agent who is expert in analyzing the data including image collected from all the relevant document for insurance calim.
    your task is to normalise the provided data into a layman's language and it's format. Analyze all the given data precisely and accurately. 
    extracted_data: {extracted_data}
    use the extracted data to normalise the claim and provide the output in a Json format with no backticks and extra text.
    The output should be a JSON object with the following keys if present else don't include the key in output but make sure that all the necessary detail even not mentioned in the keys are present in the output:
    - claim_id
    - policy_id
    - registration_number
    - accident_date
    - accident_description
    - claimed_damage
    - garage_estimate
    - damage_image
    """
    message=[{"type":"text","text":prompt_template}]
    if image:
        message.append({"type":"image_url", "image_url":{"url":f"data:image/png;base64,{image}"}})
    template=[HumanMessage(content=message)]
    response=json.loads(llm.invoke(template).content)
    claim_id= response.get("claim_id", "")
    return {"claim_id":claim_id,"normalised_claim":json.loads(response)}
