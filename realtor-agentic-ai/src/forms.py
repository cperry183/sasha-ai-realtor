from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import date
from enum import Enum

class CommissionType(str, Enum):
    exclusive_right = "exclusive_right"
    exclusive_agency = "exclusive_agency"
    open = "open"

class ListingAgreement(BaseModel):
    """Standard realtor listing agreement [web:15][web:46]."""
    seller_name: str = Field(..., description="Full name of seller(s)")
    seller_address: str
    seller_phone: str
    seller_email: str
    agent_name: str
    brokerage_name: str
    property_address: str = Field(..., description="Full legal address")
    property_description: str  # e.g., beds/baths/sqft
    list_price: float = Field(..., ge=0)
    commission_type: CommissionType
    commission_rate: float = Field(..., ge=0, le=1)  # e.g., 0.06 for 6%
    listing_start_date: date
    listing_duration_months: int = 6
    known_defects: List[str] = []
    liens_encumbrances: List[str] = []

class PurchaseAgreement(BaseModel):
    """Real estate purchase contract [web:14][web:45]."""
    buyer_name: str
    buyer_address: str
    seller_name: str
    property_address: str
    purchase_price: float = Field(..., ge=0)
    earnest_money: float = Field(..., ge=0)
    closing_date: date
    financing_contingency: bool = True
    inspection_contingency: bool = True
    appraisal_contingency: bool = True
    contingencies: List[str] = []
    inclusions: List[str] = []  # Appliances, fixtures
    inclusions_exclusions: str = ""

class SellersDisclosure(BaseModel):
    """Seller's property condition disclosure [web:47][web:49]."""
    property_address: str
    seller_name: str
    roof_age: Optional[int]
    roof_leaks: bool
    foundation_issues: bool
    plumbing_issues: bool
    electrical_issues: bool
    water_damage: bool
    mold: bool
    pests_infestation: bool
    lead_paint: Optional[bool]
    asbestos: Optional[bool]
    flood_zone: bool
    zoning_violations: List[str] = []
    appliances_included: List[str] = []
    additional_disclosures: str = ""

class BuyerDisclosure(BaseModel):
    """Buyer's financial/rep disclosure [web:45]."""
    buyer_name: str
    pre_approval_amount: Optional[float]
    financing_type: Literal["cash", "conventional", "FHA", "VA"]
    employment_status: str
    income_range: str
    rental_history: bool

class AgencyDisclosure(BaseModel):
    """Mandatory agency relationship disclosure [web:52]."""
    agent_name: str
    brokerage: str
    client_name: str
    relationship: Literal["seller_agent", "buyer_agent", "dual", "transaction_broker"]
    date: date
    signature: str = Field(..., description="Digital sig placeholder")

class LeadPaintDisclosure(BaseModel):
    """Federal lead-based paint disclosure."""
    property_built_before_1978: bool
    lead_paint_pamphlet_provided: bool
    known_lead_hazards: List[str] = []
    evaluation_rights_acknowledged: bool

class CounterOffer(BaseModel):
    """Counter offer form."""
    original_offer_price: float
    counter_price: float
    changes: List[str]  # e.g., "Closing date: 30 days"
    expiration_date: date

class Addendum(BaseModel):
    """General addendum for changes."""
    original_agreement_date: date
    property_address: str
    changes_description: str
    effective_date: date

# Registry for agent use
FORMS = {
    "listing_agreement": ListingAgreement.model_json_schema(),
    "purchase_agreement": PurchaseAgreement.model_json_schema(),
    "sellers_disclosure": SellersDisclosure.model_json_schema(),
    "buyer_disclosure": BuyerDisclosure.model_json_schema(),
    "agency_disclosure": AgencyDisclosure.model_json_schema(),
    "lead_paint": LeadPaintDisclosure.model_json_schema(),
    "counter_offer": CounterOffer.model_json_schema(),
    "addendum": Addendum.model_json_schema()
}

# Factory to instantiate filled forms
def create_form(form_type: str, data: dict):
    model = {
        "listing_agreement": ListingAgreement,
        "purchase_agreement": PurchaseAgreement,
        "sellers_disclosure": SellersDisclosure,
        "buyer_disclosure": BuyerDisclosure,
        "agency_disclosure": AgencyDisclosure,
        "lead_paint": LeadPaintDisclosure,
        "counter_offer": CounterOffer,
        "addendum": Addendum
    }.get(form_type)
    if model:
        return model(**data)
    raise ValueError(f"Unknown form: {form_type}")
