from datetime import datetime, timedelta
from odoo import models, api, exceptions
from odoo.http import request
from odoo import fields
from werkzeug.exceptions import BadRequest


class SaleOrder(models.Model):
    _name = 'custom_sale_order'
    _description = 'Custom Sale Order Model'

    @api.model
    def create_sale_order(self, data, user_id, company_id):

        '''
             --> Assuming that Customer Ref is Mandatory in request data So no need for whole customer
             --> There is another Option to Receive the Customer object in the data and check if the customer exist
                Use its id and If not we can Create a new Customer
        '''

        sale_order_lines = data.get('order_lines', [])
        customer_reference = data.get('reference')
        if not customer_reference or not sale_order_lines:
            raise BadRequest('No customer or sale order lines received')

        partner = request.env['res.partner'].sudo().search([('ref', '=', customer_reference)], limit=1)
        if not partner:
            raise BadRequest('Customer not found')

        sale_order_vals = {
            'user_id': user_id,
            'partner_id': partner.id,
            'company_id': company_id,
            'order_line': [],
            'client_order_ref': customer_reference,
            'date_order': datetime.now()
        }
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': []
        }

        for line in sale_order_lines:
            product = request.env['product.product'].sudo().search([('id', '=', line['product_id'])], limit=1)
            if not product:
                raise BadRequest('Product not found')

            order_line_vals = (0, 0, {
                'product_id': product.id,
                'product_uom_qty': line['quantity'],
                'price_unit': line['price'],
            })
            invoice_line_vals = (0, 0, {
                'product_id': product.id,
                'quantity': line['quantity'],
                'price_unit': line['price'],
                'name': product.name,
            })

            sale_order_vals['order_line'].append(order_line_vals)
            invoice_vals['invoice_line_ids'].append(invoice_line_vals)

        order = request.env['sale.order'].sudo().create(sale_order_vals)
        invoice = request.env['account.move'].sudo().create(invoice_vals)

        return {
            'success': True,
            'sale_order_id': order.id,
            'sale_order_name': order.name,
            'sale_order_state': order.state,
            'total_amount': order.amount_total,
            'invoice_id': invoice.id if invoice else None,
            'invoice_state': invoice.state if invoice else None,
        }