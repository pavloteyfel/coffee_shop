from auth import AuthError



def a():
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Authorization malformed.'
    }, 401)



try:
    a()
except Exception as e:
    if isinstance(e, AuthError) and e.status_code == 401:
        print('gotcha')