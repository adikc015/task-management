from marshmallow import Schema, fields

# For output
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str()
    priority = fields.Str()
    due_date = fields.Date(allow_none=True)
    
# For input
class TaskCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(load_default="pending")
    priority = fields.Str(allow_none=True)
    due_date = fields.Date(allow_none=True)
    project_id = fields.Int(required=True)
    
# For update
class TaskUpdateSchema(Schema):
    title=fields.Str()
    description=fields.Str(allow_none=True)
    status=fields.Str()
    priority=fields.Str()
    due_date=fields.Date(allow_none=True)