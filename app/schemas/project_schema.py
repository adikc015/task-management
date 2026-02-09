from marshmallow import Schema, fields

class ProjectSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()
    department_id=fields.Int()

class ProjectCreateSchema(Schema):
    name=fields.Str(required=True)
    department_id=fields.Int(required=True)