#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:17
# @Author : ZhangXiaobo
# @Software: PyCharm

"""
捕捉所有的错误，并将错误信息，渲染到前端页面
"""

from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    """
    403错误
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """
    404错误
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """
    500错误
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
