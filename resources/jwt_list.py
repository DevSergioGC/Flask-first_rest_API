from flask.views import MethodView
from flask_smorest import Blueprint
from models import JWTRevokedModel
from schemas import RevokedJWTSchema

blp = Blueprint("JWT", "revoked_jwt", description="List of all revoked JWT's")

@blp.route("/jwt")
class RevokedJWT(MethodView):
    @blp.response(200, RevokedJWTSchema(many=True))
    def get(self):
        return JWTRevokedModel.query.all()