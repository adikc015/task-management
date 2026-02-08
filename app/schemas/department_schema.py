from marshmallow import Schema, fields

class DepartmentCreateSchema(Schema): # for input
    name=fields.Str(required=True)

class DepartmentSchema(Schema): # for output
    id=fields.Int(dump_only=True)
    name=fields.Str()