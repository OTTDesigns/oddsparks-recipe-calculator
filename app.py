import streamlit as st
import math
import os
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Oddsparks Crafting Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling that matches your original design
st.markdown("""
<style>
    /* Main theme colors similar to your original */
    .main {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #1e1e1e;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #4a9eff 0%, #357abd 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(74, 158, 255, 0.3);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
    }
    
    /* Item cards with modern styling */
    .item-card {
        border: 1px solid #444444;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        background: #2d2d2d;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .item-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }
    
    /* Base ingredients - green accent */
    .base-ingredient {
        border-left: 4px solid #50c878;
        background: linear-gradient(135deg, #2d4a2d 0%, #2d2d2d 100%);
    }
    
    /* Intermediate ingredients - blue accent */
    .intermediate-ingredient {
        border-left: 4px solid #4a9eff;
        background: linear-gradient(135deg, #2d3d4a 0%, #2d2d2d 100%);
    }
    
    /* Direct ingredients - orange accent */
    .direct-ingredient {
        border-left: 4px solid #ff9800;
        background: linear-gradient(135deg, #4a3d2d 0%, #2d2d2d 100%);
    }
    
    /* Item grid styling */
    .item-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 15px;
        padding: 20px;
        background: #2d2d2d;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .item-button {
        background: #3d3d3d;
        border: 2px solid #555555;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .item-button:hover {
        border-color: #4a9eff;
        background: #4d4d4d;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 158, 255, 0.3);
    }
    
    .item-button.selected {
        border-color: #4a9eff;
        background: #357abd;
        color: white;
    }
    
    /* Machine requirement styling */
    .machine-req {
        background: #3d3d3d;
        border: 1px solid #555555;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        color: #b8b8b8;
    }
    
    /* Batch info styling */
    .batch-info {
        background: #2a2a2a;
        border: 1px solid #4a9eff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #4a9eff;
    }
    
    /* Category filter buttons */
    .filter-button {
        background: #3d3d3d;
        color: #b8b8b8;
        border: 1px solid #555555;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .filter-button.active {
        background: #4a9eff;
        color: white;
        border-color: #4a9eff;
    }
    
    /* Streamlit component overrides */
    .stSelectbox > div > div {
        background-color: #3d3d3d;
        color: white;
        border: 1px solid #555555;
    }
    
    .stNumberInput > div > div > input {
        background-color: #3d3d3d;
        color: white;
        border: 1px solid #555555;
    }
    
    .stTextInput > div > div > input {
        background-color: #3d3d3d;
        color: white;
        border: 1px solid #555555;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2d2d2d;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #3d3d3d;
        color: #b8b8b8;
        border-radius: 8px 8px 0px 0px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4a9eff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Complete recipe definitions (exactly like your original)
recipes = {
    # Sparks - Woodland
    "Stumpy Spark": {"output": 1, "ingredients": {"Aether Shard": 1, "Wooden Log": 5}},
    "Crafty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Wooden Panel": 2}},
    "Loamy Spark": {"output": 1, "ingredients": {"Aether Shard": 5, "Fertiliser": 3}},
    "Choppy Spark": {"output": 1, "ingredients": {"Stumpy Spark": 3, "Wooden Blade": 1}},
    "Carry Spark": {"output": 1, "ingredients": {"Crafty Spark": 1, "Sawn Timber": 4}},
    
    # Sparks - Mountain
    "Rocky Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Stone": 5}},
    "Hauling Spark": {"output": 1, "ingredients": {"Carry Spark": 2, "Stone Wheel": 4}},
    "Scouty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 1, "Dowsing Stone": 1}},
    "Boomy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Explosives": 3}},
    "Puffy Spark": {"output": 1, "ingredients": {"Rocky Spark": 1, "Fabric": 4}},
    "Crashy Spark": {"output": 1, "ingredients": {"Boomy Spark": 2, "Stone Spike": 5}},
    "Slashy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Choppy Spark": 3}},
    
    # Items - Woodland
    "Beelephant Carapace": {"output": 1, "ingredients": {"Beelephant": 1}},
    "Tree Bark": {"output": 3, "ingredients": {"Wooden Log": 1}},
    "Coal": {"output": 2, "ingredients": {"Wooden Log": 3}},
    "Mantis Stag Antler": {"output": 1, "ingredients": {"Mantis Stag": 1}},
    "Fabric": {"output": 1, "ingredients": {"Tree Bark": 4, "Rope": 2}},
    "Fertiliser": {"output": 2, "ingredients": {"Leaves": 4}},
    "Ladder": {"output": 1, "ingredients": {"Wooden Log": 4, "Sawn Timber": 10}},
    "Sawn Timber": {"output": 4, "ingredients": {"Wooden Log": 1}},
    "Wooden Panel": {"output": 1, "ingredients": {"Sawn Timber": 6}},
    "Rope": {"output": 2, "ingredients": {"Tree Bark": 1, "Leaves": 2}},
    "Wooden Blade": {"output": 1, "ingredients": {"Sawn Timber": 3, "Wooden Panel": 1}},
    
    # Items - Mountain
    "Large Vial": {"output": 1, "ingredients": {"Quartz": 5, "Coal": 1}},
    "Dowsing Stone": {"output": 3, "ingredients": {"Quartz": 1, "Rope": 1}},
    "Frowl Sac": {"output": 1, "ingredients": {"Frowl": 1}},
    "Pengus Tendon": {"output": 1, "ingredients": {"Pengus": 1}},
    "Rock Teron Shell": {"output": 1, "ingredients": {"Rock Teron": 1}},
    "Squilican Tube": {"output": 1, "ingredients": {"Squilican": 1}},
    "Explosives": {"output": 3, "ingredients": {"Fertiliser": 2, "Limestone": 4}},
    "Path Tile": {"output": 5, "ingredients": {"Pebble": 10, "Limestone": 5}},
    "Pebble": {"output": 5, "ingredients": {"Stone": 1}},
    "Small Vial": {"output": 2, "ingredients": {"Quartz": 2, "Coal": 1}},
    "Stone Plate": {"output": 2, "ingredients": {"Stone": 2}},
    "Stone Spike": {"output": 1, "ingredients": {"Wooden Blade": 1, "Stone Plate": 3}},
    "Stone Wheel": {"output": 1, "ingredients": {"Path Tile": 3, "Stone Plate": 2}},
    
    # Magic Items
    "Aetheric Clump": {"output": 1, "ingredients": {"Large Enemy": 1}},
    "Aetheric Pellet": {"output": 3, "ingredients": {"Aetheric Clump": 1}},
    "Miasma Vial": {"output": 1, "ingredients": {"Small Vial": 2, "Miasma": 2}},
    "Raw Aether": {"output": 1, "ingredients": {"Miasma Vial": 2, "Aether Shard": 1}},
    "Refined Aether": {"output": 1, "ingredients": {"Raw Aether": 3, "Large Vial": 1}},
    
    # Buildings - Refiners
    "Sawbench": {"output": 1, "ingredients": {"Wooden Log": 15}},
    "Aetheric Distiller": {"output": 1, "ingredients": {"Stone": 15, "Large Vial": 3, "Aether Shard": 5}},
    "Cutter": {"output": 1, "ingredients": {"Wooden Panel": 8, "Stone Plate": 5, "Wooden Blade": 2}},
    "Stonecutter": {"output": 1, "ingredients": {"Stone": 20, "Stone Plate": 8, "Stone Wheel": 2}},
    "Furnace": {"output": 1, "ingredients": {"Stone": 25, "Coal": 10, "Stone Plate": 5}},
    
    # Buildings - Assemblers
    "Spark Workbench": {"output": 1, "ingredients": {"Wooden Panel": 8, "Stumpy Spark": 1, "Aether Shard": 3}},
    "Spark Workstation": {"output": 1, "ingredients": {"Wooden Panel": 10, "Crafty Spark": 1, "Aether Shard": 5}},
    "Wood Workshop": {"output": 1, "ingredients": {"Wooden Panel": 10, "Sawn Timber": 12, "Wooden Blade": 1}},
    "Loom": {"output": 1, "ingredients": {"Wooden Panel": 8, "Fabric": 4, "Tree Bark": 8}},
    "Stone Workshop": {"output": 1, "ingredients": {"Stone": 15, "Stone Plate": 8, "Wooden Panel": 5}},
    "Alchemy Lab": {"output": 1, "ingredients": {"Stone Plate": 8, "Large Vial": 3, "Small Vial": 8}},
    
    # Buildings - Harvesters
    "Logger": {"output": 1, "ingredients": {"Wooden Panel": 12, "Choppy Spark": 1, "Wooden Blade": 2}},
    "Drill": {"output": 1, "ingredients": {"Stone Plate": 12, "Rocky Spark": 1, "Stone Spike": 2}},
    "Miasma Collector": {"output": 1, "ingredients": {"Stone Plate": 8, "Large Vial": 3, "Aether Shard": 5}},
    
    # Buildings - Storages
    "Shed": {"output": 1, "ingredients": {"Wooden Panel": 15, "Sawn Timber": 12}},
    "Barrel": {"output": 1, "ingredients": {"Wooden Panel": 5, "Rope": 2}},
    "Crate": {"output": 1, "ingredients": {"Sawn Timber": 10}},
    "Spark Pen": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 3}},
    "Supply Chest": {"output": 1, "ingredients": {"Wooden Panel": 12, "Stone Plate": 4}},
    "Big Barrel": {"output": 1, "ingredients": {"Wooden Panel": 10, "Rope": 4}},
    "Big Crate": {"output": 1, "ingredients": {"Sawn Timber": 20, "Wooden Panel": 5}},
    "Large Spark Pen": {"output": 1, "ingredients": {"Wooden Panel": 15, "Aether Shard": 8, "Aetheric Pellet": 3}},
    
    # Buildings - Delivery Chests
    "Delivery Chest Mayor": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    "Delivery Chest Divine Researcher": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    "Delivery Chest Woodsman": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    "Delivery Chest Quartermaster": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    "Delivery Chest Merchant": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    "Delivery Chest Mason Sisters": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 2}},
    
    # Buildings - Path AddOns
    "Spark Itemiser": {"output": 1, "ingredients": {"Wooden Panel": 4, "Aether Shard": 2}},
    "Spark Activator": {"output": 1, "ingredients": {"Stone Plate": 4, "Aether Shard": 2}},
    "Signpost": {"output": 1, "ingredients": {"Wooden Log": 2, "Wooden Panel": 1}},
    "Stone Path": {"output": 5, "ingredients": {"Stone": 8, "Pebble": 4}},
    "Animal Scarer": {"output": 1, "ingredients": {"Wooden Panel": 4, "Fabric": 2}},
    "Amount Filter": {"output": 1, "ingredients": {"Wooden Panel": 4, "Stone Plate": 2}},
    "Item Filter": {"output": 1, "ingredients": {"Wooden Panel": 4, "Stone Plate": 2}},
    "Crossing": {"output": 1, "ingredients": {"Stone Path": 3}},
    "Blocker": {"output": 1, "ingredients": {"Stone Plate": 2, "Stone": 4}},
    "Spark Filter": {"output": 1, "ingredients": {"Wooden Panel": 4, "Aether Shard": 2}},
    "Wait Gate": {"output": 1, "ingredients": {"Stone Plate": 4, "Wooden Panel": 2}},
    "Splitter": {"output": 1, "ingredients": {"Stone Path": 2, "Stone Plate": 1}},
    "One Way": {"output": 1, "ingredients": {"Stone Path": 1, "Stone Plate": 1}},
    "Counter": {"output": 1, "ingredients": {"Stone Plate": 4, "Wooden Panel": 2}},
    "Ladder Built": {"output": 1, "ingredients": {"Ladder": 1}},
    "Ramp": {"output": 1, "ingredients": {"Stone": 12, "Stone Path": 4}},
    "Zipline": {"output": 1, "ingredients": {"Wooden Panel": 8, "Rope": 12}},
    "Elevator": {"output": 1, "ingredients": {"Stone Plate": 12, "Stone Wheel": 3, "Rope": 8}},
    "Cannon": {"output": 1, "ingredients": {"Stone Plate": 8, "Explosives": 4}},
}

# Machine requirements (exactly like your original)
machine_requirements = {
    "Sawn Timber": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    "Wooden Panel": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    "Wooden Blade": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    "Coal": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    "Large Vial": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    "Small Vial": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    "Tree Bark": {"machine": "Cutter", "description": "Cuts and processes materials"},
    "Pebble": {"machine": "Cutter", "description": "Cuts and processes materials"},
    "Stone Plate": {"machine": "Cutter", "description": "Cuts and processes materials"},
    "Path Tile": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    "Stone Wheel": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    "Stone Spike": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    "Fabric": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    "Ladder": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    "Rope": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    "Explosives": {"machine": "Stone Workshop", "description": "Crafts complex stone items"},
    "Dowsing Stone": {"machine": "Stone Workshop", "description": "Crafts complex stone items"},
    "Fertiliser": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Miasma Vial": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Raw Aether": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Refined Aether": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Aetheric Pellet": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Stumpy Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Loamy Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Rocky Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Scouty Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Crafty Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Choppy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Carry Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Hauling Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Boomy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Puffy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Crashy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Slashy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
}

# Categories (exactly like your original)
categories = {
    "Spark Types": {
        "Woodland Sparks": ["Stumpy Spark", "Crafty Spark", "Loamy Spark", "Choppy Spark", "Carry Spark"],
        "Mountain Sparks": ["Rocky Spark", "Hauling Spark", "Scouty Spark", "Boomy Spark", "Puffy Spark", "Crashy Spark", "Slashy Spark"]
    },
    "Items": {
        "Woodland Items": ["Beelephant Carapace", "Tree Bark", "Coal", "Mantis Stag Antler", "Fabric", "Fertiliser", "Ladder", "Leaves", "Wooden Log", "Sawn Timber", "Wooden Panel", "Rope", "Wooden Blade"],
        "Mountain Items": ["Large Vial", "Coral", "Dowsing Stone", "Frowl Sac", "Pengus Tendon", "Rock Teron Shell", "Squilican Tube", "Explosives", "Fluted Coral", "Limestone", "Path Tile", "Pebble", "Quartz", "Small Vial", "Stone", "Stone Plate", "Stone Spike", "Stone Wheel"],
        "Magic Items": ["Aether Crystal", "Aetheric Clump", "Aetheric Pellet", "Aether Shard", "Fog", "Miasma Vial", "Liquid Fertilizer", "Raw Aether", "Refined Aether", "Miasma"],
        "Cave Items": ["Volcanic Soil", "Lava Cap", "Glowshroom", "Shiny Geode", "Cracked Geode", "Bumpy Geode", "Copper Ore", "Copper Ingot", "Drill Bit", "Lava Shellhorse Comb", "Crangolin Scale", "Crangolin Lavascale"],
        "Plateau Items": ["Frozen Log", "Frozen Stone", "Stellar Ice", "Stellar Seed", "Frost", "Stellar Fertilizer", "Icehorn Ram Horn", "Frilled Walrion Tusk"],
        "Botanical Items": ["Leaf Knot", "Coral Seed", "Stellar Leaves", "Fireshroom Cluster", "Copper Seed", "Aether Flower", "Aether Seed", "Geode Cluster", "Copper Cuttings", "Copper Sap", "Aether Apple", "Aether Segment"]
    },
    "Buildings": {
        "Refiners": ["Sawbench", "Aetheric Distiller", "Cutter", "Stonecutter", "Furnace"],
        "Assemblers": ["Spark Workbench", "Spark Workstation", "Wood Workshop", "Loom", "Stone Workshop", "Alchemy Lab"],
        "Harvesters": ["Logger", "Drill", "Miasma Collector"],
        "Storages": ["Shed", "Barrel", "Crate", "Spark Pen", "Supply Chest", "Big Barrel", "Big Crate", "Large Spark Pen"],
        "Delivery Chests": ["Delivery Chest Mayor", "Delivery Chest Divine Researcher", "Delivery Chest Woodsman", "Delivery Chest Quartermaster", "Delivery Chest Merchant", "Delivery Chest Mason Sisters"],
        "Path AddOns": ["Spark Itemiser", "Spark Activator", "Signpost", "Stone Path", "Animal Scarer", "Amount Filter", "Item Filter", "Crossing", "Blocker", "Spark Filter", "Wait Gate", "Splitter", "One Way", "Counter", "Ladder Built", "Ramp", "Zipline", "Elevator", "Cannon"]
    }
}

# Initialize session state
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None
if 'show_sparks' not in st.session_state:
    st.session_state.show_sparks = True
if 'show_items' not in st.session_state:
    st.session_state.show_items = True
if 'show_buildings' not in st.session_state:
    st.session_state.show_buildings = True

@st.cache_data
def load_icon(item_name):
    """Load icon for an item if it exists - with correct path"""
    try:
        # Convert item name to filename format
        filename = item_name.lower().replace(" ", "_") + ".png"
        
        # Try multiple possible paths
        possible_paths = [
            os.path.join("assets", "icons", filename),
            os.path.join("icons", filename),
            filename
        ]
        
        for icon_path in possible_paths:
            if os.path.exists(icon_path):
                return Image.open(icon_path)
        
        return None
    except Exception as e:
        st.error(f"Error loading icon for {item_name}: {e}")
        return None

def get_recipe_info(item):
    """Get recipe ingredients and output quantity for an item."""
    if item not in recipes:
        return None, 1
    
    recipe_data = recipes[item]
    
    if isinstance(recipe_data, dict) and "ingredients" in recipe_data:
        ingredients = recipe_data["ingredients"]
        output_qty = recipe_data.get("output", 1)
    else:
        ingredients = recipe_data
        output_qty = 1
    
    return ingredients, output_qty

def calculate_batches_needed(needed_qty, output_per_batch):
    """Calculate how many batches needed to produce at least needed_qty items."""
    return math.ceil(needed_qty / output_per_batch)

def get_base_ingredients(item, qty, results=None):
    """Recursively accumulate only TRUE base ingredients."""
    if results is None:
        results = {}
    
    ingredients, output_qty = get_recipe_info(item)
    
    if ingredients is None:
        results[item] = results.get(item, 0) + qty
        return results
    
    batches_needed = calculate_batches_needed(qty, output_qty)
    
    for ingredient, amount in ingredients.items():
        get_base_ingredients(ingredient, amount * batches_needed, results)
    
    return results

def get_intermediate_materials(item, qty, intermediates=None, visited=None):
    """Get all intermediate materials needed."""
    if intermediates is None:
        intermediates = {}
    if visited is None:
        visited = set()
    
    ingredients, output_qty = get_recipe_info(item)
    
    if ingredients is None or item in visited:
        return intermediates
    
    visited.add(item)
    batches_needed = calculate_batches_needed(qty, output_qty)
    
    for ingredient, amount in ingredients.items():
        total_needed = amount * batches_needed
        
        ing_ingredients, _ = get_recipe_info(ingredient)
        if ing_ingredients is not None:
            intermediates[ingredient] = intermediates.get(ingredient, 0) + total_needed
            get_intermediate_materials(ingredient, total_needed, intermediates, visited.copy())
    
    return intermediates

def display_item_with_icon(item_name, quantity, item_type="direct"):
    """Display an item with its icon and quantity in a modern card layout"""
    
    # Create columns for layout
    icon_col, content_col, qty_col = st.columns([1, 6, 2])
    
    with icon_col:
        icon = load_icon(item_name)
        if icon:
            st.image(icon, width=50)
        else:
            st.markdown("🔧")  # Fallback emoji
    
    with content_col:
        # Item name with appropriate styling
        if item_type == "base":
            st.markdown(f"**{item_name}**")
        elif item_type == "intermediate":
            st.markdown(f"*{item_name}*")
        else:
            st.markdown(item_name)
        
        # Show machine requirement if applicable
        if item_name in machine_requirements:
            machine_info = machine_requirements[item_name]
            st.markdown(f'<div class="machine-req">🏭 {machine_info["machine"]} - {machine_info["description"]}</div>', unsafe_allow_html=True)
    
    with qty_col:
        # Quantity with appropriate styling
        if item_type == "base":
            st.markdown(f"**{quantity:,}**")
        else:
            st.markdown(f"{quantity:,}")

def get_filtered_items():
    """Get items based on current filters and search"""
    filtered_items = []
    search_term = st.session_state.get('search_term', '').lower()
    
    # Apply category filters
    if st.session_state.show_sparks:
        for subcategory, items in categories["Spark Types"].items():
            filtered_items.extend(items)
    
    if st.session_state.show_items:
        for subcategory, items in categories["Items"].items():
            filtered_items.extend(items)
    
    if st.session_state.show_buildings:
        for subcategory, items in categories["Buildings"].items():
            filtered_items.extend(items)
    
    # Apply search filter
    if search_term:
        filtered_items = [item for item in filtered_items if search_term in item.lower()]
    
    return sorted(list(set(filtered_items)))

def create_item_grid(items):
    """Create a responsive grid of items with icons"""
    if not items:
        st.warning("No items match your current filters.")
        return
    
    # Create grid layout
    cols_per_row = 4
    rows = [items[i:i + cols_per_row] for i in range(0, len(items), cols_per_row)]
    
    for row in rows:
        cols = st.columns(cols_per_row)
        for i, item in enumerate(row):
            with cols[i]:
                # Create item button
                icon = load_icon(item)
                
                # Display icon and name
                if icon:
                    st.image(icon, width=60)
                else:
                    st.markdown("🔧")
                
                # Item selection button
                is_selected = st.session_state.selected_item == item
                button_style = "selected" if is_selected else ""
                
                if st.button(item, key=f"btn_{item}", help=f"Select {item}"):
                    st.session_state.selected_item = item
                    st.rerun()

# Main App Header
st.markdown('<div class="main-header"><h1>⚡ Oddsparks Recipe Calculator</h1><p>Calculate crafting recipes and resource requirements for all your Oddsparks projects</p></div>', unsafe_allow_html=True)

# Sidebar filters (similar to your original categories)
with st.sidebar:
    st.header("🔍 Filters & Search")
    
    # Search functionality
    search_term = st.text_input("🔍 Search items:", placeholder="Type to filter...", key="search_input")
    if search_term != st.session_state.get('search_term', ''):
        st.session_state.search_term = search_term
    
    st.markdown("---")
    
    # Category toggles
    st.subheader("Categories")
    
    new_show_sparks = st.checkbox("⚡ Show Sparks", value=st.session_state.show_sparks)
    if new_show_sparks != st.session_state.show_sparks:
        st.session_state.show_sparks = new_show_sparks
        st.rerun()
    
    new_show_items = st.checkbox("🔧 Show Items", value=st.session_state.show_items)
    if new_show_items != st.session_state.show_items:
        st.session_state.show_items = new_show_items
        st.rerun()
    
    new_show_buildings = st.checkbox("🏗️ Show Buildings", value=st.session_state.show_buildings)
    if new_show_buildings != st.session_state.show_buildings:
        st.session_state.show_buildings = new_show_buildings
        st.rerun()
    
    # Subcategory filters (collapsible)
    if st.session_state.show_sparks:
        with st.expander("Spark Types"):
            st.checkbox("🌲 Woodland Sparks", value=True, key="woodland_sparks")
            st.checkbox("⛰️ Mountain Sparks", value=True, key="mountain_sparks")
    
    if st.session_state.show_items:
        with st.expander("Item Types"):
            st.checkbox("🌲 Woodland Items", value=True, key="woodland_items")
            st.checkbox("⛰️ Mountain Items", value=True, key="mountain_items")
            st.checkbox("✨ Magic Items", value=True, key="magic_items")
            st.checkbox("🕳️ Cave Items", value=True, key="cave_items")
            st.checkbox("🏔️ Plateau Items", value=True, key="plateau_items")
            st.checkbox("🌿 Botanical Items", value=True, key="botanical_items")
    
    if st.session_state.show_buildings:
        with st.expander("Building Types"):
            st.checkbox("⚙️ Refiners", value=True, key="refiners")
            st.checkbox("🔨 Assemblers", value=True, key="assemblers")
            st.checkbox("⛏️ Harvesters", value=True, key="harvesters")
            st.checkbox("📦 Storages", value=True, key="storages")
            st.checkbox("📮 Delivery Chests", value=True, key="delivery")
            st.checkbox("🛤️ Path Add-ons", value=True, key="path_addons")

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-header">📋 Item Selection</div>', unsafe_allow_html=True)
    
    # Get filtered items
    filtered_items = get_filtered_items()
    
    if not filtered_items:
        st.warning("No items match your current filters. Try adjusting your search or category filters.")
    else:
        # Create item grid
        create_item_grid(filtered_items)

with col2:
    st.markdown('<div class="section-header">⚙️ Recipe Calculator</div>', unsafe_allow_html=True)
    
    # Show selected item
    if st.session_state.selected_item:
        selected_item = st.session_state.selected_item
        
        # Display selected item with icon
        col_icon, col_name = st.columns([1, 3])
        with col_icon:
            icon = load_icon(selected_item)
            if icon:
                st.image(icon, width=60)
        with col_name:
            st.markdown(f"### {selected_item}")
        
        # Quantity input
        quantity = st.number_input(
            "How many do you need?",
            min_value=1,
            value=1,
            step=1,
            help="Enter the number of items you want to craft"
        )
        
        # Calculate button
        if st.button("🧮 Calculate Recipe", type="primary", use_container_width=True):
            # Get recipe data
            ingredients, output_qty = get_recipe_info(selected_item)
            
            if ingredients is None:
                st.info(f"**{selected_item}** is a base resource that cannot be crafted. It must be gathered directly from the world.")
            else:
                # Calculate recipe
                batches_needed = calculate_batches_needed(quantity, output_qty)
                total_produced = batches_needed * output_qty
                
                # Show main recipe info
                st.success(f"Recipe for **{quantity:,} × {selected_item}**")
                
                # Show machine requirement for main item
                if selected_item in machine_requirements:
                    machine_info = machine_requirements[selected_item]
                    st.info(f"🏭 **Requires:** {machine_info['machine']} - {machine_info['description']}")
                
                # Show batch info if relevant
                if output_qty > 1:
                    st.markdown(f'<div class="batch-info">Each batch produces {output_qty} items • {batches_needed} batch{"es" if batches_needed != 1 else ""} needed</div>', unsafe_allow_html=True)
                    if total_produced > quantity:
                        st.warning(f"Will produce {total_produced} total ({total_produced - quantity} extra)")
                
                # Calculate all materials
                direct_ingredients = {ing: amt * batches_needed for ing, amt in ingredients.items()}
                intermediate_materials = get_intermediate_materials(selected_item, quantity)
                base_ingredients = get_base_ingredients(selected_item, quantity)
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["🔨 Direct Ingredients", "⚙️ Intermediate Materials", "🌱 Base Resources"])
                
                with tab1:
                    st.markdown('<div class="section-header">Direct Ingredients</div>', unsafe_allow_html=True)
                    if direct_ingredients:
                        for ing_name, amt in sorted(direct_ingredients.items()):
                            with st.container():
                                st.markdown('<div class="item-card direct-ingredient">', unsafe_allow_html=True)
                                display_item_with_icon(ing_name, amt, "direct")
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("No direct ingredients needed.")
                
                with tab2:
                    st.markdown('<div class="section-header">Intermediate Materials</div>', unsafe_allow_html=True)
                    if intermediate_materials:
                        for mat_name, amt in sorted(intermediate_materials.items()):
                            with st.container():
                                st.markdown('<div class="item-card intermediate-ingredient">', unsafe_allow_html=True)
                                display_item_with_icon(mat_name, amt, "intermediate")
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("No intermediate materials needed.")
                
                with tab3:
                    st.markdown('<div class="section-header">Base Resources Required</div>', unsafe_allow_html=True)
                    if base_ingredients:
                        for base_name, amt in sorted(base_ingredients.items()):
                            with st.container():
                                st.markdown('<div class="item-card base-ingredient">', unsafe_allow_html=True)
                                display_item_with_icon(base_name, amt, "base")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Summary
                        st.markdown("---")
                        total_unique_resources = len(base_ingredients)
                        total_items_needed = sum(base_ingredients.values())
                        st.info(f"**Summary:** {total_unique_resources} unique base resources • {total_items_needed:,} total items needed")
                    else:
                        st.info("No base resources needed.")
    
    else:
        st.info("👈 Select an item from the grid to see its recipe breakdown!")

# Footer
st.markdown("---")
st.markdown("*Made for the Oddsparks community - Calculate optimal crafting recipes and resource requirements*")
st.markdown("*Having issues with icons? Make sure they're in the `assets/icons/` folder with lowercase names and underscores instead of spaces.*")
