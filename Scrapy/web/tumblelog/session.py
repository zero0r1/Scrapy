from flask import session
from functools import wraps
from flask import redirect

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if session.get('token_user') == ''.strip():
            return redirect('login')
        return f(*args, **kwds)
    return wrapper

@requires_auth
def example():
    """Docstring"""
    print('Called example function')