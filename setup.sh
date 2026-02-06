#!/bin/bash
# Finlytics Setup Script

echo "=========================================="
echo "  Finlytics Trading System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file - you can edit it to customize settings"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p logs data

echo ""
echo "=========================================="
echo "  Setup Complete! ✅"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run demo: python demo.py"
echo "3. Run tests: pytest tests/"
echo "4. Run full system: python -m src.main"
echo ""
echo "Documentation:"
echo "- Quick Start: QUICKSTART.md"
echo "- Full Guide: README.md"
echo "- Architecture: ARCHITECTURE.md"
echo ""
echo "Happy Trading! 🚀"
