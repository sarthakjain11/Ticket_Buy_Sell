from application import project, db
from application.forms import LoginForm, RegisterForm, VenueForm, ShowForm, BookingForm
from application.models import Venue, Show, Bookings
from flask import render_template, url_for, redirect, request, flash
from application.login import admindb
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user


@project.route('/addvenue', methods=('GET', 'POST'))
@login_required
def addvenue():
    form = VenueForm()
    if form.validate_on_submit():
        newvenue = Venue(venueid=form.venueid.data, venuename=form.venuename.data, place=form.place.data,
                         capacity=form.capacity.data, contact=form.contact.data)
        db.session.add(newvenue)
        db.session.commit()
        return redirect(url_for('admindb'))
    return render_template("addvenue.html", form=form)


@project.route('/edit_venue/<int:venueid>', methods=['GET', 'POST'])
@login_required
def edit_venue(venueid):
    venue = Venue.query.get_or_404(venueid)
    form = VenueForm()
    if form.validate_on_submit():
        venue.venueid = form.venueid.data
        venue.venuename = form.venuename.data
        venue.capacity = form.capacity.data
        venue.place = form.place.data
        venue.contact = form.contact.data
        # upadte database
        db.session.add(venue)
        db.session.commit()
        flash("Venue has been Updated")
        return redirect(url_for('admindb'))
    form.venueid.data = venue.venueid
    form.venuename.data = venue.venuename
    form.capacity.data = venue.capacity
    form.place.data = venue.place
    form.contact.data = venue.contact
    return render_template('edit_venue.html', form=form)


@project.route('/delete_venue/<int:venueid>', methods=['GET', 'POST'])
@login_required
def delete_venue(venueid):
    venue = Venue.query.get_or_404(venueid)
    try:
        for show in venue.shows:
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        venues = Venue.query.order_by(Venue.venueid)
        return redirect(url_for('admindb'))
    except:
        venues = Venue.query.order_by(Venue.venueid)
        return redirect(url_for('admindb'))


@project.route('/add_show/<int:venueid>', methods=['GET', 'POST'])
@login_required
def add_show(venueid):
    form = ShowForm()
    if form.validate_on_submit():
        newshow = Show(showid=form.showid.data, showname=form.showname.data, showtime=form.showtime.data,
                       showdate=form.showdate.data, rating=form.rating.data, tags=form.tags.data, price=form.price.data,
                       venueid=venueid)
        db.session.add(newshow)
        db.session.commit()
        return redirect(url_for('admindb'))
    return render_template('add_show.html', form=form)


@project.route('/edit_show/<int:showid>', methods=['GET', 'POST'])
@login_required
def edit_show(showid):
    show = Show.query.get_or_404(showid)
    form = ShowForm()
    if form.validate_on_submit():
        show.showid = form.showid.data
        show.showname = form.showname.data
        show.showtime = form.showtime.data
        show.showdate = form.showdate.data
        show.rating = form.rating.data
        show.tags = form.tags.data
        show.price = form.price.data
        # upadte database
        db.session.add(show)
        db.session.commit()
        flash("Venue has been Updated")
        return redirect(url_for('admindb'))
    form.showid.data = show.showid
    form.showname.data = show.showname
    form.showtime.data = show.showtime
    form.showdate.data = show.showdate
    form.rating.data = show.rating
    form.tags.data = show.tags
    form.price.data = show.price
    return render_template('edit_show.html', form=form)


@project.route('/delete_show/<int:showid>', methods=['GET', 'POST'])
@login_required
def delete_show(showid):
    show = Show.query.get_or_404(showid)
    try:
        db.session.delete(show)
        db.session.commit()
        flash("Show Deleted Succesfully")
        return redirect(url_for('admindb'))
    except:
        flash("Could not delete Show, Try Again!!")
        return redirect(url_for('admindb'))


@project.route('/book_tickets/<int:showid>', methods=['GET', 'POST'])
@login_required
def book_tickets(showid):
    show = Show.query.get_or_404(showid)
    venue = Venue.query.get_or_404(show.venueid)
    form = BookingForm()
    existing_booking = Bookings.query.filter_by(username=current_user.username, showid=show.showid).first()
    if form.validate_on_submit():
        if existing_booking:
            existing_booking.numoftickets = existing_booking.numoftickets + form.numoftickets.data
            show.booked = show.booked + form.numoftickets.data
            if show.booked <= venue.capacity:
                db.session.commit()
                flash("Booking Updated Successfully")
                return redirect(url_for('userdashb'))
            else:
                flash("Capacity Reached")
        else:
            newbooking = Bookings(username=current_user.username, showid=show.showid, venueid=show.venueid,
                                  numoftickets=form.numoftickets.data)
            show.booked = show.booked + form.numoftickets.data
            if show.booked <= venue.capacity:
                db.session.add(newbooking)
                db.session.commit()
                flash("Booking Successful")
                return redirect(url_for('userdashb'))
            else:
                flash("Capacity Reached")
    return render_template('bookticket.html', form=form, show=show)

