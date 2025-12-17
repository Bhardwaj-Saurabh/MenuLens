"""
MenuLens Streamlit Testing App
A web interface to test the MenuLens backend API
"""
import streamlit as st
import requests
from PIL import Image
import io
import json

# Configure Streamlit page
st.set_page_config(
    page_title="MenuLens - AI Menu Scanner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Standardize all food images to same size */
    .stImage > img {
        width: 100% !important;
        height: 250px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }

    .food-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .allergen-warning {
        background-color: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .veg-badge {
        background-color: #4caf50;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin: 5px;
    }
    .non-veg-badge {
        background-color: #f44336;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin: 5px;
    }
    .vegan-badge {
        background-color: #8bc34a;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)


def check_backend_health():
    """Check if the backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        return False


def analyze_menu(image_file):
    """Send menu image to backend for analysis"""
    try:
        files = {"file": image_file}
        response = requests.post(
            f"{API_BASE_URL}/api/menu/analyze",
            files=files,
            timeout=180  # 3 minutes for AI analysis + image search
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None


def get_food_type_badge(food_type):
    """Return HTML badge for food type"""
    if food_type and "vegetarian" in food_type.lower():
        return '<span class="veg-badge">🥗 Vegetarian</span>'
    elif food_type and "vegan" in food_type.lower():
        return '<span class="vegan-badge">🌱 Vegan</span>'
    elif food_type and "non-vegetarian" in food_type.lower():
        return '<span class="non-veg-badge">🍖 Non-Vegetarian</span>'
    else:
        return f'<span class="veg-badge">{food_type or "Unknown"}</span>'


def display_menu_item(item, index):
    """Display a single menu item with all details"""
    st.markdown(f"### {index}. {item.get('name', 'Unknown Dish')}")

    # Create two columns for image and details
    col1, col2 = st.columns([1, 2])

    with col1:
        # Display food image
        image_url = item.get('image_url')
        if image_url:
            try:
                st.image(image_url, use_column_width=True, caption=item.get('name'))
            except Exception as e:
                st.info("📷 Image not available")
        else:
            st.info("📷 No image found")

    with col2:
        # Food type badges
        st.markdown(get_food_type_badge(item.get('food_type')), unsafe_allow_html=True)

        # Meat type warning
        meat_type = item.get('meat_type', 'None')
        if meat_type and meat_type != 'None':
            if item.get('contains_pork'):
                st.warning(f"⚠️ Contains Pork ({meat_type})")
            elif item.get('contains_beef'):
                st.warning(f"⚠️ Contains Beef ({meat_type})")
            else:
                st.info(f"🍖 Meat: {meat_type}")

        # Ingredients
        ingredients = item.get('ingredients', [])
        if ingredients:
            st.markdown("**Ingredients:**")
            st.write(", ".join(ingredients))

        # Allergens
        allergens = item.get('allergens', [])
        if allergens:
            st.markdown("**⚠️ Allergen Warnings:**")
            for allergen in allergens:
                st.markdown(f'<div class="allergen-warning">🚨 {allergen}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No common allergens detected")

    st.divider()


def main():
    """Main Streamlit app"""

    # Header
    st.title("🍽️ MenuLens - AI Menu Scanner")
    st.markdown("Upload a restaurant menu image to get instant analysis with food images, ingredients, and allergen warnings!")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Backend health check
        if check_backend_health():
            st.success("✅ Backend API is running")
        else:
            st.error("❌ Backend API is not running")
            st.info("Start the backend with:\n```\ncd backend\nsource venv/bin/activate\nuvicorn app.main:app --reload\n```")
            st.stop()

        st.divider()

        # User preferences (for future implementation)
        st.header("👤 Dietary Preferences")
        st.info("User profile features coming soon!")

        is_vegetarian = st.checkbox("Vegetarian")
        is_vegan = st.checkbox("Vegan")
        avoid_pork = st.checkbox("Avoid Pork")
        avoid_beef = st.checkbox("Avoid Beef")

        st.divider()

        # Allergen preferences
        st.header("🌾 Allergen Alerts")
        selected_allergens = st.multiselect(
            "Select your allergens:",
            ["Dairy", "Eggs", "Nuts", "Peanuts", "Gluten", "Soy", "Shellfish", "Fish", "Sesame"]
        )

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📸 Scan Menu", "📊 Results", "ℹ️ About"])

    with tab1:
        st.header("Upload Menu Image")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a menu image (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload a clear photo of a restaurant menu"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Menu", use_column_width=True)

            # Analyze button
            if st.button("🔍 Analyze Menu", type="primary"):
                with st.spinner("🤖 AI is analyzing your menu and fetching food images... This may take 1-3 minutes..."):
                    # Reset file pointer
                    uploaded_file.seek(0)

                    # Send to backend
                    result = analyze_menu(uploaded_file)

                    if result and result.get('success'):
                        st.session_state['analysis_result'] = result
                        st.success("✅ Analysis complete! Check the Results tab.")
                        st.balloons()
                    else:
                        st.error("❌ Analysis failed. Please try again.")

    with tab2:
        st.header("Analysis Results")

        if 'analysis_result' in st.session_state:
            result = st.session_state['analysis_result']
            analysis = result.get('analysis', {})

            # Display metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                cuisine = analysis.get('cuisine_type', 'Unknown')
                st.metric("Cuisine Type", cuisine)
            with col2:
                language = analysis.get('language', 'Unknown')
                st.metric("Language", language)
            with col3:
                item_count = len(analysis.get('menu_items', []))
                st.metric("Items Found", item_count)

            st.divider()

            # Display menu items
            menu_items = analysis.get('menu_items', [])

            if menu_items:
                st.subheader(f"🍽️ Found {len(menu_items)} Menu Items")

                # Filter based on user preferences
                filtered_items = menu_items
                if is_vegetarian or is_vegan:
                    filtered_items = [
                        item for item in menu_items
                        if 'vegetarian' in item.get('food_type', '').lower() or
                           'vegan' in item.get('food_type', '').lower()
                    ]

                if avoid_pork:
                    filtered_items = [
                        item for item in filtered_items
                        if not item.get('contains_pork', False)
                    ]

                if avoid_beef:
                    filtered_items = [
                        item for item in filtered_items
                        if not item.get('contains_beef', False)
                    ]

                # Show filtering results
                if len(filtered_items) < len(menu_items):
                    st.warning(f"Showing {len(filtered_items)} items based on your preferences (filtered {len(menu_items) - len(filtered_items)} items)")

                # Display each item
                for idx, item in enumerate(filtered_items, 1):
                    display_menu_item(item, idx)

                # Download results
                st.divider()
                json_str = json.dumps(analysis, indent=2)
                st.download_button(
                    label="📥 Download Full Analysis (JSON)",
                    data=json_str,
                    file_name="menu_analysis.json",
                    mime="application/json"
                )
            else:
                st.warning("No menu items found in the analysis.")
        else:
            st.info("👈 Upload and analyze a menu image in the 'Scan Menu' tab to see results here.")

    with tab3:
        st.header("About MenuLens")
        st.markdown("""
        **MenuLens** is an AI-powered menu scanner that helps you make informed dining decisions.

        ### Features:
        - 🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4o Vision to read and understand menus
        - 📸 **Food Images**: Automatically fetches images of dishes using Tavily API
        - 🥗 **Dietary Classification**: Identifies vegetarian, vegan, and non-vegetarian items
        - 🍖 **Religious Considerations**: Clearly marks pork and beef for dietary restrictions
        - 🌾 **Allergen Detection**: Identifies common allergens in food items
        - 🌍 **Multi-Language Support**: Analyzes menus in different languages

        ### Technology Stack:
        - **Backend**: FastAPI (Python)
        - **AI**: OpenAI GPT-4o with Vision
        - **Image Search**: Tavily API
        - **Frontend**: Streamlit (Testing), React Native (Mobile App)

        ### How to Use:
        1. Upload a clear photo of a restaurant menu
        2. Click "Analyze Menu" and wait for AI processing
        3. View detailed analysis with images, ingredients, and allergens
        4. Filter results based on your dietary preferences

        ### Note:
        This is a testing interface. The full mobile app is under development.
        """)

        st.divider()

        st.markdown("### API Status")
        if check_backend_health():
            st.success("Backend API: Running ✅")
            st.code(f"API URL: {API_BASE_URL}")
        else:
            st.error("Backend API: Not Running ❌")


if __name__ == "__main__":
    main()
