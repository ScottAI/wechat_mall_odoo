# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from .error_code import error_code

import logging

_logger = logging.getLogger(__name__)

class TestTest(http.Controller):
    @http.route('/<string:sub_domain>/test',type='json',auth='public',methods=['GET'])
    def get(self, sub_domain, key=None):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                print("没有找到user")
                return request.make_response(json.dumps({'code': 405, 'msg': error_code[405]}))

            if not key:
                print("没有key")
                return request.make_response(json.dumps({'code': 300, 'msg': error_code[300].format('key')}))

            config = request.env['wechat_mall.config.settings']
            value_obj = config.get_config(key, uid=user.id, obj=True)
            if not value_obj:
                print("没有找到value_obj")
                return request.make_response(json.dumps({'code': 406, 'msg': error_code[406]}))

            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'data': {
                        'creatAt': value_obj.create_date,
                        'dateType': 0,
                        'id': value_obj.id,
                        'key': key,
                        'remark': '',
                        'updateAt': value_obj.write_date,
                        'userId': user.id,
                        'value': config.get_config(key, uid=user.id)
                    },
                    'msg': 'success'
                })
            )
            return response
        except AttributeError:
            return request.make_response(json.dumps({'code': 407, 'msg': error_code[407]}))

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))


