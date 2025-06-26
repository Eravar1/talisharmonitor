from collections import defaultdict

def process_equipment(deck_data):
    """Extract all equipment items"""
    if not deck_data:
        return {}
    
    equipment = {
        "weapons": [], "head": [], "chest": [],
        "arms": [], "legs": [], "offhand": []
    }
    
    # Main equipment
    for slot in equipment.keys():
        items = deck_data.get(slot, [])
        if items:
            if slot == "weapons" and isinstance(items[0], dict):
                equipment[slot] = [w["id"] for w in items if "id" in w]
            else:
                equipment[slot] = items
    
    # Sideboard equipment
    for slot in ["headSB", "chestSB", "armsSB", "legsSB"]:
        items = deck_data.get(slot, [])
        if items:
            equipment[slot.replace("SB", "")].extend(items)
    
    return equipment

def process_decklist(deck_data):
    """Analyze deck composition"""
    if not deck_data:
        return {}
    
    decklist = {
        "main_deck": defaultdict(int),
        "sideboard": [],
        "demi_hero": []
    }
    
    # Main deck cards
    for card in deck_data.get("cards", []):
        decklist["main_deck"][card] += 1
    
    # Sideboard cards
    decklist["sideboard"] = deck_data.get("cardsSB", [])
    
    # Demi-hero cards
    decklist["demi_hero"] = deck_data.get("demiHero", [])
    
    return decklist

def format_deck_info(deck_data):
    """Generate human-readable deck summary"""
    if not deck_data:
        return "No deck data available"
    
    sections = []
    
    # Hero and Format
    sections.append(f"Hero: {deck_data.get('heroName', 'Unknown')}")
    sections.append(f"Format: {deck_data.get('format', 'Unknown')}")
    
    # Equipment
    equipment = process_equipment(deck_data)
    for slot, items in equipment.items():
        if items:
            sections.append(f"{slot.capitalize()}: {', '.join(items)}")
    
    # Decklist
    decklist = process_decklist(deck_data)
    if decklist["main_deck"]:
        cards_str = ", ".join([f"{card}x{count}" for card, count in decklist["main_deck"].items()])
        sections.append(f"\nMain Deck ({sum(decklist['main_deck'].values())} cards):")
        sections.append(cards_str)
    
    if decklist["sideboard"]:
        sections.append(f"\nSideboard ({len(decklist['sideboard'])} cards):")
        sections.append(", ".join(decklist["sideboard"]))
    
    return "\n".join(sections)