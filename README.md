# MenuLens - AI Menu Scanner App

MenuLens is an AI-powered mobile application that scans restaurant menus to provide instant images of each food item, ingredient breakdowns, allergen warnings, and dietary information (vegetarian/non-vegetarian/vegan, specific meat types for religious considerations).

## Architecture

- **Backend**: Python (FastAPI) - Handles image upload, AI analysis, allergen database
- **Frontend**: React Native - Mobile app with camera integration
- **AI**: Anthropic Claude 3.5 Sonnet or OpenAI GPT-4o Vision
- **Database**: PostgreSQL

## Features

- 📸 Scan restaurant menus with your camera
- 🤖 AI-powered menu item extraction
- 🥗 Food type classification (Veg/Non-Veg/Vegan)
- 🍖 Specific meat type identification (Pork/Beef warnings for religious beliefs)
- 🌾 Allergen detection and warnings
- 👤 User profiles with dietary preferences
- 📱 iOS-first development (Mac-optimized)

## Project Structure

```
MenuLens/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── core/           # Core services (AI, config, security)
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/            # API routes
│   │   └── db/             # Database connection
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── mobile/                 # React Native app (to be created)
└── claude.md              # Development plan
```

## Setup Instructions (macOS)

### Prerequisites

1. **Homebrew** (macOS package manager)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Python 3.11+**
   ```bash
   brew install python@3.11
   ```

3. **PostgreSQL**
   ```bash
   brew install postgresql@15
   brew services start postgresql@15
   ```

4. **Node.js & Watchman** (for React Native)
   ```bash
   brew install node watchman
   ```

5. **Xcode** (for iOS development)
   - Install from App Store
   - Install Xcode Command Line Tools:
     ```bash
     xcode-select --install
     ```

6. **CocoaPods**
   ```bash
   sudo gem install cocoapods
   ```

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - ANTHROPIC_API_KEY or OPENAI_API_KEY
   # - DATABASE_URL
   # - Other configuration
   ```

5. **Create database**
   ```bash
   # Connect to PostgreSQL
   psql postgres

   # In PostgreSQL prompt:
   CREATE DATABASE menulens;
   \q
   ```

6. **Run the backend server**
   ```bash
   # Make sure virtual environment is activated
   python -m uvicorn app.main:app --reload
   ```

   The API will be available at: `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Mobile App Setup (Coming Soon)

React Native mobile app will be initialized in the `mobile/` directory.

```bash
# Create React Native app
npx react-native init MenuLensApp
# Or with Expo (easier for beginners):
npx create-expo-app MenuLensApp
```

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health information

### Menu Analysis
- `POST /api/menu/upload` - Upload menu image
- `POST /api/menu/analyze` - Upload and analyze menu in one step
- `GET /api/menu/items/{filename}` - Get previous analysis
- `DELETE /api/menu/items/{filename}` - Delete uploaded image

### User Profile (To be implemented)
- `POST /api/user/profile` - Create user profile
- `GET /api/user/profile/{user_id}` - Get user profile
- `PUT /api/user/profile/{user_id}` - Update user profile

### Allergens
- `GET /api/allergens` - Get list of common allergens

## Testing the API

1. **Test health endpoint**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test menu analysis** (requires a menu image)
   ```bash
   curl -X POST "http://localhost:8000/api/menu/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/menu-image.jpg"
   ```

3. **Interactive API documentation**
   - Open browser: `http://localhost:8000/docs`
   - Use Swagger UI to test all endpoints

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# AI Provider (choose 'anthropic' or 'openai')
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://localhost:5432/menulens

# Upload settings
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760

# Security
SECRET_KEY=change-this-to-random-string
```

## Development Workflow

1. **Start PostgreSQL**
   ```bash
   brew services start postgresql@15
   ```

2. **Activate virtual environment**
   ```bash
   cd backend
   source venv/bin/activate
   ```

3. **Run backend with auto-reload**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run tests** (when implemented)
   ```bash
   pytest
   ```

## Next Steps

See [claude.md](claude.md) for the complete development plan.

### Immediate TODO:
- [ ] Set up AI API keys (Anthropic or OpenAI)
- [ ] Configure database
- [ ] Test menu analysis with sample images
- [ ] Implement image search service (Unsplash/Google)
- [ ] Create React Native mobile app
- [ ] Implement user authentication
- [ ] Build allergen database

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- Anthropic/OpenAI SDK - AI vision analysis
- Pillow - Image processing
- PostgreSQL - Database

**Mobile (Coming Soon):**
- React Native - Cross-platform mobile framework
- Expo Camera - Camera integration
- Axios - HTTP client
- React Navigation - App navigation

## Contributing

This is a personal project. Refer to the development plan in [claude.md](claude.md) for implementation phases.

## License

MIT License

## Getting Help

- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Check the [Anthropic documentation](https://docs.anthropic.com/)
- Check the [React Native documentation](https://reactnative.dev/)
- Review the development plan in [claude.md](claude.md)
