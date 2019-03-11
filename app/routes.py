"""
    Define as rotas da aplicação
"""

from app import APP, manager

@APP.route('/<int:code>:<string:start>&<string:end>')
def endpoint(code, start, end):
    """
        Fallback
    """
    return manager.transaction(code, start, end)
