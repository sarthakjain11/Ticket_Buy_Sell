from flask_login import UserMixin

from application import project, db


class UserLogin(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def get_id(self):
        return str(self.user_id)


class Venue(db.Model, UserMixin):
    venueid = db.Column(db.Integer, primary_key=True, unique=True)
    venuename = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.Integer, nullable=False)

    shows = db.relationship("Show", back_populates="venue")

    def get_id(self):
        return str(self.venueid)

    def __repr__(self):
        return f'Venue(venueid={self.venueid}, venuename={self.venuename}, capacity={self.capacity}, place={self.place}, contact-{self.contact},' \
               f' shows={self.shows})'


class Show(db.Model, UserMixin):
    showid = db.Column(db.Integer, primary_key=True, unique=True)
    showname = db.Column(db.String(80), nullable=False)
    showdate = db.Column(db.Date, nullable=False)
    showtime = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    booked = db.Column(db.Integer, nullable=False, default=0)
    # foreign key to link shows
    venueid = db.Column(db.Integer, db.ForeignKey('venue.venueid'))
    venue = db.relationship("Venue", back_populates="shows")

    def get_id(self):
        return str(self.showid)


class Bookings(db.Model, UserMixin):
    username = db.Column(db.String(50), db.ForeignKey('user_login.username'), primary_key=True)
    showid = db.Column(db.Integer, db.ForeignKey('show.showid'))
    venueid = db.Column(db.Integer, db.ForeignKey('venue.venueid'))
    numoftickets = db.Column(db.Integer, nullable=False)
