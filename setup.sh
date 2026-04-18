#!/bin/bash
echo "Setting up Secure Donation Platform..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo ""
echo "Setup complete! Run with: python app.py"
