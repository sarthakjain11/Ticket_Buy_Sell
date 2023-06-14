from application.models import UserLogin
from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField, PasswordField, StringField, SelectField, IntegerField, DateField, \
    TimeField, DecimalField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError


class RegisterForm(FlaskForm):
    username = StringField(label="Enter Username", validators=[InputRequired(), Length(min=6, max=49)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(label="Enter Password", validators=[InputRequired(), Length(min=5, max=20)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField(label="Register")

    def validate_username(self, username):
        existing_user = UserLogin.query.filter_by(username=username.data).first()

        if existing_user:
            raise ValidationError(
                "Username Already Exists,Try Login or Use different username"
            )


class LoginForm(FlaskForm):
    username = StringField(label="Enter Username", validators=[InputRequired(), Length(min=6, max=49)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(label="Enter Password", validators=[InputRequired(), Length(min=5, max=20)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField(label="Login")


class VenueForm(FlaskForm):
    venueid = IntegerField(label="Enter Venue ID", validators=[InputRequired()],
                           render_kw={"placeholder": "4 digit Venue id"})
    venuename = StringField(label="Enter Name of the Venue", validators=[InputRequired(), Length(min=1, max=80)],
                            render_kw={"placeholder": "Venue Name"})
    place = StringField(label="Enter Place", validators=[InputRequired(), Length(min=1, max=40)],
                        render_kw={"placeholder": "Place"})
    capacity = IntegerField(label="Enter Capacity", validators=[InputRequired()],
                            render_kw={"placeholder": "Range 50-500"})
    contact = IntegerField(label="Enter Contact Number", validators=[InputRequired()],
                           render_kw={"placeholder": "10 digit number"})
    submit = SubmitField(label="Save")


class ShowForm(FlaskForm):
    showid = IntegerField(label="Enter Show ID", validators=[InputRequired()],
                          render_kw={"placeholder": "show id"})
    showname = StringField(label="Enter Name of the Show", validators=[InputRequired(), Length(min=1, max=80)],
                           render_kw={"placeholder": "Show Name"})
    showdate = DateField(label="Enter Show Date",validators=[InputRequired()])
    showtime = StringField(label="Enter Show Time", validators=[InputRequired()],render_kw={"placeholder": "show time.ex 10:00 AM to 01:00 PM"})
    rating = DecimalField(label="Enter Ratings", places=1, rounding=None, use_locale=False,
                          validators=[InputRequired()], render_kw={"placeholder": "rating on scale of 10"})
    tags = TextAreaField(label="Enter tags", validators=[InputRequired()], render_kw={"placeholder": "tags"})
    price = IntegerField(label="Enter Ticket Price", validators=[InputRequired()], render_kw={"placeholder": "price"})
    submit = SubmitField(label="Save")

class BookingForm(FlaskForm):
    numoftickets = IntegerField(label="Enter Number of Tickets", validators=[InputRequired()])
    submit = SubmitField(label="Book")


