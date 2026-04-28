from typing import Dict, Any, Listfrom .base_agent import BaseAgent
from ..models.conversation_state import ConversationState
from ..models.property_data import PropertyData

class ConversationAgent(BaseAgent):
def __init__(self):
super().__init__()
self.state = ConversationState()
self.questions = {
"property_address": "What is the full property address?",
"property_type": "Is this a single-family home, condo, or multi-family property?",
"list_price": "What is the listing price?",
"client_name": "What is the client's full name?",
"client_type": "Are you the buyer or seller?",
"closing_date": "What's the desired closing date? (YYYY-MM-DD)",
"earnest_money": "What amount is being offered as earnest money deposit?",
"inspection_period": "How many days for inspection contingency?",
"financing_type": "What type of financing will be used? (Conventional/FHA/VA/Cash)"
}

async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
response = input_data.get("message", "")
current_field = self.state.current_field

if current_field and current_field in self.questions:
self.state.responses[current_field] = response
self.state.completed_fields.append(current_field)

# Determine next question
next_field = self._get_next_field()

if next_field:
self.state.current_field = next_field
return {
"type": "question",
"field": next_field,
"question": self.questions[next_field],
"progress": len(self.state.completed_fields) / len(self.questions)
}
else:
# All questions answered, create property data
property_data = PropertyData(**self.state.responses)
return {
"type": "complete",
"data": property_data.dict(),
"message": "I have all the information needed. Ready to generate documents!"
}

def _get_next_field(self) -> str:
for field in self.questions.keys():
if field not in self.state.completed_fields:
return field
return None
