from datetime import datetime
from extensions import db

# ── Donor (User) ─────────────────────────────────────────────────────────────
class Donor(db.Model):
    __tablename__ = "donors"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)   # bcrypt hash
    is_active     = db.Column(db.Boolean, default=True)
    is_admin      = db.Column(db.Boolean, default=False)
    login_attempts= db.Column(db.Integer, default=0)
    locked_until  = db.Column(db.DateTime, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    donations     = db.relationship("Donation", backref="donor", lazy=True)

    def __repr__(self):
        return f"<Donor {self.email}>"


# ── Donation Transaction ──────────────────────────────────────────────────────
class Donation(db.Model):
    __tablename__ = "donations"

    id                   = db.Column(db.Integer, primary_key=True)
    donor_id             = db.Column(db.Integer, db.ForeignKey("donors.id"), nullable=False)

    # Stored AES-encrypted as hex strings
    encrypted_amount     = db.Column(db.Text, nullable=False)
    encrypted_cause      = db.Column(db.Text, nullable=False)
    encrypted_card_last4 = db.Column(db.Text, nullable=True)

    # SHA-256 integrity hash of the raw transaction data
    integrity_hash       = db.Column(db.String(64), nullable=False)

    status               = db.Column(db.String(20), default="pending")  # pending / approved / flagged
    donor_ip             = db.Column(db.String(45), nullable=True)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    fraud_flag           = db.relationship("FraudFlag", backref="donation", uselist=False)
    receipt              = db.relationship("Receipt",   backref="donation", uselist=False)

    def __repr__(self):
        return f"<Donation {self.id} status={self.status}>"


# ── Fraud Flag ────────────────────────────────────────────────────────────────
class FraudFlag(db.Model):
    __tablename__ = "fraud_flags"

    id          = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey("donations.id"), nullable=False)
    reason      = db.Column(db.String(255), nullable=False)
    flagged_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FraudFlag donation={self.donation_id} reason={self.reason}>"


# ── Donation Receipt ──────────────────────────────────────────────────────────
class Receipt(db.Model):
    __tablename__ = "receipts"

    id               = db.Column(db.Integer, primary_key=True)
    donation_id      = db.Column(db.Integer, db.ForeignKey("donations.id"), nullable=False)
    encrypted_receipt= db.Column(db.Text, nullable=False)   # AES-encrypted PDF bytes (hex)
    receipt_hash     = db.Column(db.String(64), nullable=False)  # SHA-256 of receipt
    generated_at     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Receipt donation={self.donation_id}>"


# ── Audit Log ─────────────────────────────────────────────────────────────────
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id         = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)   # LOGIN / DONATION / FRAUD / RECEIPT
    user_id    = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    details    = db.Column(db.Text, nullable=True)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.event_type} user={self.user_id}>"
