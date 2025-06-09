import streamlit as st
import math
import os
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Oddsparks Recipe Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .section-header {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .item-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f9f9f9;
    }
    .base-ingredient {
        border-left: 4px solid #4CAF50;
        background: #f0fff0;
    }
    .intermediate-ingredient {
        border-left: 4px solid #2196F3;
        background: #f0f8ff;
    }
    .direct-ingredient {
        border-left: 4px solid #FF9800;
        background: #fff8f0;
    }
    .stSelectbox > div > div {
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Recipe definitions (same as your original)
recipes = {
    # Sparks
    "Stumpy Spark": {"output": 1, "ingredients": {"Aether Shard": 1, "Wooden Log": 5}},
    "Crafty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Wooden Panel": 2}},
    "Loamy Spark": {"output": 1, "ingredients": {"Aether Shard": 5, "Fertiliser": 3}},
    "Choppy Spark": {"output": 1, "ingredients": {"Stumpy Spark": 3, "Wooden Blade": 1}},
    "Carry Spark": {"output": 1, "ingredients": {"Crafty Spark": 1, "Sawn Timber": 4}},
    "Rocky Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Stone": 5}},
    "Hauling Spark": {"output": 1, "ingredients": {"Carry Spark": 2, "Stone Wheel": 4}},
    "Scouty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 1, "Dowsing Stone": 1}},
    "Boomy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Explosives": 3}},
    "Puffy Spark": {"output": 1, "ingredients": {"Rocky Spark": 1, "Fabric": 4}},
    "Crashy Spark": {"output": 1, "ingredients": {"Boomy Spark": 2, "Stone Spike": 5}},
    "Slashy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Choppy Spark": 3}},
    
    # Items
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
    
    "Aetheric Clump": {"output": 1, "ingredients": {"Large Enemy": 1}},
    "Aetheric Pellet": {"output": 3, "ingredients": {"Aetheric Clump": 1}},
    "Miasma Vial": {"output": 1, "ingredients": {"Small Vial": 2, "Miasma": 2}},
    "Raw Aether": {"output": 1, "ingredients": {"Miasma Vial": 2, "Aether Shard": 1}},
    "Refined Aether": {"output": 1, "ingredients": {"Raw Aether": 3, "Large Vial": 1}},
    
    # Buildings
    "Sawbench": {"output": 1, "ingredients": {"Wooden Log": 15}},
    "Aetheric Distiller": {"output": 1, "ingredients": {"Stone": 15, "Large Vial": 3, "Aether Shard": 5}},
    "Cutter": {"output": 1, "ingredients": {"Wooden Panel": 8, "Stone Plate": 5, "Wooden Blade": 2}},
    "Stonecutter": {"output": 1, "ingredients": {"Stone": 20, "Stone Plate": 8, "Stone Wheel": 2}},
    "Furnace": {"output": 1, "ingredients": {"Stone": 25, "Coal": 10, "Stone Plate": 5}},
    "Spark Workbench": {"output": 1, "ingredients": {"Wooden Panel": 8, "Stumpy Spark": 1, "Aether Shard": 3}},
    "Spark Workstation": {"output": 1, "ingredients": {"Wooden Panel": 10, "Crafty Spark": 1, "Aether Shard": 5}},
    "Wood Workshop": {"output": 1, "ingredients": {"Wooden Panel": 10, "Sawn Timber": 12, "Wooden Blade": 1}},
    "Loom": {"output": 1, "ingredients": {"Wooden Panel": 8, "Fabric": 4, "Tree Bark": 8}},
    "Stone Workshop": {"output": 1, "ingredients": {"Stone": 15, "Stone Plate": 8, "Wooden Panel": 5}},
    "Alchemy Lab": {"output": 1, "ingredients": {"Stone Plate": 8, "Large Vial": 3, "Small Vial": 8}},
    "Logger": {"output": 1, "ingredients": {"Wooden Panel": 12, "Choppy Spark": 1, "Wooden Blade": 2}},
    "Drill": {"output": 1, "ingredients": {"Stone Plate": 12, "Rocky Spark": 1, "Stone Spike": 2}},
    "Miasma Collector": {"output": 1, "ingredients": {"Stone Plate": 8, "Large Vial": 3, "Aether Shard": 5}},
    "Shed": {"output": 1, "ingredients": {"Wooden Panel": 15, "Sawn Timber": 12}},
    "Barrel": {"output": 1, "ingredients": {"Wooden Panel": 5, "Rope": 2}},
    "Crate": {"output": 1, "ingredients": {"Sawn Timber": 10}},
    "Spark Pen": {"output": 1, "ingredients": {"Wooden Panel": 8, "Aether Shard": 3}},
    "Supply Chest": {"output": 1, "ingredients": {"Wooden Panel": 12, "Stone Plate": 4}},
    "Big Barrel": {"output": 1, "ingredients": {"Wooden Panel": 10, "Rope": 4}},
    "Big Crate": {"output": 1, "ingredients": {"Sawn Timber": 20, "Wooden Panel": 5}},
    "Large Spark Pen": {"output": 1, "ingredients": {"Wooden Panel": 15, "Aether Shard": 8, "Aetheric Pellet": 3}},
}

# Machine requirements (same as your original)
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

# Categories (same as your original)
categories = {
    "Spark Types": {
        "Woodland Sparks": ["Stumpy Spark", "Crafty Spark", "Loamy Spark", "Choppy Spark", "Carry Spark"],
        "Mountain Sparks": ["Rocky Spark", "Hauling Spark", "Scouty Spark", "Boomy Spark", "Puffy Spark", "Crashy Spark", "Slashy Spark"]
    },
    "Items": {
        "Woodland Items": ["Beelephant Carapace", "Tree Bark", "Coal", "Mantis Stag Antler", "Fabric", "Fertiliser", "Ladder", "Leaves", "Wooden Log", "Sawn Timber", "Wooden Panel", "Rope", "Wooden Blade"],
        "Mountain Items": ["Large Vial", "Coral", "Dowsing Stone", "Frowl Sac", "Pengus Tendon", "Rock Teron Shell", "Squilican Tube", "Explosives", "Fluted Coral", "Limestone", "Path Tile", "Pebble", "Quartz", "Small Vial", "Stone", "Stone Plate", "Stone Spike", "Stone Wheel"],
        "Magic Items": ["Aether Crystal", "Aetheric Clump", "Aetheric Pellet", "Aether Shard", "Fog", "Miasma Vial", "Liquid Fertilizer", "Raw Aether", "Refined Aether", "Miasma"],
    },
    "Buildings": {
        "Refiners": ["Sawbench", "Aetheric Distiller", "Cutter", "Stonecutter", "Furnace"],
        "Assemblers": ["Spark Workbench", "Spark Workstation", "Wood Workshop", "Loom", "Stone Workshop", "Alchemy Lab"],
        "Harvesters": ["Logger", "Drill", "Miasma Collector"],
        "Storages": ["Shed", "Barrel", "Crate", "Spark Pen", "Supply Chest", "Big Barrel", "Big Crate", "Large Spark Pen"],
    }
}

def load_icon(item_name):
    """Load icon for an item if it exists"""
    try:
        filename = item_name.lower().replace(" ", "_") + ".png"
        icon_path = os.path.join("assets", "icons", filename)
        if os.path.exists(icon_path):
            return Image.open(icon_path)
        return None
    except:
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
    """Display an item with its icon and quantity"""
    col1, col2, col3 = st.columns([1, 6, 3])
    
    with col1:
        icon = load_icon(item_name)
        if icon:
            st.image(icon, width=40)
        else:
            st.write("🔧")  # Fallback emoji
    
    with col2:
        if item_type == "base":
            st.markdown(f"**{item_name}**")
        elif item_type == "intermediate":
            st.markdown(f"*{item_name}*")
        else:
            st.write(item_name)
    
    with col3:
        if item_type == "base":
            st.markdown(f"**{quantity:,}**")
        else:
            st.write(f"{quantity:,}")
    
    # Show machine requirement if applicable
    if item_name in machine_requirements:
        machine_info = machine_requirements[item_name]
        st.caption(f"🏭 Requires: {machine_info['machine']} - {machine_info['description']}")

# Main App
st.markdown('<div class="main-header"><h1>⚡ Oddsparks Recipe Calculator</h1><p>Calculate crafting recipes and resource requirements</p></div>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Category filters
show_sparks = st.sidebar.checkbox("Show Sparks", value=True)
show_items = st.sidebar.checkbox("Show Items", value=True)
show_buildings = st.sidebar.checkbox("Show Buildings", value=True)

# Search functionality
search_term = st.sidebar.text_input("🔍 Search items:", placeholder="Type to filter...")

# Get filtered items
filtered_items = []

if show_sparks:
    for subcategory, items in categories["Spark Types"].items():
        filtered_items.extend(items)

if show_items:
    for subcategory, items in categories["Items"].items():
        filtered_items.extend(items)

if show_buildings:
    for subcategory, items in categories["Buildings"].items():
        filtered_items.extend(items)

# Apply search filter
if search_term:
    filtered_items = [item for item in filtered_items if search_term.lower() in item.lower()]

# Sort items
filtered_items = sorted(list(set(filtered_items)))

# Main interface
col1, col2 = st.columns([2, 3])

with col1:
    st.header("📋 Recipe Selection")
    
    if not filtered_items:
        st.warning("No items match your current filters.")
    else:
        # Item selection
        selected_item = st.selectbox(
            "Choose an item to craft:",
            options=filtered_items,
            index=0 if filtered_items else None,
            help="Select an item to see its crafting recipe"
        )
        
        # Show item icon if available
        if selected_item:
            icon = load_icon(selected_item)
            if icon:
                st.image(icon, width=80, caption=selected_item)
        
        # Quantity input
        quantity = st.number_input(
            "How many do you need?",
            min_value=1,
            value=1,
            step=1,
            help="Enter the number of items you want to craft"
        )
        
        # Calculate button
        calculate_pressed = st.button("🧮 Calculate Recipe", type="primary")

with col2:
    st.header("📊 Recipe Results")
    
    if 'selected_item' in locals() and selected_item and calculate_pressed:
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
                st.info(f"Each batch produces {output_qty} items • {batches_needed} batch{'es' if batches_needed != 1 else ''} needed")
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
    
    elif not ('selected_item' in locals() and selected_item):
        st.info("👆 Select an item and click Calculate to see the recipe breakdown!")
    else:
        st.info("👆 Click the Calculate Recipe button to see the results!")

# Footer
st.markdown("---")
st.markdown("*Made for Oddsparks players - Calculate optimal crafting recipes and resource requirements*")