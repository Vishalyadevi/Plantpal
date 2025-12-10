#!/bin/bash

echo "🌿 PlantPal Setup Script"
echo "========================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "🤖 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)"

# Create instance folder
echo "📁 Creating instance folder..."
mkdir -p instance

# Initialize database
echo "🗄️  Initializing database..."
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
print("✅ Database initialized successfully!")
EOF

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate  (macOS/Linux)"
echo "     venv\\Scripts\\activate     (Windows)"
echo "  2. Run the app:"
echo "     python app.py"
echo "  3. Open browser:"
echo "     http://127.0.0.1:5000"
echo ""
echo "Happy planting! 🌱"