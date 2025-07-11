from collections import defaultdict
from .logger import log_message



# def process_equipment(deck_data):
#     """Extract all equipment items"""
#     if not deck_data or not isinstance(deck_data, dict):
#         return {}
    
    
#     equipment = {
#         "weapons": [], "head": [], "chest": [],
#         "arms": [], "legs": [], "offhand": []
#     }
    
#     # Main equipment
#     for slot in equipment.keys():
#         items = deck_data.get(slot, [])
#         if items:
#             if slot == "weapons" and isinstance(items[0], dict):
#                 equipment[slot] = [w["id"] for w in items if "id" in w]
#             else:
#                 equipment[slot] = items
    
#     # Sideboard equipment
#     for slot in ["headSB", "chestSB", "armsSB", "legsSB"]:
#         items = deck_data.get(slot, [])
#         if items:
#             equipment[slot.replace("SB", "")].extend(items)
    
#     return equipment

# In deck_parser.py
def process_equipment(deck_data):
    """Safer equipment processing"""
    equipment = {
        "weapons": [], "head": [], "chest": [],
        "arms": [], "legs": [], "offhand": []
    }
    
    if not deck_data or not isinstance(deck_data, dict):
        return equipment
    
    try:
        # Main equipment
        for slot in equipment.keys():
            items = deck_data.get(slot, [])
            if items and isinstance(items, list):  # Ensure it's a list
                if slot == "weapons" and items and isinstance(items[0], dict):
                    equipment[slot] = [w.get("id") for w in items if w and isinstance(w, dict)]
                else:
                    equipment[slot] = [item for item in items if item]
        
        # Sideboard equipment
        for slot in ["headSB", "chestSB", "armsSB", "legsSB"]:
            items = deck_data.get(slot, [])
            if items and isinstance(items, list):
                base_slot = slot.replace("SB", "")
                if base_slot in equipment:
                    equipment[base_slot].extend(item for item in items if item)
                    
    except Exception as e:
        log_message(f"⚠️ Equipment processing error: {str(e)}")
    
    return equipment
def process_decklist(deck_data):
    """Analyze deck composition"""
    if not deck_data or not isinstance(deck_data, dict):
        return {
            "main_deck": defaultdict(int),
            "sideboard": [],
            "demi_hero": []
        }
    
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

# def format_deck_info(deck_data):
#     """Generate human-readable deck summary"""
#     if not deck_data:
#         return "No deck data available"
    
#     sections = []
    
#     # Hero and Format
#     sections.append(f"Hero: {deck_data.get('heroName', 'Unknown')}")
#     sections.append(f"Format: {deck_data.get('format', 'Unknown')}")
    
#     # Equipment
#     equipment = process_equipment(deck_data)
#     for slot, items in equipment.items():
#         if items:
#             sections.append(f"{slot.capitalize()}: {', '.join(items)}")
    
#     # Decklist
#     decklist = process_decklist(deck_data)
#     if decklist["main_deck"]:
#         cards_str = ", ".join([f"{card}x{count}" for card, count in decklist["main_deck"].items()])
#         sections.append(f"\nMain Deck ({sum(decklist['main_deck'].values())} cards):")
#         sections.append(cards_str)
    
#     if decklist["sideboard"]:
#         sections.append(f"\nSideboard ({len(decklist['sideboard'])} cards):")
#         sections.append(", ".join(decklist["sideboard"]))
    
#     return "\n".join(sections)
# In deck_parser.py
def format_deck_info(deck_data):
    """Generate human-readable deck summary"""
    if not deck_data or not isinstance(deck_data, dict):
        return "No deck data available"
    
    try:
        sections = []
        
        # Hero and Format
        hero_name = deck_data.get('heroName', 'Unknown')
        format_type = deck_data.get('format', 'Unknown')
        sections.append(f"Hero: {hero_name}")
        sections.append(f"Format: {format_type}")
        
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
    except Exception as e:
        return f"Error formatting deck info: {str(e)}"

