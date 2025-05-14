# Odoo Sale Order RestfulAPI with JWT Authentication

This module provides an API endpoint for creating Sale Orders and Invoices in Odoo 

## Features
- Recieve order data in json
- Create Sale Orders and Invoices(draft state) via API
- JWT token based authentication
- Ensure only authorized users can call the API
- search for customer with unique ref
- Returns created order and invoice details

## Prerequisites
- Odoo 17
- PyJWT library (pip install PyJWT)

## Installation
1. Place the module directory in your Odoo addons path in odoo.conf file
2. add theser params in config file (jwt_secret = 63f4945d921d599f27ae4fdf5bada3f1
jwt_duration_in_minutes = 20
jwt_issuer = cartona)
3. Install via Odoo Apps:
   - Enable Developer Mode
   - Go to Apps > Update Apps List
   - Search for "custom_api_sale_invoice" and install
     
### Endpoint
POST /api/auth/login
POST /api/create_sale_order

### Request Body Example

{  
  "reference": "ref_3",
  "order_lines": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 120.0
    },
    {
      "product_id": 5,
      "quantity": 1,
      "price": 200.0
    }
  ]
}

### Response
{
    "jsonrpc": "2.0",
    "id": null,
    "result": {
        "success": true,
        "sale_order_id": 19,
        "sale_order_name": "S00023",
        "sale_order_state": "draft",
        "total_amount": 501.6,
        "invoice_id": 6,
        "invoice_state": "draft"
    }
}
