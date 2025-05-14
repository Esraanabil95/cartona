import odoo
from odoo.tests import TransactionCase, tagged
from werkzeug.exceptions import BadRequest
from unittest.mock import patch
import pdb


@tagged('standard', 'at_install')
class TestCustomSaleOrder(TransactionCase):
    def setUp(self):
        super(TestCustomSaleOrder, self).setUp()
        # Mock the request environment
        self.patcher = patch('odoo.http.request')
        self.mock_request = self.patcher.start()
        self.mock_request.env = self.env

        # Create test data
        self.sale_order_model = self.env['custom_sale_order']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'ref': 'TEST123'
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'list_price': 100.0
        })
        self.user_id = self.env.user.id
        self.company_id = self.env.company.id

    def tearDown(self):
        self.patcher.stop()
        super(TestCustomSaleOrder, self).tearDown()

    def test_create_sale_order_success(self):
        pdb.set_trace()
        """Test successful creation of a sale order with invoice"""
        data = {
            'reference': 'TEST123',
            'order_lines': [
                {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price': 100.0
                }
            ]
        }

        result = self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)

        # Verify result structure
        self.assertTrue(result['success'])
        self.assertTrue(result['sale_order_id'])
        self.assertTrue(result['sale_order_name'])
        self.assertEqual(result['sale_order_state'], 'draft')
        self.assertEqual(result['total_amount'], 200.0)
        self.assertTrue(result['invoice_id'])
        self.assertEqual(result['invoice_state'], 'draft')

        # Verify sale order was created correctly
        sale_order = self.env['sale.order'].browse(result['sale_order_id'])
        self.assertEqual(sale_order.partner_id, self.partner)
        self.assertEqual(sale_order.client_order_ref, 'TEST123')
        self.assertEqual(len(sale_order.order_line), 1)
        self.assertEqual(sale_order.order_line[0].product_id, self.product)
        self.assertEqual(sale_order.order_line[0].product_uom_qty, 2)
        self.assertEqual(sale_order.order_line[0].price_unit, 100.0)

        # Verify invoice was created correctly
        invoice = self.env['account.move'].browse(result['invoice_id'])
        self.assertEqual(invoice.partner_id, self.partner)
        self.assertEqual(invoice.move_type, 'out_invoice')
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(invoice.invoice_line_ids[0].product_id, self.product)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 2)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 100.0)

    def test_create_sale_order_multiple_lines(self):
        """Test creating a sale order with multiple order lines"""
        product2 = self.env['product.product'].create({
            'name': 'Second Product',
            'type': 'product',
            'list_price': 50.0
        })

        data = {
            'reference': 'TEST123',
            'order_lines': [
                {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price': 100.0
                },
                {
                    'product_id': product2.id,
                    'quantity': 3,
                    'price': 50.0
                }
            ]
        }

        result = self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)

        self.assertTrue(result['success'])
        self.assertEqual(result['total_amount'], 350.0)  # 2*100 + 3*50

        sale_order = self.env['sale.order'].browse(result['sale_order_id'])
        self.assertEqual(len(sale_order.order_line), 2)

        invoice = self.env['account.move'].browse(result['invoice_id'])
        self.assertEqual(len(invoice.invoice_line_ids), 2)

    def test_create_sale_order_missing_customer(self):
        """Test error when customer reference is missing"""
        data = {
            'reference': '',  # Empty reference
            'order_lines': [
                {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price': 100.0
                }
            ]
        }

        with self.assertRaises(BadRequest):
            self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)

    def test_create_sale_order_customer_not_found(self):
        """Test error when customer is not found"""
        data = {
            'reference': 'NONEXISTENT',
            'order_lines': [
                {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price': 100.0
                }
            ]
        }

        with self.assertRaises(BadRequest):
            self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)

    def test_create_sale_order_no_lines(self):
        """Test error when no order lines are provided"""
        data = {
            'reference': 'TEST123',
            'order_lines': []
        }

        with self.assertRaises(BadRequest):
            self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)

    def test_create_sale_order_product_not_found(self):
        """Test error when product is not found"""
        data = {
            'reference': 'TEST123',
            'order_lines': [
                {
                    'product_id': 999999,  # Non-existent product ID
                    'quantity': 1,
                    'price': 100.0
                }
            ]
        }

        with self.assertRaises(BadRequest):
            self.env['custom_sale_order'].create_sale_order(data, self.user_id, self.company_id)
