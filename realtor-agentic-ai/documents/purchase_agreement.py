from typing import Dict, Anyfrom jinja2 import Template

class PurchaseAgreement:
def __init__(self, data: Dict[str, Any]):
self.data = data

def generate(self) -> str:
template = Template("""
REAL ESTATE PURCHASE AGREEMENT

Date: {{ current_date }}

1. PARTIES:
Buyer: {{ client_name }}
Seller: To be identified

2. PROPERTY:
Address: {{ property_address }}
Type: {{ property_type }}

3. PURCHASE PRICE AND TERMS:
List Price: ${{ list_price }}
Earnest Money Deposit: ${{ earnest_money }}

4. FINANCING:
Financing Type: {{ financing_type }}

5. CLOSING:
Closing Date: {{ closing_date }}
Inspection Period: {{ inspection_period }} days

6. CONTINGENCIES:
- Inspection Contingency: {{ inspection_period }} days
- Financing Contingency: 21 days
- Appraisal Contingency: 17 days

7. ADDITIONAL TERMS:
- Property to be sold in "as-is" condition unless otherwise stated
- All appliances included in sale
- Buyer to pay for title search and insurance

This Agreement is legally binding. All parties should review carefully before signing.

_________________________________
Buyer Signature

_________________________________
Seller Signature

Date: _______________
""")

from datetime import datetime
return template.render(
current_date=datetime.now().strftime("%Y-%m-%d"),
**self.data
)
