import streamlit as st
from PIL import Image
import os
import math
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Oddsparks Crafting Calculator",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Recipe definitions with output quantities
# Format: "Item": {"output": quantity, "ingredients": {ingredient: amount, ...}}
# If "output" is not specified, it defaults to 1
recipes = {
    # Sparks
    # Woodland Sparks
    "Stumpy Spark": {"output": 1, "ingredients": {"Aether Shard": 1, "Wooden Log": 5}},
    "Crafty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Wooden Panel": 2}},
    "Loamy Spark": {"output": 1, "ingredients": {"Aether Shard": 5, "Fertiliser": 3}},
    "Choppy Spark": {"output": 1, "ingredients": {"Stumpy Spark": 3, "Wooden Blade": 1}},
    "Carry Spark": {"output": 1, "ingredients": {"Crafty Spark": 1, "Sawn Timber": 4}},

    # Mountain Sparks
    "Rocky Spark": {"output": 1, "ingredients": {"Stumpy Spark": 2, "Stone": 5}},
    "Hauling Spark": {"output": 1, "ingredients": {"Carry Spark": 2, "Stone Wheel": 4}},
    "Scouty Spark": {"output": 1, "ingredients": {"Stumpy Spark": 1, "Dowsing Stone": 1}},
    "Boomy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Explosives": 3}},
    "Puffy Spark": {"output": 1, "ingredients": {"Rocky Spark": 1, "Fabric": 4}},
    "Crashy Spark": {"output": 1, "ingredients": {"Boomy Spark": 2, "Stone Spike": 5}},
    "Slashy Spark": {"output": 1, "ingredients": {"Rocky Spark": 2, "Choppy Spark": 3}},
   
    # Items
    # Woodland Items
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

    # Mountain Items
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

# Machine/Building requirements for crafting items
# Format: "Item": {"machine": "Machine Name", "description": "Brief description"}
machine_requirements = {
    # Items requiring Sawbench
    "Sawn Timber": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    "Wooden Panel": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    "Wooden Blade": {"machine": "Sawbench", "description": "Cuts logs into timber"},
    
    # Items requiring Furnace
    "Coal": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    "Large Vial": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    "Small Vial": {"machine": "Furnace", "description": "Burns materials at high temperature"},
    
    # Items requiring Cutter
    "Tree Bark": {"machine": "Cutter", "description": "Cuts and processes materials"},
    "Pebble": {"machine": "Cutter", "description": "Cuts and processes materials"},
    "Stone Plate": {"machine": "Cutter", "description": "Cuts and processes materials"},
    
    # Items requiring Stonecutter
    "Path Tile": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    "Stone Wheel": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    "Stone Spike": {"machine": "Stonecutter", "description": "Cuts and shapes stone"},
    
    # Items requiring Wood Workshop
    "Fabric": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    "Ladder": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    "Rope": {"machine": "Wood Workshop", "description": "Crafts complex wooden items"},
    
    # Items requiring Stone Workshop
    "Explosives": {"machine": "Stone Workshop", "description": "Crafts complex stone items"},
    "Dowsing Stone": {"machine": "Stone Workshop", "description": "Crafts complex stone items"},
    
    # Items requiring Loom
    "Fabric": {"machine": "Loom", "description": "Weaves fibers into fabric"},
    
    # Items requiring Alchemy Lab
    "Fertiliser": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Miasma Vial": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Raw Aether": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Refined Aether": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    "Aetheric Pellet": {"machine": "Alchemy Lab", "description": "Mixes alchemical compounds"},
    
    # Items requiring Aetheric Distiller
    "Refined Aether": {"machine": "Aetheric Distiller", "description": "Distills aetheric materials"},
    
    # Items requiring Spark Workbench
    "Stumpy Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Loamy Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Rocky Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    "Scouty Spark": {"machine": "Spark Workbench", "description": "Crafts basic sparks"},
    
    # Items requiring Spark Workstation
    "Crafty Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Choppy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Carry Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Hauling Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Boomy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Puffy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Crashy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
    "Slashy Spark": {"machine": "Spark Workstation", "description": "Crafts advanced sparks"},
}

# Define categories for items
categories = {
    "Sparks": [
        "Woodland Sparks", 
        "Mountain Sparks"
    ],
    "Items": [
        "Woodland Items", 
        "Mountain Items", 
        "Magic Items"
    ],
    "Buildings": [
        "Refiners", 
        "Assemblers", 
        "Harvesters", 
        "Storages", 
        "Delivery Chests", 
        "Path AddOns"
    ]
}

# Define subcategories and their items
subcategories = {
    "Woodland Sparks": ["Stumpy Spark", "Crafty Spark", "Loamy Spark", "Choppy Spark", "Carry Spark"],
    "Mountain Sparks": ["Rocky Spark", "Hauling Spark", "Scouty Spark", "Boomy Spark", "Puffy Spark", "Crashy Spark", "Slashy Spark"],
    "Woodland Items": ["Beelephant Carapace", "Tree Bark", "Coal", "Mantis Stag Antler", "Fabric", "Fertiliser", "Ladder", "Sawn Timber", "Wooden Panel", "Rope", "Wooden Blade"],
    "Mountain Items": ["Large Vial", "Dowsing Stone", "Frowl Sac", "Pengus Tendon", "Rock Teron Shell", "Squilican Tube", "Explosives", "Path Tile", "Pebble", "Small Vial", "Stone Plate", "Stone Spike", "Stone Wheel"],
    "Magic Items": ["Aetheric Clump", "Aetheric Pellet", "Miasma Vial", "Raw Aether", "Refined Aether"],
    "Refiners": ["Sawbench", "Aetheric Distiller", "Cutter", "Stonecutter", "Furnace"],
    "Assemblers": ["Spark Workbench", "Spark Workstation", "Wood Workshop", "Loom", "Stone Workshop", "Alchemy Lab"],
    "Harvesters": ["Logger", "Drill", "Miasma Collector"],
    "Storages": ["Shed", "Barrel", "Crate", "Spark Pen", "Supply Chest", "Big Barrel", "Big Crate", "Large Spark Pen"],
    "Delivery Chests": ["Delivery Chest Mayor", "Delivery Chest Divine Researcher", "Delivery Chest Woodsman", "Delivery Chest Quartermaster", "Delivery Chest Merchant", "Delivery Chest Mason Sisters"],
    "Path AddOns": ["Spark Itemiser", "Spark Activator", "Signpost", "Stone Path", "Animal Scarer", "Amount Filter", "Item Filter", "Crossing", "Blocker", "Spark Filter", "Wait Gate", "Splitter", "One Way", "Counter", "Ladder Built", "Ramp", "Zipline", "Elevator", "Cannon"]
}

# Function to calculate all ingredients needed for a recipe
def calculate_all_ingredients(item_name, quantity=1, memo=None):
    if memo is None:
        memo = {}
    
    if item_name not in recipes:
        # This is a base resource
        return {item_name: quantity}
    
    recipe = recipes[item_name]
    output_quantity = recipe.get("output", 1)
    
    # Calculate how many crafting operations we need
    batches_needed = math.ceil(quantity / output_quantity)
    
    # Initialize result dictionary
    result = {}
    
    # Process each ingredient
    for ingredient, amount in recipe["ingredients"].items():
        total_amount = amount * batches_needed
        
        if ingredient in recipes:
            # This is a crafted item, recursively calculate its ingredients
            sub_ingredients = calculate_all_ingredients(ingredient, total_amount, memo)
            for sub_ing, sub_amt in sub_ingredients.items():
                result[sub_ing] = result.get(sub_ing, 0) + sub_amt
        else:
            # This is a base resource
            result[ingredient] = result.get(ingredient, 0) + total_amount
    
    return result

# Function to separate base and intermediate ingredients
def separate_ingredients(all_ingredients):
    base_ingredients = {}
    intermediate_materials = {}
    
    for item, amount in all_ingredients.items():
        if item in recipes:
            intermediate_materials[item] = amount
        else:
            base_ingredients[item] = amount
    
    return base_ingredients, intermediate_materials

# Function to load an image with error handling
def load_image(item_name):
    # Convert item name to lowercase and replace spaces with underscores for filename
    filename = item_name.lower().replace(" ", "_").replace("-", "_") + ".png"
    image_path = os.path.join("icons", filename)
    
    try:
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            # Return a placeholder or None
            return None
    except Exception as e:
        st.error(f"Error loading image for {item_name}: {e}")
        return None

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e0e0e0;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4a9eff;
        color: white;
    }
    .item-card {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        cursor: pointer;
    }
    .item-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .item-card.selected {
        border: 2px solid #4a9eff;
        box-shadow: 0 0 8px rgba(74, 158, 255, 0.5);
    }
    .category-button {
        width: 100%;
        margin-bottom: 8px;
    }
    .subcategory-button {
        width: 100%;
        margin-bottom: 4px;
        font-size: 0.9em;
    }
    .result-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .base-ingredient {
        color: #28a745;
        font-weight: 500;
    }
    .intermediate-ingredient {
        color: #ff9800;
        font-weight: 500;
    }
    .machine-info {
        background-color: #e8f4fd;
        border-left: 4px solid #4a9eff;
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 4px 4px 0;
    }
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-text {
        margin-left: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown(
    """
    <div class="header-container">
        <h1>Oddsparks Crafting Calculator</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar for category selection
with col1:
    st.subheader("Select Category")
    
    # Initialize session state for selected category and subcategory
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = list(categories.keys())[0]
    if 'selected_subcategory' not in st.session_state:
        st.session_state.selected_subcategory = categories[st.session_state.selected_category][0]
    if 'selected_item' not in st.session_state:
        st.session_state.selected_item = None
    if 'quantity' not in st.session_state:
        st.session_state.quantity = 1
    
    # Category buttons
    for category in categories:
        if st.button(category, key=f"cat_{category}", 
                    help=f"Show {category} subcategories",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_category == category else "secondary"):
            st.session_state.selected_category = category
            st.session_state.selected_subcategory = categories[category][0]
            st.session_state.selected_item = None
            st.experimental_rerun()
    
    st.subheader("Select Subcategory")
    
    # Subcategory buttons
    for subcategory in categories[st.session_state.selected_category]:
        if st.button(subcategory, key=f"subcat_{subcategory}", 
                    help=f"Show items in {subcategory}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_subcategory == subcategory else "secondary"):
            st.session_state.selected_subcategory = subcategory
            st.session_state.selected_item = None
            st.experimental_rerun()
    
    # Quantity input
    st.subheader("Quantity")
    quantity = st.number_input("How many do you want to craft?", 
                              min_value=1, max_value=1000, value=st.session_state.quantity,
                              help="Enter the number of items you want to craft")
    
    if quantity != st.session_state.quantity:
        st.session_state.quantity = quantity
    
    # Calculate button (only shown when an item is selected)
    if st.session_state.selected_item:
        if st.button("Calculate Ingredients", type="primary", use_container_width=True):
            st.session_state.calculate = True
        
        # Reset button
        if st.button("Reset Selection", type="secondary", use_container_width=True):
            st.session_state.selected_item = None
            st.session_state.calculate = False
            st.experimental_rerun()

# Main content area
with col2:
    if st.session_state.selected_subcategory:
        st.subheader(f"{st.session_state.selected_subcategory}")
        
        # Display items in a grid
        items = subcategories[st.session_state.selected_subcategory]
        cols = 4  # Number of columns in the grid
        
        # Create rows for the grid
        for i in range(0, len(items), cols):
            row_items = items[i:i+cols]
            columns = st.columns(cols)
            
            for j, item in enumerate(row_items):
                with columns[j]:
                    # Load item image if available
                    img = load_image(item)
                    
                    # Create a clickable card for each item
                    card_style = "item-card selected" if st.session_state.selected_item == item else "item-card"
                    
                    # Display item with image if available
                    if img:
                        st.image(img, width=60, caption=item)
                    else:
                        st.markdown(f"<div class='{card_style}'><p>{item}</p></div>", unsafe_allow_html=True)
                    
                    # Button to select the item
                    if st.button("Select", key=f"select_{item}", use_container_width=True,
                                type="primary" if st.session_state.selected_item == item else "secondary"):
                        st.session_state.selected_item = item
                        st.session_state.calculate = False
                        st.experimental_rerun()
    
    # Display calculation results
    if st.session_state.selected_item and hasattr(st.session_state, 'calculate') and st.session_state.calculate:
        st.markdown("---")
        st.subheader(f"Crafting {st.session_state.quantity}x {st.session_state.selected_item}")
        
        # Calculate ingredients
        all_ingredients = calculate_all_ingredients(st.session_state.selected_item, st.session_state.quantity)
        base_ingredients, intermediate_materials = separate_ingredients(all_ingredients)
        
        # Display recipe information
        recipe = recipes[st.session_state.selected_item]
        output_quantity = recipe.get("output", 1)
        
        st.markdown(f"**Recipe Output:** {output_quantity}x {st.session_state.selected_item} per craft")
        
        # Display machine requirements if any
        if st.session_state.selected_item in machine_requirements:
            machine_info = machine_requirements[st.session_state.selected_item]
            st.markdown(
                f"""
                <div class="machine-info">
                    <strong>Required Building:</strong> {machine_info['machine']} - {machine_info['description']}
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Display direct ingredients
        st.markdown("### Direct Ingredients (per craft)")
        direct_ingredients = recipes[st.session_state.selected_item]["ingredients"]
        
        for ingredient, amount in direct_ingredients.items():
            st.markdown(f"- {amount}x **{ingredient}**")
        
        # Display all required ingredients
        st.markdown("---")
        st.markdown("### Total Resources Required")
        
        # Intermediate materials
        if intermediate_materials:
            st.markdown("#### Intermediate Materials")
            for item, amount in sorted(intermediate_materials.items()):
                st.markdown(
                    f"""<span class="intermediate-ingredient">{amount}x {item}</span>""", 
                    unsafe_allow_html=True
                )
        
        # Base ingredients
        st.markdown("#### Base Resources")
        for item, amount in sorted(base_ingredients.items()):
            st.markdown(
                f"""<span class="base-ingredient">{amount}x {item}</span>""", 
                unsafe_allow_html=True
            )
        
        # Summary
        st.markdown("---")
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 8px;">
                <p>Total: {len(base_ingredients)} base resources • {len(intermediate_materials)} intermediate items</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <p>Oddsparks Crafting Calculator - Streamlit Version</p>
    </div>
    """, 
    unsafe_allow_html=True
)
