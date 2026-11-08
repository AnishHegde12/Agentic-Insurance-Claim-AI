from typing import Any, Dict, List, TypedDict

class State(TypedDict):
    file_path_list:List[str]
    image_base64: str
    extracted_data:str
    claim_id:str
    report:str
    completeness_list:List[str]
    mock_api_list:List[str]
    risk_score:float
    risk_category:str
    risk_description:str
    normalised_claim:Dict[str, Any]
    recommendation:str
    requires_hilt:bool
    report_path:str
    hilt_comment:str
    decision:str
    hilt_action:str
    
