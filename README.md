# Oddsparks Crafting Calculator

A Streamlit web application for calculating crafting recipes in Oddsparks. This application helps players determine the resources needed to craft items in the game.

## Features

- Browse items by categories and subcategories
- Visual item selection with icons
- Calculate exact resource requirements for any quantity of items
- View intermediate materials and base resources needed
- See machine/building requirements for crafting

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/oddsparks-crafting-calculator.git
cd oddsparks-crafting-calculator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### How to Use

1. Select a category from the left sidebar
2. Choose a subcategory to view available items
3. Click on an item you want to craft
4. Enter the desired quantity
5. Click "Calculate Ingredients" to see the required resources

## Deployment

This application can be deployed to Streamlit Cloud for free:

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app

## Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `icons/` - Directory containing item icons

## Credits

This is a Streamlit web version of the original Oddsparks Crafting Calculator desktop application.

## License

MIT
