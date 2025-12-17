# MenuLens Streamlit Testing Guide

This guide will help you test the MenuLens backend using the Streamlit web interface.

## Quick Start

### Option 1: Using Shell Scripts (Easiest)

1. **Start the Backend API** (in Terminal 1):
   ```bash
   ./run_backend.sh
   ```

2. **Start the Streamlit App** (in Terminal 2):
   ```bash
   ./run_streamlit.sh
   ```

### Option 2: Manual Setup

1. **Install Dependencies**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start Backend API** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   ```

3. **Start Streamlit** (Terminal 2):
   ```bash
   source backend/venv/bin/activate
   streamlit run streamlit_app.py
   ```

## Using the Streamlit App

1. **Open your browser** - Streamlit will automatically open at `http://localhost:8501`

2. **Check Backend Status** - The sidebar will show if the backend is running

3. **Upload a Menu Image**:
   - Go to the "📸 Scan Menu" tab
   - Click "Browse files" and select a menu image (JPG, PNG, WEBP)
   - Click "🔍 Analyze Menu"

4. **View Results**:
   - Switch to the "📊 Results" tab
   - See all detected menu items with:
     - Food images (from Tavily)
     - Vegetarian/Non-Veg/Vegan classification
     - Meat type warnings (Pork/Beef)
     - Ingredients list
     - Allergen warnings

5. **Set Dietary Preferences** (Sidebar):
   - Check "Vegetarian" to filter non-veg items
   - Check "Avoid Pork" or "Avoid Beef"
   - Results will automatically filter

## Features

### ✨ Main Features
- 📸 **Image Upload** - Drag & drop or browse for menu images
- 🤖 **AI Analysis** - Real-time processing with OpenAI GPT-4o
- 🖼️ **Food Images** - Automatic image search with Tavily
- 🥗 **Dietary Info** - Veg/Non-Veg/Vegan badges
- ⚠️ **Allergen Warnings** - Highlighted allergen alerts
- 🍖 **Religious Restrictions** - Clear pork/beef warnings
- 🌍 **Multi-Language** - Detects menu language
- 📥 **Export Results** - Download JSON analysis

### 🎨 Interface Features
- **Three Tabs**:
  1. 📸 Scan Menu - Upload and analyze
  2. 📊 Results - Detailed view of all items
  3. ℹ️ About - App information

- **Sidebar Settings**:
  - Backend health check
  - Dietary preferences
  - Allergen selections

## Troubleshooting

### Backend Not Running
If you see "❌ Backend API is not running":

1. Open a new terminal
2. Run:
   ```bash
   ./run_backend.sh
   ```
3. Wait for "Application startup complete"
4. Refresh Streamlit page

### Dependencies Not Installed
If you see import errors:

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Streamlit Port Conflict
If port 8501 is in use:

```bash
streamlit run streamlit_app.py --server.port 8502
```

### API Keys Not Working
Check your `.env` file has valid keys:

```bash
cat backend/.env
```

Make sure these are set:
- `OPENAI_API_KEY` - Your OpenAI API key
- `TAVILY_API_KEY` - Your Tavily API key

## Example Workflow

1. **Start both servers**:
   ```bash
   # Terminal 1
   ./run_backend.sh

   # Terminal 2
   ./run_streamlit.sh
   ```

2. **Upload a test menu** (use any restaurant menu photo)

3. **Wait for analysis** (10-30 seconds depending on menu size)

4. **Explore results**:
   - View food images
   - Check ingredients
   - See allergen warnings
   - Filter by dietary preferences

5. **Download results** as JSON for further use

## API Endpoints Used

The Streamlit app uses these backend endpoints:

- `GET /health` - Check backend status
- `POST /api/menu/analyze` - Upload and analyze menu
- `GET /api/allergens` - Get allergen list

## Screenshots

### Scan Menu Tab
- Clean interface to upload menu images
- Real-time processing with spinner
- Success/error notifications

### Results Tab
- Beautiful card-based layout
- Food images with captions
- Color-coded badges (Green=Veg, Red=Non-Veg)
- Allergen warnings in red boxes
- Expandable ingredient lists

### Sidebar
- Live backend health check
- Dietary preference toggles
- Allergen multi-select

## Development

To customize the Streamlit app, edit `streamlit_app.py`:

```python
# Change API URL
API_BASE_URL = "http://localhost:8000"

# Customize styling
st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
""", unsafe_allow_html=True)
```

## Next Steps

After testing with Streamlit:

1. **Build the React Native mobile app** - Follow the main development plan
2. **Add user authentication** - Implement JWT auth
3. **Connect to database** - Store menu scan history
4. **Deploy backend** - Deploy to Heroku/Railway/AWS
5. **Add more features** - Restaurant search, saved preferences, etc.

## Support

For issues:
1. Check [README.md](README.md) for setup instructions
2. Review [claude.md](claude.md) for development plan
3. Check backend logs in Terminal 1
4. Check Streamlit logs in Terminal 2

---

**Happy Testing! 🍽️**
