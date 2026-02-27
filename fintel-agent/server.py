from fastmcp import FastMCP
from tools.sanctions import check_sanctions
from tools.entity import resolve_entities
from tools.transaction import flag_transaction

mcp = FastMCP("FintelAgent - AML/KYC Intelligence Server")

@mcp.tool()
def sanctions_check(entity_name: str) -> dict:
    """
    Check if an entity appears on the OFAC SDN sanctions list.
    Uses fuzzy matching against sanctioned entities.
    Returns hit status, confidence score, and matched entry.
    """
    return check_sanctions(entity_name)

@mcp.tool()
def entity_resolution(name1: str, name2: str) -> dict:
    """
    Determine if two company or person names refer to the same entity.
    Uses multiple fuzzy matching algorithms.
    Returns match decision and confidence breakdown.
    """
    return resolve_entities(name1, name2)

@mcp.tool()
def transaction_risk(amount: float, country: str, entity: str) -> dict:
    """
    Assess AML risk of a financial transaction.
    Checks FATF jurisdiction risk, transaction size, and shell company indicators.
    Returns risk level (LOW/MEDIUM/HIGH/CRITICAL) with flags.
    """
    return flag_transaction(amount, country, entity)

@mcp.tool()
def full_kyc_report(entity_name: str, country: str, amount: float) -> dict:
    """
    Run a complete KYC/AML report on an entity.
    Combines sanctions screening, entity resolution, and transaction risk.
    Returns a unified risk report.
    """
    sanctions = check_sanctions(entity_name)
    transaction = flag_transaction(amount, country, entity_name)
    entity_check = resolve_entities(entity_name, "Rosneft Trading")

    overall_risk = "LOW"
    risk_factors = []

    if sanctions["sanctions_hit"]:
        overall_risk = "CRITICAL"
        risk_factors.append(f"SANCTIONS HIT: matched '{sanctions['matched_entry']}' with {sanctions['confidence']}% confidence")

    if transaction["risk_level"] in ["HIGH", "CRITICAL"]:
        if overall_risk != "CRITICAL":
            overall_risk = transaction["risk_level"]
        risk_factors.extend(transaction["flags"])

    if entity_check["score"] >= 80:
        risk_factors.append(f"Entity similar to known high-risk entity ({entity_check['score']}% match)")

    return {
        "entity": entity_name,
        "country": country,
        "amount": amount,
        "overall_risk": overall_risk,
        "risk_factors": risk_factors,
        "sanctions_detail": sanctions,
        "transaction_detail": transaction,
        "entity_resolution_detail": entity_check
    }

if __name__ == "__main__":
    mcp.run()