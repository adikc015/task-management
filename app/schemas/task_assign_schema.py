from marshmallow import Schema, fields

class TaskAssignSchema(Schema):
    user_ids = fields.List(
        fields.Int(),
        required=True,
        validate=lambda x:len(x)>0
    )