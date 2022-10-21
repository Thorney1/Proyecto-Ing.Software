from functools import wraps
from flask import Response, request, session, render_template, redirect, url_for


def validar_sesion(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        #validar sesion si existe
        
        if 'user_id' in session:
            return func(*args, **kwargs)

        #return Response('No autenticado', mimetype='text/plain', status=401)
        return redirect(url_for('login'))
    return decorated_function