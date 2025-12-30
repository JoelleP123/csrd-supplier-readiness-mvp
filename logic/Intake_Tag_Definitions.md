# Dictionary of Question Tags (internal)
QUESTION_TO_TAG = {
    
    # Section A

    "Where is your company primarily operating?": "operates_in_eu",
    "Do you sell directly or indirectly to EU-based companies or investors?": "sells_to_eu_buyers",
    "What best describes your company size?": "company_size",
    "Which sector best fits your operations?": "sector",
    "Which best describes your role in the value chain today?": "value_chain_role",
    
    #Section B

    "How complex is your supply chain?": "supply_chain_complexity",
    "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?" :    "sourcing_risk_H_Rights",
    "Are labor conditions a material issue in your operations or sourcing?" : "sourcing_laborissues",
    "Have buyers or partners asked you about environmental or climate-related topics?" : "partner_ask_abt_climate",
    "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?" : "which_topic_environment",

    #Section C

    "Have buyers or partners recently requested ESG, sustainability, or human-rights information?" : "recent_info_request",
    "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "info_request_more_detailed",
    "What do you think prompted these requests?" : "opinion_prompt",
    "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?" : "CSRD_reporting_request",

    # Section D

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

tags


