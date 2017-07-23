from flask import request, jsonify, session
from flask.views import MethodView

from opplett.pluggable_views.user_auth import login_required


class UserProfileAPI(MethodView):

    methods = ['GET', 'POST']
    decorators = [login_required]

    def get(self):
        return jsonify({'user_validated': True,
                        'credentials': session['credentials']
                        })
