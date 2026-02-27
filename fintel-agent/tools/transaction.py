FATF_HIGH_RISK = {
    "iran", "north korea", "myanmar", "russia", "belarus",
    "syria", "cuba", "venezuela", "yemen", "libya",
    "somalia", "sudan", "south sudan", "afghanistan", "haiti"
}

FATF_MONITORED = {
    "nigeria", "pakistan", "uae", "philippines", "vietnam",
    "kenya", "cameroon", "senegal", "croatia", "morocco"
}

def flag_transaction(amount: float, country: str, entity: str) -> dict:
    flags = []
    risk_score = 0
    country_lower = country.lower().strip()

    if country_lower in FATF_HIGH_RISK:
        flags.append(f"HIGH RISK jurisdiction: {country}")
        risk_score += 50

    if country_lower in FATF_MONITORED:
        flags.append(f"MONITORED jurisdiction: {country}")
        risk_score += 25

    if amount > 10000:
        flags.append(f"Large transaction: ${amount:,.2f} exceeds $10,000 threshold")
        risk_score += 20

    if amount > 50000:
        flags.append(f"Very large transaction: ${amount:,.2f} exceeds $50,000 threshold")
        risk_score += 15

    shell_keywords = ["holding", "trading", "international", "global", "ventures", "offshore"]
    if any(kw in entity.lower() for kw in shell_keywords):
        flags.append("Entity name contains shell company indicators")
        risk_score += 15

    risk_level = "LOW"
    if risk_score >= 70:
        risk_level = "CRITICAL"
    elif risk_score >= 40:
        risk_level = "HIGH"
    elif risk_score >= 20:
        risk_level = "MEDIUM"

    return {
        "entity": entity,
        "country": country,
        "amount": amount,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "flags": flags
    }