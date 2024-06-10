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
    user_name = fields.Str(required=True)
    user_email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


class UserGetSchema(Schema):
    user_name = fields.Str(required=True)
