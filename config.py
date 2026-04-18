import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Core Flask ──────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///donation_platform.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── JWT ─────────────────────────────────────────
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))
    )

    # ── AES key (must be 32 bytes for AES-256) ──────
    AES_SECRET_KEY = os.getenv("AES_SECRET_KEY", "12345678901234567890123456789012").encode()

    # ── Fraud Detection ─────────────────────────────
    FRAUD_MAX_AMOUNT = int(os.getenv("FRAUD_MAX_AMOUNT", 50000))
    FRAUD_MAX_ATTEMPTS_PER_IP = int(os.getenv("FRAUD_MAX_ATTEMPTS_PER_IP", 5))
    FRAUD_WINDOW_MINUTES = int(os.getenv("FRAUD_WINDOW_MINUTES", 10))

    # ── Bcrypt ──────────────────────────────────────
    BCRYPT_LOG_ROUNDS = 12          # Higher = slower = more secure
    MAX_LOGIN_ATTEMPTS = 5          # Brute-force lockout threshold
    LOCKOUT_MINUTES = 15
