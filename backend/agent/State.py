from typing import List, Any, Dict, Annotated, Optional
from typing_extensions import TypedDict
import operator


class InputState(TypedDict):
    question: str
    parsed_question: Dict[str, Any]
    sql_query: str
    results: List[Any]
    
class OutputState(TypedDict):
    question: str
    parsed_question: Dict[str, Any]
    sql_query: str
    sql_valid: bool
    sql_issues: str
    results: List[Any]
    answer: Annotated[str, operator.add]
    error: str