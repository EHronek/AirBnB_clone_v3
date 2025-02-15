#!/usr/bin/python3
"""Iniatializes a blueprint instance and loads all routes from index"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
