from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, Note
from ..schemas import NoteCreateSchema, NoteUpdateSchema, NoteSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Operations on notes"
)

# PUBLIC_INTERFACE
@blp.route("/")
class NotesList(MethodView):
    """CRUD endpoints for listing and creating notes."""

    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """List all notes."""
        notes = Note.query.order_by(Note.created_at.desc()).all()
        return notes

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, new_data):
        """Create a new note."""
        try:
            note = Note(**new_data)
            db.session.add(note)
            db.session.commit()
            return note
        except SQLAlchemyError as e:
            db.session.rollback()
            blp.abort(400, message=f"Error creating note: {str(e)}")

# PUBLIC_INTERFACE
@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """CRUD endpoints for retrieving, updating, and deleting a single note."""

    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """Retrieve a note by ID."""
        note = Note.query.get(note_id)
        if not note:
            blp.abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def patch(self, update_data, note_id):
        """Update a note by ID (partial update)."""
        note = Note.query.get(note_id)
        if not note:
            blp.abort(404, message="Note not found")
        for key, value in update_data.items():
            setattr(note, key, value)
        try:
            db.session.commit()
            return note
        except SQLAlchemyError as e:
            db.session.rollback()
            blp.abort(400, message=f"Error updating note: {str(e)}")

    # PUBLIC_INTERFACE
    @blp.response(204)
    def delete(self, note_id):
        """Delete a note by ID."""
        note = Note.query.get(note_id)
        if not note:
            blp.abort(404, message="Note not found")
        try:
            db.session.delete(note)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            blp.abort(400, message=f"Error deleting note: {str(e)}")
