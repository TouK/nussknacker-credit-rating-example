import marshmallow as ma
from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
import random

import json

class ChecklistResult:
    def __init__(self, is_present):
        self.is_present = is_present

class ErrorResponse:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=None)

app = Flask(__name__, static_folder = '/static')

@app.route('/swagger')
def root():
    return app.send_static_file('swagger.json')

app.config['API_TITLE'] = 'ScoringServices'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
api = Api(app)

class ChecklistResultSchema(ma.Schema):
    is_present = ma.fields.Bool()

class ErrorResponseSchema(ma.Schema):
    code = ma.fields.String()
    message = ma.fields.String()

list_blp = Blueprint('checklist', 'checklist', url_prefix='/checklist')
@list_blp.route('/<any(allowlist, blocklist):list_type>/<document_id>')
class CheckList(MethodView):

    @list_blp.response(200, ChecklistResultSchema)
    @list_blp.alt_response(404, schema=ErrorResponseSchema)
    @list_blp.alt_response(500, schema=ErrorResponseSchema)
    @list_blp.doc(operationId='isOnList')
    def get(self, list_type, document_id):
        if list_type == "allowlist" and document_id == "1002":
            return ChecklistResult(True)
        elif list_type == "blocklist" and document_id == "1005":
            return ChecklistResult(True)
        else:
            return ChecklistResult(False)

class ScoringRequestSchema(ma.Schema):
    doc_id = ma.fields.String()
    name = ma.fields.String()
    sur_name = ma.fields.String()

class ScoringResponseSchema(ma.Schema):
    scoring = ma.fields.Int(dump_only=True)

class Scoring:
    def __init__(self, scoring):
        self.scoring = scoring

accis_blp = Blueprint('accis', 'accis', url_prefix='/accis')
@accis_blp.route('/')
class Accis(MethodView):

    @accis_blp.arguments(ScoringRequestSchema)
    @accis_blp.response(201, ScoringResponseSchema)
    @list_blp.doc(operationId='accis')
    def post(self, new_data):
        return Scoring(random.randrange(10))

ceidg_blp = Blueprint('debt-register', 'debt-register', url_prefix='/debt-register')
@ceidg_blp.route("/")
class NationalRegisterOfDebt(MethodView):
    @ceidg_blp.arguments(ScoringRequestSchema, location="query")
    @accis_blp.response(201, ScoringResponseSchema)
    @accis_blp.doc(operationId='debt-register')
    def get(self, query_args):
        return Scoring(random.randrange(100))

api.register_blueprint(list_blp)
api.register_blueprint(accis_blp)
api.register_blueprint(ceidg_blp)

