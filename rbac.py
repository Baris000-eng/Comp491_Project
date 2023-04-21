from typing import List
import functools

from constants import ROLES
from flask import session, request


def allow_roles(allowed_roles: List[str], current_session: session, current_request: request):
    """
    Checks if the user has the necessary role to access the endpoint based on following rules:
    1. If current session does not include a role, return 401 Unauthorized.
    2. If role is admin, allow access.
    3. Otherwise, if current session does not match role from path variable or allowed roles, return 403 Forbidden.
    4. Otherwise, allow access.

    :param allowed_roles: List of roles that are allowed to access, e.g. ['student', 'teacher']
    :param current_session: The session dictionary
    """
    DEBUG = False

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            path_variables = current_request.view_args

            if DEBUG:
                print("IN DECORATOR")
                print(f'Path variables: {path_variables}')
                print(f"path_variables.get('role') = {path_variables.get('role')}")
                print(f"current_session.get('role'): {current_session.get('role')}")
                print(f'current_session: {current_session}')
                print(f'current_request: {current_request}')                


            if current_session.get('role') is None:
                return '', 401 # Not logged in

            if current_session.get('role') == "admin":
                result = func(*args, **kwargs)
                return result

            if path_variables.get('role') is None:
                if not (current_session.get('role') in allowed_roles):
                    return '', 403 # No permission
                else:
                    result = func(*args, **kwargs)
                    return result
            
            if path_variables.get('role') == current_session.get('role') and path_variables.get('role') in allowed_roles:
                    result = func(*args, **kwargs)
                    return result

            return '', 403 # No permission

        return wrapper
    return decorator
