from marshmallow import Schema, fields


class SwitchStatusRetrivalSchema(Schema):
    name = fields.Str(required=True)
    place_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)


class SwitchSchema(Schema):
    name = fields.Str(required=True)
    place_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    status_calculation_logic = fields.Str(required=True)


class SwitchGetSchema(Schema):
    name = fields.Str(required=True)
    place_id = fields.Int(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    user_name = fields.Str(required=True)
    user_email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


class UserGetSchema(Schema):
    user_name = fields.Str(required=True)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)


class PlaceGetSchema(Schema):
    name = fields.Str(required=True)
    user_id = fields.Int(required=True)


class PlaceGetAllSchema(Schema):
    user_id = fields.Int(required=True)


class PlaceSwitchesSchema(PlaceSchema):
    switches = fields.List(fields.Nested(SwitchSchema()), dump_only=True)

