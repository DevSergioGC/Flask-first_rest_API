from db import db

class JWTRevokedModel(db.Model):
    __tablename__ = "jwt_revoked"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(80), unique=True, nullable=False)