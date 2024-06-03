from marshmallow import Schema, fields


class SwitchDetails(Schema):
    status = fields.Str(dump_only=True)


class SwitchSchema(Schema):
    name = fields.Str(required=True)
    details = fields.Nested(SwitchDetails(), dump_only=True)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
