from typing import Dict, Any, Listfrom .base_agent import BaseAgent
from ..documents.purchase_agreement import PurchaseAgreement
from ..documents.listing_agreement import ListingAgreement
from ..documents.disclosure_form import DisclosureForm
from ..utils.pdf_generator import PDFGenerator

class DocumentAgent(BaseAgent):
def __init__(self):
super().__init__()
self.pdf_generator = PDFGenerator()
self.document_types = {
"purchase_agreement": PurchaseAgreement,
"listing_agreement": ListingAgreement,
"disclosure_form": DisclosureForm
}

async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
property_data = input_data.get("property_data", {})
doc_type = input_data.get("document_type", "purchase_agreement")

# Determine which documents to generate based on client type
client_type = property_data.get("client_type", "").lower()

documents_to_generate = []

if client_type == "buyer":
documents_to_generate = ["purchase_agreement", "disclosure_form"]
elif client_type == "seller":
documents_to_generate = ["listing_agreement", "disclosure_form"]
else:
documents_to_generate = ["purchase_agreement", "listing_agreement", "disclosure_form"]

# Generate requested documents
generated_docs = []
for doc in documents_to_generate:
if doc_type == "all" or doc_type == doc:
doc_class = self.document_types.get(doc)
if doc_class:
document = doc_class(property_data)
content = document.generate()
pdf_path = await self.pdf_generator.generate_pdf(content, f"{doc}_{property_data.get('property_address')}")
generated_docs.append({
"type": doc,
"path": pdf_path,
"content": content
})

return {
"type": "documents_ready",
"documents": generated_docs,
"message": f"Generated {len(generated_docs)} document(s) successfully!"
}
