from flask import Blueprint, abort
from flask.views import MethodView

from webargs import ValidationError
from webargs.flaskparser import use_args


def use_args_json(schema_cls, only=None, schema_kwargs=None, **kwargs):
    """Produces webargs 'use_args' decorator for json location
    using Marshmallow schema class and json input keys

    Args:
        schema_cls (marshmallow.Schema): Definition for schema to accept
        schema_kwargs (dict, optional): kwargs to pass to schema class init. Defaults to None.

    Returns:
        function: use_args from webargs.flaskparser
    """
    schema_kwargs = schema_kwargs or {}
    only = only or None

    def factory(request):
        # print(only, type(only))
        # only = only or request.get_json().keys()

        return schema_cls(only=only, partial=True, context={"request": request}, **schema_kwargs)

    return use_args(factory, location='json', **kwargs)


def register_api(blueprint: Blueprint, view: MethodView,
                 endpoint: str, url: str, pk='id', pk_type='int'):
    """Registers a methodview to a blueprint at given url prefix

    Provides GET route without an id (pk) and GET with an id in route
    Provides POST route with no id in route
    Provides PUT and DELETE routes with id in route

    Args:
        blueprint (Blueprint): [description]
        view (MethodView): [description]
        endpoint (str): [description]
        url (str): [description]
        pk (str, optional): [description]. Defaults to 'id'.
        pk_type (str, optional): [description]. Defaults to 'int'.
    """
    view_func = view.as_view(endpoint)
    blueprint.add_url_rule(
        url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    blueprint.add_url_rule(url, view_func=view_func, methods=['POST'])
    blueprint.add_url_rule(f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=[
                           'GET', 'PUT', 'DELETE'])
