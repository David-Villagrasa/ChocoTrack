jockey_rank = {"Unknown": 0, "Bronze": 1, "Silver": 2, "Gold": 3, "Plat": 4}

def get_top_3(chocobos):
    """Return the top 3 chocobos based on performance."""
    return [c[0] for c in chocobos[:3]] if len(chocobos) >= 3 else []

def generate_bets(top_3):
    """Generate paired bets from the top 3 chocobos."""
    return [f"[{top_3[0]}-{top_3[1]}]", f"[{top_3[0]}-{top_3[2]}]", f"[{top_3[1]}-{top_3[2]}]"] if len(top_3) == 3 else []

def calculate_winning_bets(chocobos):
    """Compute the winning bets based on chocobo performance."""
    min_jockey_rank = min(jockey_rank[c[3]] for c in chocobos)
    chocobos_filtered = [c for c in chocobos if jockey_rank[c[3]] > min_jockey_rank]
    
    if len(chocobos_filtered) < 3:
        chocobos_filtered = chocobos  

    chocobos_sorted_1 = sorted(chocobos_filtered, key=lambda x: x[4], reverse=True)
    chocobos_sorted_2 = sorted(chocobos_filtered, key=lambda x: (x[1], jockey_rank[x[3]]), reverse=True)
    chocobos_sorted_3 = sorted(chocobos, key=lambda x: x[4], reverse=True)

    return {
        "method_1": generate_bets(get_top_3(chocobos_sorted_1)),
        "method_2": generate_bets(get_top_3(chocobos_sorted_2)),
        "method_3": generate_bets(get_top_3(chocobos_sorted_3)),
    }
