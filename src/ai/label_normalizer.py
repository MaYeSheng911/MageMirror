def normalize_category(category):

    if not category:
        return "unknown"

    category = category.lower().strip()

    mapping = {

        # ===== TOP =====

        "shirt": "shirt",
        "tshirt": "t-shirt",
        "t-shirt": "t-shirt",
        "tee": "t-shirt",

        # ===== OUTER =====

        "jacket": "outer",
        "coat": "outer",
        "hoodie": "outer",
        "blazer": "outer",
        "suit jacket": "outer",
        "windbreaker": "outer",

        # ===== BOTTOM =====

        "pants": "pants",
        "trousers": "pants",
        "jeans": "jeans",
        "shorts": "shorts",

        # ===== SHOES =====

        "shoes": "shoes",
        "sneakers": "shoes",
        "boots": "shoes"

    }

    return mapping.get(category, category)

def normalize_color(color):

    color = color.lower()

    mapping = {

        "dark": "black",
        "navy": "blue",
        "sky blue": "blue",

        "light gray": "gray",
        "dark gray": "gray",

        "beige": "brown"

    }

    return mapping.get(color, color)


def normalize_season(season):

    season = season.lower()

    mapping = {

        "fall": "autumn"

    }

    return mapping.get(season, season)


def normalize_style(style):

    style = style.lower()

    mapping = {

        "daily": "casual",
        "sports": "sport"

    }

    return mapping.get(style, style)
