CUSTOMERS = {
    "C-1001": {
        "id": "C-1001",
        "name": "Sarah Chen",
        "age": 34,
        "occupation": "Senior Software Engineer",
        "employer": "TechCorp Inc.",
        "annual_income": 185000,
        "years_employed": 6,
        "requested_product": "Mortgage",
        "requested_amount": 750000,
        "down_payment_pct": 20,
    },
    "C-1002": {
        "id": "C-1002",
        "name": "Marcus Rivera",
        "age": 42,
        "occupation": "Restaurant Owner",
        "employer": "Rivera's Kitchen LLC",
        "annual_income": 95000,
        "years_employed": 3,
        "requested_product": "Business Expansion Loan",
        "requested_amount": 250000,
        "down_payment_pct": 10,
    },
    "C-1003": {
        "id": "C-1003",
        "name": "Emily Watson",
        "age": 24,
        "occupation": "Marketing Coordinator",
        "employer": "Digital Media Corp",
        "annual_income": 62000,
        "years_employed": 1,
        "requested_product": "Auto Loan",
        "requested_amount": 35000,
        "down_payment_pct": 15,
    },
}

# --- MCP Tool: credit_bureau_service ---

CREDIT_SCORES = {
    "C-1001": {
        "credit_score": 742,
        "score_range": "Good",
        "provider": "TransUnion",
        "report_date": "2026-05-18",
    },
    "C-1002": {
        "credit_score": 668,
        "score_range": "Fair",
        "provider": "Equifax",
        "report_date": "2026-05-17",
    },
    "C-1003": {
        "credit_score": 695,
        "score_range": "Fair-Good",
        "provider": "Experian",
        "report_date": "2026-05-19",
    },
}

CREDIT_HISTORY = {
    "C-1001": {
        "history_years": 12,
        "open_accounts": 5,
        "closed_accounts": 3,
        "total_credit_limit": 45000,
        "current_utilization_pct": 18,
        "payment_history": "98% on-time (2 late payments in 12 years)",
        "derogatory_marks": 0,
        "hard_inquiries_12mo": 1,
        "collections": 0,
        "bankruptcies": 0,
        "oldest_account": "2014-03-15",
    },
    "C-1002": {
        "history_years": 18,
        "open_accounts": 8,
        "closed_accounts": 5,
        "total_credit_limit": 62000,
        "current_utilization_pct": 45,
        "payment_history": "91% on-time (6 late in 18 years, 2 in last 24mo)",
        "derogatory_marks": 1,
        "hard_inquiries_12mo": 3,
        "collections": 0,
        "bankruptcies": 0,
        "oldest_account": "2008-07-22",
    },
    "C-1003": {
        "history_years": 3,
        "open_accounts": 2,
        "closed_accounts": 0,
        "total_credit_limit": 8000,
        "current_utilization_pct": 32,
        "payment_history": "100% on-time",
        "derogatory_marks": 0,
        "hard_inquiries_12mo": 2,
        "collections": 0,
        "bankruptcies": 0,
        "oldest_account": "2023-09-01",
    },
}

DEBT_SUMMARY = {
    "C-1001": {
        "total_debt": 28000,
        "monthly_obligations": 850,
        "debt_to_income_ratio": 5.5,
        "breakdown": [
            {"type": "Student Loan", "balance": 18000, "monthly": 350, "rate": 4.5},
            {"type": "Credit Card", "balance": 8100, "monthly": 300, "rate": 19.9},
            {"type": "Auto Loan", "balance": 1900, "monthly": 200, "rate": 3.9},
        ],
    },
    "C-1002": {
        "total_debt": 178000,
        "monthly_obligations": 4200,
        "debt_to_income_ratio": 53.1,
        "breakdown": [
            {"type": "Business Line of Credit", "balance": 85000, "monthly": 1800, "rate": 8.5},
            {"type": "Commercial Mortgage", "balance": 62000, "monthly": 1400, "rate": 6.2},
            {"type": "Credit Cards", "balance": 28000, "monthly": 800, "rate": 22.9},
            {"type": "Equipment Lease", "balance": 3000, "monthly": 200, "rate": 7.0},
        ],
    },
    "C-1003": {
        "total_debt": 22000,
        "monthly_obligations": 680,
        "debt_to_income_ratio": 13.2,
        "breakdown": [
            {"type": "Student Loan", "balance": 19500, "monthly": 450, "rate": 5.8},
            {"type": "Credit Card", "balance": 2500, "monthly": 230, "rate": 21.9},
        ],
    },
}

# --- MCP Tool: employment_verification_service ---

EMPLOYMENT_RECORDS = {
    "C-1001": {
        "employer": "TechCorp Inc.",
        "title": "Senior Software Engineer",
        "employment_type": "Full-time",
        "start_date": "2020-03-15",
        "years_at_employer": 6.2,
        "verified": True,
        "employer_industry": "Technology",
        "employer_size": "5000+ employees",
    },
    "C-1002": {
        "employer": "Rivera's Kitchen LLC",
        "title": "Owner / Operator",
        "employment_type": "Self-employed",
        "start_date": "2023-06-01",
        "years_at_employer": 3.0,
        "verified": True,
        "employer_industry": "Food & Beverage",
        "employer_size": "12 employees",
    },
    "C-1003": {
        "employer": "Digital Media Corp",
        "title": "Marketing Coordinator",
        "employment_type": "Full-time",
        "start_date": "2025-04-10",
        "years_at_employer": 1.1,
        "verified": True,
        "employer_industry": "Digital Marketing",
        "employer_size": "200 employees",
    },
}

INCOME_HISTORY = {
    "C-1001": {
        "current_annual": 185000,
        "previous_years": [
            {"year": 2025, "income": 175000},
            {"year": 2024, "income": 162000},
            {"year": 2023, "income": 148000},
        ],
        "income_trend": "Consistent upward growth (~8% annually)",
        "additional_income": [
            {"source": "Stock RSU Vesting", "annual_amount": 32000},
        ],
        "total_verified_income": 217000,
        "income_stability": "High",
    },
    "C-1002": {
        "current_annual": 95000,
        "previous_years": [
            {"year": 2025, "income": 88000},
            {"year": 2024, "income": 72000},
            {"year": 2023, "income": 45000},
        ],
        "income_trend": "Growing but volatile (restaurant industry)",
        "additional_income": [
            {"source": "Catering Side Business", "annual_amount": 18000},
        ],
        "total_verified_income": 113000,
        "income_stability": "Moderate",
    },
    "C-1003": {
        "current_annual": 62000,
        "previous_years": [
            {"year": 2025, "income": 58000},
            {"year": 2024, "income": 42000},
        ],
        "income_trend": "Early career growth",
        "additional_income": [],
        "total_verified_income": 62000,
        "income_stability": "Moderate - limited history",
    },
}

TAX_RETURNS = {
    "C-1001": {
        "filing_status": "Single",
        "years_filed": [2025, 2024, 2023],
        "agi_2025": 192000,
        "consistent_with_stated_income": True,
        "flags": [],
    },
    "C-1002": {
        "filing_status": "Married Filing Jointly",
        "years_filed": [2025, 2024, 2023],
        "agi_2025": 108000,
        "consistent_with_stated_income": True,
        "flags": ["Schedule C losses in 2023-2024 during restaurant startup"],
    },
    "C-1003": {
        "filing_status": "Single",
        "years_filed": [2025, 2024],
        "agi_2025": 61500,
        "consistent_with_stated_income": True,
        "flags": ["Only 2 years of tax history available"],
    },
}

# --- MCP Tool: market_data_service ---

MARKET_CONDITIONS = {
    "Mortgage": {
        "sector": "Residential Real Estate",
        "current_30yr_rate": 6.45,
        "rate_trend": "Declining (down from 7.1% peak)",
        "housing_inventory": "Low - seller's market in most metros",
        "median_home_price_trend": "+3.2% YoY",
        "delinquency_rate": "2.1% (below historical average)",
        "outlook": "Stable with moderate growth expected",
        "risk_level": "Low-Moderate",
    },
    "Business Expansion Loan": {
        "sector": "Small Business / Food & Beverage",
        "sba_rate": 8.75,
        "rate_trend": "Stable",
        "restaurant_failure_rate_5yr": "60%",
        "consumer_spending_trend": "+1.8% YoY",
        "small_biz_confidence_index": 98.2,
        "outlook": "Cautious - elevated failure rates in F&B sector",
        "risk_level": "Moderate-High",
    },
    "Auto Loan": {
        "sector": "Auto Lending",
        "current_new_rate": 5.9,
        "current_used_rate": 7.2,
        "rate_trend": "Declining slightly",
        "auto_delinquency_rate": "2.8%",
        "vehicle_depreciation_avg": "15-20% year 1",
        "outlook": "Stable - improving affordability",
        "risk_level": "Low-Moderate",
    },
}

SECTOR_EXPOSURE = {
    "C-1001": {
        "primary_sector": "Technology",
        "sector_health": "Strong",
        "concentration_risk": "Moderate (income + RSUs tied to tech sector)",
        "geographic_market": "San Francisco Bay Area",
        "property_market_risk": "Moderate-High (high prices, tech layoff exposure)",
    },
    "C-1002": {
        "primary_sector": "Food & Beverage",
        "sector_health": "Mixed",
        "concentration_risk": "High (single-business income dependency)",
        "geographic_market": "Austin, TX",
        "property_market_risk": "Low (commercial lease, not purchase)",
    },
    "C-1003": {
        "primary_sector": "Digital Marketing",
        "sector_health": "Good",
        "concentration_risk": "Low (standard employment, no asset concentration)",
        "geographic_market": "Denver, CO",
        "property_market_risk": "N/A (auto loan)",
    },
}

# --- MCP Tool: compliance_screening_service ---

SANCTIONS_CHECK = {
    "C-1001": {
        "ofac_match": False,
        "eu_sanctions_match": False,
        "un_sanctions_match": False,
        "adverse_media_hits": 0,
        "screening_date": "2026-05-20",
        "status": "CLEAR",
    },
    "C-1002": {
        "ofac_match": False,
        "eu_sanctions_match": False,
        "un_sanctions_match": False,
        "adverse_media_hits": 1,
        "adverse_media_detail": "Local news mention: health code violation (resolved 2024)",
        "screening_date": "2026-05-20",
        "status": "CLEAR - minor flag noted",
    },
    "C-1003": {
        "ofac_match": False,
        "eu_sanctions_match": False,
        "un_sanctions_match": False,
        "adverse_media_hits": 0,
        "screening_date": "2026-05-20",
        "status": "CLEAR",
    },
}

PEP_CHECK = {
    "C-1001": {"is_pep": False, "pep_level": None, "related_to_pep": False},
    "C-1002": {"is_pep": False, "pep_level": None, "related_to_pep": False},
    "C-1003": {"is_pep": False, "pep_level": None, "related_to_pep": False},
}

KYC_DOCUMENTS = {
    "C-1001": {
        "identity_verified": True,
        "id_type": "US Passport",
        "id_expiry": "2029-08-15",
        "address_verified": True,
        "address_method": "Utility bill (PG&E, dated 2026-04-28)",
        "source_of_funds": "Employment income + RSU vesting",
        "risk_category": "Standard",
        "enhanced_due_diligence_required": False,
    },
    "C-1002": {
        "identity_verified": True,
        "id_type": "US Driver's License",
        "id_expiry": "2027-11-03",
        "address_verified": True,
        "address_method": "Bank statement (Chase, dated 2026-05-01)",
        "source_of_funds": "Business income + catering revenue",
        "risk_category": "Medium",
        "enhanced_due_diligence_required": False,
    },
    "C-1003": {
        "identity_verified": True,
        "id_type": "US Driver's License",
        "id_expiry": "2030-02-19",
        "address_verified": True,
        "address_method": "Lease agreement (dated 2025-03-01)",
        "source_of_funds": "Employment income",
        "risk_category": "Standard",
        "enhanced_due_diligence_required": False,
    },
}

# --- Pre-built agent analysis responses (mock mode) ---

MOCK_ANALYSES = {
    "C-1001": {
        "credit_analyst": {
            "score": 82,
            "rating": "B+",
            "summary": "Strong credit profile. Score of 742 with 12-year history and low utilization (18%). Minimal debt relative to income. DTI of 5.5% is excellent. Only 2 late payments in 12 years. Single hard inquiry suggests disciplined borrowing. Well-positioned for mortgage approval.",
            "key_findings": [
                "Credit score 742 (Good range)",
                "Low credit utilization at 18%",
                "DTI ratio of 5.5% — well below 43% threshold",
                "Clean payment history (98% on-time)",
            ],
        },
        "income_verifier": {
            "score": 90,
            "rating": "A",
            "summary": "Highly stable income profile. $185K base salary at TechCorp (6+ years tenure) with additional $32K in RSU vesting. Consistent upward trajectory of ~8% annual growth. Total verified income of $217K provides strong debt service capacity for $750K mortgage. Income stability rated HIGH.",
            "key_findings": [
                "Verified income: $217K (base + RSUs)",
                "6+ years at current employer",
                "Consistent 8% annual income growth",
                "Tax returns corroborate stated income",
            ],
        },
        "market_analyst": {
            "score": 68,
            "rating": "B-",
            "summary": "Mixed market signals. Current 30yr mortgage rates at 6.45% are declining from peak, improving affordability. However, Bay Area market carries elevated price risk and tech sector concentration. Low housing inventory supports property values but limits negotiating power. Moderate concern around tech-sector layoff exposure affecting both income and regional property values.",
            "key_findings": [
                "30yr rate at 6.45% — declining trend favorable",
                "Bay Area: high prices, tech-sector dependency",
                "Housing delinquency rate below average (2.1%)",
                "Concentration risk: income + property in same sector",
            ],
        },
        "compliance_officer": {
            "score": 95,
            "rating": "A+",
            "summary": "Clean compliance profile. No sanctions matches across OFAC, EU, or UN lists. No PEP connections. Zero adverse media findings. Identity fully verified via US Passport. Source of funds clearly documented through employment and RSU vesting. Standard risk category — no enhanced due diligence required.",
            "key_findings": [
                "All sanctions screenings: CLEAR",
                "No PEP status or connections",
                "Identity and address verified",
                "Standard risk — no EDD required",
            ],
        },
    },
    "C-1002": {
        "credit_analyst": {
            "score": 55,
            "rating": "C+",
            "summary": "Concerning credit indicators for a $250K business loan. Score of 668 (Fair) with high utilization at 45%. DTI of 53.1% significantly exceeds standard thresholds. Recent late payments (2 in last 24 months) and one derogatory mark signal stress. Multiple recent hard inquiries suggest active credit-seeking behavior. Existing business debt of $85K on line of credit adds risk.",
            "key_findings": [
                "Credit score 668 (Fair range)",
                "High utilization at 45%",
                "DTI ratio of 53.1% — exceeds 43% threshold",
                "Recent payment issues (2 late in 24mo)",
            ],
        },
        "income_verifier": {
            "score": 58,
            "rating": "C+",
            "summary": "Income shows growth but carries significant volatility risk. Self-employed restaurant owner with $95K stated income, growing from $45K in 2023. Growth is promising but the 3-year track record is short for a $250K loan. Catering side income adds $18K but is also variable. Schedule C losses during startup period (2023-2024) are a concern. Income stability rated MODERATE.",
            "key_findings": [
                "Self-employed — income verification complex",
                "Rapid growth ($45K→$95K) but only 3-year history",
                "Schedule C losses during 2023-2024 startup",
                "Total verified: $113K (includes variable catering)",
            ],
        },
        "market_analyst": {
            "score": 42,
            "rating": "D+",
            "summary": "Elevated market risk for restaurant sector expansion. Industry data shows 60% five-year failure rate for restaurants. SBA rates at 8.75% increase debt service burden. Consumer spending growth at +1.8% is modest. Small business confidence index at 98.2 is below the 100 optimism threshold. Austin market is competitive with high restaurant density. The combination of sector risk and existing debt levels creates meaningful exposure.",
            "key_findings": [
                "Restaurant 5-year failure rate: 60%",
                "SBA rate at 8.75% — heavy debt service",
                "Consumer spending growth modest at 1.8%",
                "High sector concentration risk",
            ],
        },
        "compliance_officer": {
            "score": 82,
            "rating": "B+",
            "summary": "Mostly clean compliance profile with a minor flag. No sanctions matches. No PEP connections. One adverse media hit — a local health code violation at the restaurant, which was resolved in 2024. Identity verified. Source of funds documented through business income. Medium risk category assigned due to self-employment and variable income, but no enhanced due diligence required.",
            "key_findings": [
                "Sanctions screenings: CLEAR",
                "Minor adverse media: health code violation (resolved)",
                "Medium risk category (self-employment)",
                "No EDD required",
            ],
        },
    },
    "C-1003": {
        "credit_analyst": {
            "score": 65,
            "rating": "B-",
            "summary": "Thin but clean credit file. Score of 695 with only 3 years of history. Perfect payment record (100% on-time) is positive. Credit utilization at 32% is acceptable but not ideal. Only 2 open accounts limits the credit mix score. Student loan is the primary obligation. For a $35K auto loan, the profile is adequate but the short history is a limiting factor.",
            "key_findings": [
                "Credit score 695 (Fair-Good range)",
                "100% on-time payment history",
                "Thin file: only 3 years, 2 accounts",
                "Utilization at 32% — room for improvement",
            ],
        },
        "income_verifier": {
            "score": 60,
            "rating": "C+",
            "summary": "Early-career income profile with limited history. $62K annual salary as Marketing Coordinator with only 1.1 years at current employer. No additional income sources. Income trajectory shows growth ($42K→$62K) but the track record is too short to establish stability. Only 2 years of tax returns available. For a $35K auto loan, the income is sufficient but the lack of stability data introduces uncertainty.",
            "key_findings": [
                "Verified income: $62K (no additional sources)",
                "Only 1.1 years at current employer",
                "Limited 2-year income history",
                "Income sufficient for loan size",
            ],
        },
        "market_analyst": {
            "score": 75,
            "rating": "B+",
            "summary": "Favorable market conditions for auto lending. Current new auto rate at 5.9% is declining. Auto delinquency rates at 2.8% are manageable. Standard vehicle depreciation of 15-20% in year one is the primary asset risk but expected for auto loans. Denver market has strong employment base in the digital marketing sector. Overall low-to-moderate market risk for this loan type.",
            "key_findings": [
                "Auto loan rate at 5.9% — declining trend",
                "Delinquency rate 2.8% — normal range",
                "Denver job market strong for marketing sector",
                "Standard depreciation risk for auto assets",
            ],
        },
        "compliance_officer": {
            "score": 95,
            "rating": "A+",
            "summary": "Clean compliance profile. No matches on any sanctions lists. No PEP status or connections. Zero adverse media. Identity verified via driver's license. Address confirmed through lease agreement. Source of funds is straightforward employment income. Standard risk category. No issues identified.",
            "key_findings": [
                "All sanctions screenings: CLEAR",
                "No PEP status or connections",
                "Identity and address verified",
                "Standard risk — no EDD required",
            ],
        },
    },
}

MOCK_FINAL_ASSESSMENTS = {
    "C-1001": {
        "overall_score": 82,
        "overall_rating": "B+",
        "recommendation": "APPROVE",
        "assessment": (
            "**Recommendation: APPROVE** — Sarah Chen presents a strong risk profile for a $750,000 mortgage.\n\n"
            "**Overall Risk Score: 82/100 (Low-Moderate Risk)**\n\n"
            "The applicant demonstrates excellent debt service capacity with a verified income of $217K and a remarkably low DTI of 5.5%. "
            "Her credit history of 12 years with a 742 score and minimal delinquencies provides strong confidence in repayment behavior. "
            "The primary risk factor is geographic concentration in the Bay Area tech market, which creates correlated exposure between her income (tech employment + RSUs) and property values. "
            "This is partially mitigated by the 20% down payment.\n\n"
            "**Conditions:** Standard mortgage terms. Recommend fixed-rate product to mitigate rate risk. "
            "No compliance concerns — clean screening across all checks."
        ),
    },
    "C-1002": {
        "overall_score": 56,
        "overall_rating": "C+",
        "recommendation": "CONDITIONAL APPROVE",
        "assessment": (
            "**Recommendation: CONDITIONAL APPROVE** — Marcus Rivera's application for a $250,000 business expansion loan presents elevated risk.\n\n"
            "**Overall Risk Score: 56/100 (Moderate-High Risk)**\n\n"
            "The applicant's restaurant business shows promising growth (revenue nearly doubled in 3 years), but several risk factors require attention. "
            "The DTI ratio of 53.1% exceeds standard thresholds, credit utilization is high at 45%, and the restaurant industry carries a 60% five-year failure rate. "
            "Income volatility from self-employment and recent credit stress (2 late payments in 24 months) add concern.\n\n"
            "**Conditions:** Require additional collateral or personal guarantee. Recommend reduced loan amount ($175K-$200K). "
            "Require quarterly financial statements for first 2 years. Minor compliance note: resolved health code violation does not impact approval."
        ),
    },
    "C-1003": {
        "overall_score": 72,
        "overall_rating": "B",
        "recommendation": "APPROVE",
        "assessment": (
            "**Recommendation: APPROVE** — Emily Watson qualifies for a $35,000 auto loan with standard terms.\n\n"
            "**Overall Risk Score: 72/100 (Moderate Risk)**\n\n"
            "The applicant has a clean but thin credit profile. Perfect payment history and a 695 credit score demonstrate responsible behavior, "
            "though the 3-year credit history and limited account mix are constraints. Income of $62K is sufficient for the loan amount, "
            "but the short employment tenure (1.1 years) and limited income history introduce some uncertainty. "
            "Market conditions for auto lending are favorable with declining rates.\n\n"
            "**Conditions:** Standard auto loan terms at market rate. 15% down payment mitigates depreciation risk. "
            "Clean compliance profile. Consider 48-month term to keep monthly payments manageable relative to existing obligations ($680/mo student loan + credit card)."
        ),
    },
}
