from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256 as hasher
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
import datetime

from db import db
from blocklist import BLOCKLIST
from models import UserModel, JWTRevokedModel

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with thtat username already exists")
        
        user = UserModel(
            username = user_data["username"], 
            password = hasher.hash(user_data["password"])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if user and hasher.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=datetime.timedelta(minutes=30))
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid username or password")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = JWTRevokedModel(jti = get_jwt()["jti"])
        db.session.add(jti)
        db.session.commit()
        
        return {"access_token": new_token}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User deleted."}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = JWTRevokedModel(jti= get_jwt()["jti"])
        db.session.add(jti)
        db.session.commit()
        # BLOCKLIST.add(jti)        
        return {"message": "User logged out."}