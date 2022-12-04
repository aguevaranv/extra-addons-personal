# -*- coding: utf-8 -*-
# from odoo import http


# class Estudiantil(http.Controller):
#     @http.route('/estudiantil/estudiantil', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estudiantil/estudiantil/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estudiantil.listing', {
#             'root': '/estudiantil/estudiantil',
#             'objects': http.request.env['estudiantil.estudiantil'].search([]),
#         })

#     @http.route('/estudiantil/estudiantil/objects/<model("estudiantil.estudiantil"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estudiantil.object', {
#             'object': obj
#         })
