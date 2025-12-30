# Dictionary of Question Tags (internal)
QUESTION_TO_TAG = {
    
## Section A

    "Where is your company primarily operating?": "operates_in_eu",
    "Do you sell directly or indirectly to EU-based companies or investors?": "sells_to_eu_buyers",
    "What best describes your company size?": "company_size",
    "Which sector best fits your operations?": "sector",
    "Which best describes your role in the value chain today?": "value_chain_role",
    
## Section B

    "How complex is your supply chain?": "supply_chain_complexity",
    "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?" :    "sourcing_risk_H_Rights",
    "Are labor conditions a material issue in your operations or sourcing?" : "sourcing_laborissues",
    "Have buyers or partners asked you about environmental or climate-related topics?" : "partner_ask_abt_climate",
    "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?" : "which_topic_environment",

## Section C

    "Have buyers or partners recently requested ESG, sustainability, or human-rights information?" : "recent_info_request",
    "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "info_request_more_detailed",
    "What do you think prompted these requests?" : "opinion_prompt",
    "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?" : "CSRD_reporting_request",

## Section D

    "Who is primarily responsible for sustainability or social impact topics internally?" : "responsible_for_internal_SI",
    "Do you have written policies related to the environment, sustainability and labor?" : "policy_internal_status",
    "Do you currently track any sustainability or social data?" : "data_tracking",
    "How confident do you feel responding to buyer ESG, sustainability or human rights requests?" : "confidence_level"

}

# Convert Question Tags
tags = {}

for question, answer in intake.items():
    tag = QUESTION_TO_TAG.get(question)
    if tag is not None:
        tags[tag] = answer

# tags

{'operates_in_eu': ('EU', 'Non-EU', 'Both'),
 'sells_to_eu_buyers': ('Yes, directly', 'Yes, indirectly', 'Not sure'),
 'company_size': ('Micro', 'Small', 'Medium', 'Large'),
 'sector': ('Manufacturing (components / sub-assemblies)',
  'Processing / transformation (e.g. food, materials)',
  'Agriculture / farming',
  'Forestry / timber',
  'Fisheries / aquaculture',
  'Mining / extractives',
  'Construction / infrastructure',
  'Logistics / transport (road, sea, air),Warehousing / distribution,Energy production or supply',
  'Waste management / recycling,Chemicals / industrial inputs,Textiles / apparel / footwear,Electronics / electrical equipment,Packaging / materials,IT / digital services,Professional services,Facilities management / cleaning / security,Other services (non-industrial)'),
 'value_chain_role': ('Primarily a supplier to other companies,Both a supplier and a buyer',
  'Primarily a buyer (procures from others)'),
 'supply_chain_complexity': ('Highly multi-tiered',
  'Mostly direct suppliersMix of direct and indirect'),
 'sourcing_risk_H_Rights': ('Yes', 'Some operations', 'No', 'Not sure'),
 'sourcing_laborissues': ('Yes', 'Somewhat', 'No'),
 'partner_ask_abt_climate': ('Yes', 'Somewhat', 'No'),
 'which_topic_environment': ('Climate / emissions',
  'Energy use',
  'Water use',
  'Waste / materials',
  'Biodiversity / land use',
  'Other issue',
  'not applicable',
  'Not specified / unclear'),
 'recent_info_request': ('Yes', 'No', 'Expected soon,'),
 'info_request_more_detailed': ('Yes, significantly more detailed',
  'Yes, somewhat more detailed',
  'No change / Not applicable'),
 'opinion_prompt': ('CSRD regulations',
  'Other new regulation or law (not just CSRD)',
  'Buyer policy update,Investor requirement,Unclear / not explained'),
 'CSRD_reporting_request': 'Yes, explicitly,Yes, indirectly (e.g. “new EU requirements”),No,Not sure',
 'responsible_for_internal_SI': ('Dedicated role/team',
  'Shared responsibility,Legal / compliance only', 'No clear owner'),
 'policy_internal_status': ('Yes', 'Draft / informal', 'No'),
 'data_tracking': ('Yes, structured', 'Informal / ad hoc', 'No'),
 'confidence_level': ('Confident', 'Somewhat confident', 'Not confident')}


# Cell : Logic Tags for Questions (filtered logic / skipped logic)
TAG_DEFS = {
"CSRD_CASCADE_SIGNAL": "Buyer has referenced CSRD / EU reporting pressure.",
"BUYER_OPACITY_RISK": "Drivers/requirements unclear; risk of guessing wrong.",
"HRDD_RELEVANCE_HIGH": "Human rights due diligence is likely a buyer focus, even if not explicitly stated.",
"GOVERNANCE_OWNER_GAP": "No clear internal owner for sustainability / social / environmental topics.", 
"ENVIRONMENTAL_BASELINE_GAP": "No written environmental documents AND no environmental data tracking.",
"POLICY_LIGHT": "Policies are missing or informal.",
"DUAL_ROLE_PRESSURE": "Supplier is also a buyer, both roles.",
"SUPPLIER_CONFIDENCE_LOW": "Respondent is not confident about responding to buyer's sustainability or human rights criteria for compliance"

## Additional tags to be coded later into Intake Questions
## "EU_EXPOSURE_NON_EU": "Non-EU supplier exposed to EU buyer/investor requests.",
## "RISING_BUYER_DEMAND": "Requests are increasing in detail/frequency.",
## "OWNER_GAP": "No clear internal owner for ESG/HR topics.",
## "DATA_GAP": "Sustainability/social data tracking is missing or ad hoc.",
## "ENV_RISK": "Environmental topics are being requested by buyers.",


}




