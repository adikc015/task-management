from marshmallow import Schema, fields

class UserSchema(Schema): # for output
    id=fields.Int(dump_only=True)
    name=fields.Str()
    email=fields.Email()
    role=fields.Str()
    department_id=fields.Int()
     
class UserCreateSchema(Schema): # for input
    name=fields.Str(required=True)
    email=fields.Email(required=True)
    password=fields.Str(required=True, load_only=True)
    role=fields.Str(required=True)
    department_id=fields.Int(required=True)