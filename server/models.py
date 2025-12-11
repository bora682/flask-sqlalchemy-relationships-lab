from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# TODO: add association table
# --- Association table for Session ---

session_speakers = db.Table(
    "session_speakers",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("session_id", db.Integer,
              db.ForeignKey("sessions.id"), nullable=False),
    db.Column("speaker_id", db.Integer,
              db.ForeignKey("speakers.id"), nullable=False),
)


# TODO: set up relationships for all models
# --- Models with relationships ---

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # One-to-many
    sessions = db.relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    # FK to events.id
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))

    # many-to-one back to Event
    event = db.relationship("Event", back_populates="sessions")

    # many-to-many with Speaker
    speakers = db.relationship(
        "Speaker",
        secondary=session_speakers,
        back_populates="sessions",
    )


    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # one-to-one
    bio = db.relationship(
        "Bio",
        back_populates="speaker",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # many-to-many with Session
    sessions = db.relationship(
        "Session",
        secondary=session_speakers,
        back_populates="speakers",
    )

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'
    

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    # FK to speakers.id 
    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey("speakers.id"),
        unique=True,
        nullable=False,
    )

    # back to Speaker
    speaker = db.relationship("Speaker", back_populates="bio")

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'
