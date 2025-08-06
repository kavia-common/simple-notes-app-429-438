from marshmallow import Schema, fields, validate, EXCLUDE


class NoteCreateSchema(Schema):
    """Schema for note creation request."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=128), description="Title of the note")
    content = fields.Str(missing="", description="Content of the note")

    class Meta:
        unknown = EXCLUDE

class NoteUpdateSchema(Schema):
    """Schema for note update request."""
    title = fields.Str(validate=validate.Length(min=1, max=128), description="Title of the note")
    content = fields.Str(description="Content of the note")

    class Meta:
        unknown = EXCLUDE

class NoteSchema(Schema):
    """Schema for note serialization."""
    id = fields.Int(dump_only=True)
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
