@echo off
echo Setting up Secure Donation Platform...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo.
echo Setup complete! Run with: python app.py
