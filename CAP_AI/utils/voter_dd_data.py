"""Voter DD requirement knowledge base."""

VOTER_DD_DATA: dict[str, dict[str, dict]] = {
    "Tamil Nadu": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Due Diligence (DD) for voter registration verifies identity, age, and residential address before issuing EPIC.",
                "required_documents": ["Proof of Age (Birth Certificate/SSLC)", "Proof of Address (Aadhaar/Ration Card)", "Passport-size Photo", "Form 6"],
                "why_needed": "Prevents duplicate registrations, underage voting, and non-resident enrolment.",
                "accepted_proofs": ["Aadhaar Card", "Passport", "Driving Licence", "Bank Passbook with address", "Utility Bill (<3 months)"],
                "common_mistakes": ["Address mismatch across documents", "Photo not recent", "Missing Form 6 declaration"],
                "exceptions": ["Homeless persons may use Booth Level Officer verification", "Transgender persons — self-declaration accepted"],
            },
            "Address Change": {
                "what_is_dd": "DD confirms the applicant genuinely resides at the new address within the constituency.",
                "required_documents": ["Form 8", "Proof of new address", "Existing EPIC copy"],
                "why_needed": "Ensures electoral roll accuracy and prevents constituency-hopping fraud.",
                "accepted_proofs": ["Rent Agreement", "Property Tax Receipt", "Employer Certificate"],
                "common_mistakes": ["Old address still on Aadhaar", "Form 8 not signed"],
                "exceptions": ["Armed forces personnel — service certificate accepted"],
            },
        },
        "Correction": {
            "Name Correction": {
                "what_is_dd": "DD validates that the name correction request is genuine and supported by official records.",
                "required_documents": ["Form 8", "Gazette Notification or Court Order", "Existing EPIC"],
                "why_needed": "Prevents identity fraud and ensures ballot integrity.",
                "accepted_proofs": ["Gazette copy", "School certificate", "Passport"],
                "common_mistakes": ["No gazette for significant name change", "Spelling mismatch"],
                "exceptions": ["Minor spelling corrections may not need gazette"],
            },
        },
    },
    "Karnataka": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Karnataka ECI-mandated DD ensures only eligible citizens are enrolled in the electoral roll.",
                "required_documents": ["Form 6", "Age proof", "Address proof", "Photograph"],
                "why_needed": "Maintains clean electoral rolls for free and fair elections.",
                "accepted_proofs": ["Aadhaar", "PAN", "SSLC marksheet", "Electricity bill"],
                "common_mistakes": ["Applying in wrong constituency", "Incomplete Form 6 Part IV"],
                "exceptions": ["Students in hostels — warden certificate accepted"],
            },
        },
    },
    "Kerala": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Kerala's DD process cross-verifies identity through multiple government databases.",
                "required_documents": ["Form 6", "Age proof", "Residence proof", "Photo"],
                "why_needed": "Kerala has high migration; DD prevents ghost voters.",
                "accepted_proofs": ["Ration Card", "Aadhaar", "Passport", "Land Tax receipt"],
                "common_mistakes": ["Ration card address outdated", "Missing BLO verification"],
                "exceptions": ["NRK (Non-Resident Keralite) special provisions apply"],
            },
        },
    },
    "Andhra Pradesh": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "AP DD validates voter eligibility per Representation of People Act, 1950.",
                "required_documents": ["Form 6", "Age proof", "Address proof"],
                "why_needed": "Critical for accurate voter rolls in rapidly urbanising districts.",
                "accepted_proofs": ["Aadhaar", "Ration Card", "Property documents"],
                "common_mistakes": ["Duplicate Aadhaar linkage", "Wrong mandal selection"],
                "exceptions": ["Tribal areas — community certificate may substitute address proof"],
            },
        },
    },
    "Telangana": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Telangana DD ensures one person-one vote principle through biometric cross-check.",
                "required_documents": ["Form 6", "Age proof", "Address proof", "Photo"],
                "why_needed": "Hyderabad dual-state legacy requires rigorous verification.",
                "accepted_proofs": ["Aadhaar", "Passport", "Driving Licence", "Telephone bill"],
                "common_mistakes": ["Old AP EPIC not surrendered", "Address in GHMC limits unclear"],
                "exceptions": ["IT sector migrants — employer letter accepted temporarily"],
            },
        },
    },
    "Maharashtra": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Maharashtra DD follows ECI guidelines with additional urban verification for Mumbai/Pune.",
                "required_documents": ["Form 6", "Age proof", "Address proof", "Photo"],
                "why_needed": "Large urban population requires strict address verification.",
                "accepted_proofs": ["Aadhaar", "Leave & Licence Agreement", "Society NOC"],
                "common_mistakes": ["Society NOC missing", "Rent agreement not registered"],
                "exceptions": ["Slum rehabilitation — BLO field visit mandatory"],
            },
        },
    },
    "Delhi": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Delhi DD includes Aadhaar seeding and address verification for NCR migrants.",
                "required_documents": ["Form 6", "Age proof", "Address proof", "Photo"],
                "why_needed": "High inter-state migration demands robust DD.",
                "accepted_proofs": ["Aadhaar", "Passport", "Bank statement", "Gas connection bill"],
                "common_mistakes": ["Aadhaar address not updated after shift", "Wrong assembly segment"],
                "exceptions": ["Homeless — Night Shelter certificate accepted"],
            },
        },
    },
    "Gujarat": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Gujarat DD verifies eligibility with emphasis on rural-urban migration patterns.",
                "required_documents": ["Form 6", "Age proof", "Address proof"],
                "why_needed": "Industrial migration requires accurate roll maintenance.",
                "accepted_proofs": ["Aadhaar", "Ration Card", "Property tax receipt"],
                "common_mistakes": ["Factory address used instead of residence", "Missing photo attestation"],
                "exceptions": ["SEZ workers — company accommodation letter accepted"],
            },
        },
    },
    "West Bengal": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "West Bengal DD follows ECI SOP with BLO house-to-house verification.",
                "required_documents": ["Form 6", "Age proof", "Address proof", "Photo"],
                "why_needed": "Border district sensitivity requires enhanced DD.",
                "accepted_proofs": ["Aadhaar", "Ration Card", "EPIC of family member"],
                "common_mistakes": ["Border area documents not cross-verified", "Name transliteration errors"],
                "exceptions": ["Tea garden workers — manager certificate accepted"],
            },
        },
    },
    "Rajasthan": {
        "New Registration": {
            "Voter ID": {
                "what_is_dd": "Rajasthan DD includes desert-area special provisions for nomadic communities.",
                "required_documents": ["Form 6", "Age proof", "Address proof"],
                "why_needed": "Sparse population areas need flexible yet rigorous DD.",
                "accepted_proofs": ["Aadhaar", "Jan Aadhaar", "Bhamashah Card", "Land records"],
                "common_mistakes": ["Jan Aadhaar not linked", "Nomadic address not documented"],
                "exceptions": ["Pastoral communities — Patwari certificate accepted"],
            },
        },
    },
}


def search_voter_dd(query: str) -> list[tuple[str, str, str, dict]]:
    """Search knowledge base by state, purpose, or keyword."""
    results = []
    q = query.lower()
    for state, purposes in VOTER_DD_DATA.items():
        for purpose, docs in purposes.items():
            for doc_type, info in docs.items():
                blob = f"{state} {purpose} {doc_type} {' '.join(str(v) for v in info.values())}".lower()
                if not q or q in blob:
                    results.append((state, purpose, doc_type, info))
    return results


def get_states() -> list[str]:
    return sorted(VOTER_DD_DATA.keys())


def get_purposes(state: str) -> list[str]:
    return list(VOTER_DD_DATA.get(state, {}).keys())


def get_document_types(state: str, purpose: str) -> list[str]:
    return list(VOTER_DD_DATA.get(state, {}).get(purpose, {}).keys())
