import jwt
from datetime import datetime, timedelta
from odoo import models, api, exceptions
from odoo.tools import config

class JwtAuth(models.Model):
    _name = 'jwt.auth'
    _description = 'JWT Authentication Configuration'

    @api.model
    def generate_token(self, user_id, company_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=int(config.get("jwt_duration_in_minutes"))),
            'iat': datetime.utcnow(),
            'sub': str(user_id),
            'company_id':company_id,
            'iss': config.get("jwt_issuer")
        }
        return jwt.encode(payload, config.get("jwt_secret"), algorithm='HS256')

    @api.model
    def decode_token(self, token):
        try:
            token = token.split(' ')[1].strip()
            if not token:
                raise jwt.InvalidTokenError
            payload = jwt.decode(token, config.get("jwt_secret"), algorithms=['HS256'], issuer=config.get("jwt_issuer"))
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.ValidationError('Token expired')
        except jwt.InvalidTokenError as e:
            raise exceptions.ValidationError(f'Invalid token: {str(e)}')
