

# --- Convert list -> dict for scoring 
# --- Scoring + reasons ---


def run_screening(tags: dict) -> dict:
    tags = tags or {}

    score = 0
    reasons = []

    if tags.get("CSRD_CASCADE_SIGNAL"):
        score += 2
        reasons.append("CSRD readiness activities strongly recommended.")

    if tags.get("EU_EXPOSURE_NON_EU"):
        score += 2
        reasons.append("EU business links suggest additional CSRD vulnerability.")

    if tags.get("BUYER_OPACITY_RISK"):
        score += 2
        reasons.append("Buyers are expressing conflicting or confusing requests.")

    if tags.get("HRDD_RELEVANCE_HIGH"):
        score += 1
        reasons.append("Human rights and labor strengthening recommended.")

    if tags.get("OWNER_GAP"):
        score += 1
        reasons.append("Responsibility gaps detected.")

    if tags.get("ENVIRONMENTAL_BASELINE_GAP"):
        score += 1
        reasons.append("Environmental baseline processes missing.")

    if tags.get("POLICY_LIGHT"):
        score += 1
        reasons.append("Policy documentation is light or missing.")

    if tags.get("DUAL_ROLE_PRESSURE"):
        score += 1
        reasons.append("Multiple pressure signals detected.")

    if tags.get("SUPPLIER_CONFIDENCE_LOW"):
        score += 1
        reasons.append("Low confidence suggests external support may help.")

    # --- Band logic (unchanged) ---
    if score >= 12:
        band = "HIGH: Sustainability readiness triage recommended"
    elif score >= 5:
        band = "MEDIUM: Some Sustainability-driven pressure likely"
    else:
        band = "LOW: Limited signal of Sustainability-driven pressure"

    return {
        "score": score,
        "band": band,
        "why": reasons,
        "tags_received": [k for k, v in tags.items() if v],
    }


# --- Output --- taken out as test
# print("\nScore:", score)
# print("Band:", band)
# print("Suggested Next Steps:")



# --- Print sector baseline assumptions ---
sector = a.get("sector")
if sector and sector in SECTOR_BASELINE_ASSUMPTIONS:
    print(f"\nBaseline assumptions for '{sector}':")
    for assumption in SECTOR_BASELINE_ASSUMPTIONS[sector]:
        print(f"  - {assumption}")
else:
    print(f"\nNo specific baseline assumptions found for sector: {sector}")

# --- End print sector baseline assumptions ---

print("Recommended Next Steps:")
if reasons:
    for r in reasons:
        print("- ", r)
else:
    print("- (no reasons triggered; check whether applied_tags is empty)")

# --- Print applied tags after the main assessment ---
print("\nAll applied tags:")
for t in applied_tags:
    print(f"- {t}")
print("Full applied tags list for reference:", applied_tags)


if reasons:
    for r in reasons:
        print("- ", r)
else:
    print("- (no reasons triggered; check whether applied_tags is empty)")


# Additional tags to be given scores later (note)

# "RISING_BUYER_DEMAND": "Requests are increasing in detail/frequency."
# "ENV_RISK": "Environmental topics are being requested by buyers."

# Cell: Run screenings


def run_screening(tags: dict) -> dict:
    """
    tags: dict like {"CSRD_CASCADE_SIGNAL": True, "DATA_GAP": False, ...}
    returns: dict with keys: readiness_level, tags, interpretation, next_steps
    """

    # Keep only tags that are True
    active_tags = [k for k, v in tags.items() if v is True]

    # ---- Simple scoring model (edit weights TBD) ----
    weights = {
        "CSRD_CASCADE_SIGNAL": 1,
        "EU_EXPOSURE_NON_EU": 1,

        "POLICY_LIGHT": 2,

        "HRDD_RELEVANCE_HIGH": 2,
        "BUYER_OPACITY_RISK": 1,
        "ENVIRONMENTAL_BASELINE_GAP": 1,
        "DOCUMENTATION_LIGHT": 1,
        "SUPPLIER_CONFIDENCE_LOW": 1,
        "DUAL_ROLE_PRESSURE": 1,
        "OWNER_GAP": 2,
        ## to add later: Rising_buyer_demand and ENV_RISK
    }

    score = sum(weights.get(t, 0) for t in active_tags)

    # ---- Readiness level thresholds ----
    # Lower score = more ready; higher score = more gaps/pressure
    if score <= 2:
        readiness_level = "GREEN — Low risk / early readiness"
        interpretation = (
            "You have limited immediate pressure signals and/or only minor capability gaps. "
            "Focus on documentation hygiene and staying ahead of buyer requests."
        )
    elif score <= 6:
        readiness_level = "AMBER — Moderate risk / needs structuring"
        interpretation = (
            "You’re seeing buyer/regulatory pressure signals and some internal gaps. "
            "Prioritize ownership, policy basics, and minimum viable data tracking."
        )
    else:
        readiness_level = "RED — High risk / likely exposure"
        interpretation = (
            "You have multiple pressure signals and several internal capability gaps. "
            "This is where suppliers often get caught flat-footed during buyer requests, audits, or tender processes. "
            "Move quickly to establish ownership, baseline policies, and auditable evidence."

        )



    # Next steps generator (based on which gaps are active)
    next_steps = []

    if "OWNER_GAP" in active_tags:
        next_steps.append("Assign a single accountable owner for sustainability/compliance requests (name + role).")

    if "POLICY_LIGHT" in active_tags:
        next_steps.append("Review for gaps and draft a minimum policy set (environment + labor/human rights) with approval + version control.")

    if "DOCUMENTATION_LIGHT" in active_tags:
        next_steps.append("Start a basic data baseline and inventory check (may include: energy, emissions scope assumptions, water, waste) in a simple tracker.")

    if "HRDD_RELEVANCE_HIGH" in active_tags:
        next_steps.append("Map human rights and/or labor risk in sourcing (countries/commodities) and set up a lightweight supplier or partner due diligence checklist.")

    if "CSRD_CASCADE_SIGNAL" in active_tags or "RISING_BUYER_DEMAND" in active_tags:
        next_steps.append("Create a buyer-response pack: 1-page overview + evidence folder + standard Q&A.")

    if "EU_EXPOSURE_NON_EU" in active_tags:
        next_steps.append("Identify EU-linked customers and expected reporting asks; align your evidence to what they request most.")

    # Always include an “artifact” step so this becomes reusable IP
    next_steps.append("Package outputs into a reusable 'Readiness Folder' (policies, tracker, evidence, Q&A) for future requests.")

#note : to review / ammend "next steps" list

    return {
        "readiness_level": readiness_level,
        "tags": active_tags,
        "interpretation": interpretation,
        "next_steps": next_steps,
    }

    ## add airtable form that requests feedback for the beta ****
