import json
from odoo import http
from odoo.http import request
from werkzeug.exceptions import BadRequest

class SaleOrderAPI(http.Controller):

    @http.route('/api/create_sale_order', type='json', auth='public', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get("Authorization")
            if not auth_header:
                return BadRequest("Unauthorized")

            token_payload = request.env['jwt.auth'].decode_token(auth_header)
            user_id = int(token_payload['sub'])
            company_id = token_payload['company_id']

            data = json.loads(request.httprequest.data)
            if not data:
                return BadRequest('No data received')

            return request.env['custom_sale_order'].create_sale_order(data, user_id, company_id)
        except Exception as e:
            return BadRequest(str(e))
