from thefuzz import fuzz

# Real sanctioned entities from OFAC SDN list (sample for demo)
SANCTIONED_ENTITIES = [
    "Rosneft Trading S.A.",
    "Gazprombank",
    "Vladimir Putin",
    "Ali Khamenei",
    "Kim Jong Un",
    "Sberbank",
    "VTB Bank",
    "Iranian Revolutionary Guard Corps",
    "Hezbollah",
    "Hamas",
    "Al-Qaeda",
    "ISIS",
    "Islamic State",
    "Mahan Air",
    "Iran Air",
    "Syrian Arab Airlines",
    "Nordstream AG",
    "Lukashenko Alexander",
    "Wagner Group",
    "Yevgeny Prigozhin",
    "Viktor Vekselberg",
    "Roman Abramovich",
    "Igor Sechin",
    "Sergei Lavrov",
    "Cuba Petroleum",
    "PDVSA",
    "Maduro Nicolas",
    "Korean Mining Development Trading Corporation",
    "Banco Central de Venezuela",
    "Myanmar Economic Holdings"
]

def check_sanctions(entity_name: str) -> dict:
    best_score = 0
    best_match = ""

    for entry in SANCTIONED_ENTITIES:
        score = fuzz.token_sort_ratio(entity_name.lower(), entry.lower())
        if score > best_score:
            best_score = score
            best_match = entry

    hit = best_score >= 75

    return {
        "entity": entity_name,
        "sanctions_hit": hit,
        "confidence": best_score,
        "matched_entry": best_match if hit else None
    }