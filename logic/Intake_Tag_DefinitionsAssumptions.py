# Cell : Convert Scoring Tags for Questions (filtered logic)

TAG_DEFS = {
"CSRD_CASCADE_SIGNAL": "Buyer has referenced CSRD / EU reporting pressure.",
"BUYER_OPACITY_RISK": "Drivers/requirements unclear; risk of guessing wrong.",
"HRDD_RELEVANCE_HIGH": "Human rights due diligence is likely a buyer focus, even if not explicitly stated.",
"OWNER_GAP": "No clear internal owner for sustainability / social / environmental topics.",
"ENVIRONMENTAL_BASELINE_GAP": "No written environmental documents AND no environmental data tracking.",
"POLICY_LIGHT": "Policies are missing or informal.",
"DUAL_ROLE_PRESSURE": "Supplier is also a buyer, both roles.",
"SUPPLIER_CONFIDENCE_LOW": "Respondent is not confident about responding to buyer's sustainability or human rights criteria for compliance",
"EU_EXPOSURE_NON_EU": "Non-EU supplier exposed to EU buyer/investor requests.",
"DOCUMENTATION_LIGHT": "Sustainability/social data tracking is missing or ad hoc."
}

##Additional tags to impliment later
#"ENV_RISK": "Environmental topics are being requested by buyers."


##RISING_BUYER_DEMAND": "Requests are increasing in detail/frequency."


# Cell — Normalize into internal keys

def normalize_answers(answers_by_question: dict) -> dict:
    a = {}
    for q, ans in answers_by_question.items():
        key = QUESTION_TO_KEY.get(q)
        if key:
            a[key] = ans
    return a

a = normalize_answers(answers_by_question)
print("Normalized answers keys:", list(a.keys()))

#note: code question number 4 later, see below cell

SECTOR_BASELINE_ASSUMPTIONS = {
    "Manufacturing (components / sub-assemblies)": [
        "Environmental data often exists (energy, waste) but is inconsistent and not audit-ready.",
        "Human rights due diligence is typically weak beyond Tier 1 labor.",
        "Climate transition planning is uncommon unless driven by major customers."
    ],

    "Processing / transformation (e.g. food, materials)": [
        "Traceability is partial and upstream risks are not fully understood.",
        "Certifications may exist but are not aligned to CSRD materiality.",
        "High exposure to water, waste, and labor risks."
    ],

    "Agriculture / farming": [
        "Formal sustainability reporting is generally very limited.",
        "Data is seasonal, estimated, or proxy-based.",
        "High biodiversity and labor risks with weak documentation."
    ],

    "Forestry / timber": [
        "Chain-of-custody claims may exist but are unevenly verified.",
        "Biodiversity impacts are under-measured.",
        "Land tenure and Indigenous rights risks are often weakly governed."
    ],

    "Fisheries / aquaculture": [
        "Traceability and data maturity are low.",
        "Labor risks can be significant and poorly documented.",
        "Environmental impacts are rarely evidenced."
    ],

    "Mining / extractives": [
        "Environmental and safety reporting is usually strong internally.",
        "Community and grievance systems are uneven.",
        "Downstream and contractor risks are poorly controlled."
    ],

    "Construction / infrastructure": [
        "Safety data exists, but environmental data is fragmented.",
        "Subcontractor oversight is weak.",
        "Temporary labor complicates due diligence."
    ],

    "Logistics / transport (road, sea, air)": [
        "Fuel and emissions data exists at a high level only.",
        "Data granularity is often insufficient for CSRD.",
        "Labor risk varies widely by subcontracting depth."
    ],

    "Warehousing / distribution": [
        "Basic energy data may exist.",
        "Labor standards vary widely.",
        "Temporary workforce risks are often overlooked."
    ],

    "Energy production or supply": [
        "Strong regulatory and climate reporting exists.",
        "Transition risk is material.",
        "Social and biodiversity risks are under-integrated."
    ],

    "Waste management / recycling": [
        "Environmental metrics are tracked.",
        "Downstream leakage is difficult to verify.",
        "Circularity claims often exceed evidence."
    ],

    "Chemicals / industrial inputs": [
        "Strong compliance culture exists.",
        "Transparency rarely extends beyond minimum requirements.",
        "Downstream impacts are weakly assessed."
    ],

    "Textiles / apparel / footwear": [
        "High audit familiarity but persistent labor risks.",
        "Traceability beyond Tier 1 is weak.",
        "Audit fatigue is common."
    ],

    "Electronics / electrical equipment": [
        "Product compliance is strong.",
        "Supply chain traceability beyond Tier 1 is weak.",
        "Mineral sourcing risks persist."
    ],

    "Packaging / materials": [
        "Material data exists.",
        "Circularity performance is often overstated.",
        "End-of-life outcomes are poorly evidenced."
    ],

    "IT / digital services": [
        "Low awareness of CSRD relevance.",
        "Environmental impact is treated as indirect.",
        "Energy use from data centers is often overlooked."
    ],

    "Professional services": [
        "Sustainability maturity is low.",
        "Workforce metrics are under-measured.",
        "Often excluded from supplier programs."
    ],

    "Facilities management / cleaning / security": [
        "High labor risk and thin margins.",
        "Documentation is weak.",
        "Subcontracting is common."
    ],

    "Other services": [
        "Very limited sustainability readiness.",
        "CSRD relevance is unclear to the supplier.",
        "Data is often absent."
    ]
}

def derive_tags(intake: dict) -> list:
    tags = []

