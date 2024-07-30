from marshmallow import Schema, fields


class SwitchStatusRetrivalSchema(Schema):
    uuid = fields.Str(required=True)
    status = fields.Str(dump_only=True)

class SwitchStatusCalculationTestSchema(Schema):
    switch_calculation_logic = fields.Str(required=True)
    switch_status = fields.Str(dump_only=True)
    error_message = fields.Str(dump_only=True)

class SwitchSchema(Schema):
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    place_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    status_calculation_logic = fields.Str(required=True)


class SwitchGetSchema(Schema):
    uuid = fields.Str(required=True)


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


class LocationSchema(Schema):
    id = fields.Int(dump_only=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)
    location = fields.Nested(LocationSchema(), required=True)


class PlaceGetSchema(Schema):
    place_id = fields.Int(required=True)
    user_id = fields.Int(required=True)


class PlaceGetAllSchema(Schema):
    user_id = fields.Int(required=True)


class PlaceSwitchesSchema(PlaceSchema):
    switches = fields.List(fields.Nested(SwitchSchema()), dump_only=True)

