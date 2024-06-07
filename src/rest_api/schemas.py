from marshmallow import Schema, fields


class SwitchStatusRetrivalSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Str(dump_only=True)


class SwitchSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    status_calculation_logic = fields.Str(required=True)

class SwitchGetSchema(Schema):
    name = fields.Str(required=True)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
