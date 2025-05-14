from odoo import http
from odoo.http import request
import json
from odoo.tools import config


class JWTController(http.Controller):

    # Future improvement --> implement refreshToken
    @http.route('/api/auth/login', type='json', auth='none', methods=['POST'], csrf=False)
    def auth_login(self, **post):
        params = json.loads(request.httprequest.data)
        user_name = params.get('user_name')
        password = params.get('password')

        if not user_name or not password:
            return {'error': 'Missing credentials'}

        uid = request.session.authenticate(request.db, user_name, password)
        if not uid:
            return {'error': 'Invalid credentials'}

        user = request.env['res.users'].browse(uid)
        token = request.env['jwt.auth'].generate_token(uid, user.company_id.id)

        return {
            'uid': uid,
            'token': token,
            'expires_in': 60 * int(config.get("jwt_duration_in_minutes"))
        }
