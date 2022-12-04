# -*- coding: utf-8 -*-
# from odoo import http


# class Tienda(http.Controller):
#     @http.route('/tienda/tienda', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tienda/tienda/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tienda.listing', {
#             'root': '/tienda/tienda',
#             'objects': http.request.env['tienda.tienda'].search([]),
#         })

#     @http.route('/tienda/tienda/objects/<model("tienda.tienda"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tienda.object', {
#             'object': obj
#         })
