# -*- coding: utf-8 -*-

from datetime import datetime, date
import smtplib

from flask import (Blueprint, render_template, request, abort, flash, url_for,
                   redirect, session, current_app, jsonify)
from flask.ext.mail import Message
from ..extensions import db, mail
from .forms import MakeAppointmentForm
from .models import Appointment


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        wpic_no_send_email = u" "
        form = MakeAppointmentForm(next=request.args.get('next'))

        if form.email.data is "" or form.email.data is "":
            form.email.data = wpic_no_send_email

        if not form.validate_on_submit():
            return render_template('appointment/create.html',
                                   form=form,
                                   horizontal=True)
        else:
            # Keep name and email in session
            session['name'] = form.name.data
            session['email'] = form.email.data

            appointment = Appointment()
            form.populate_obj(appointment)
            
            
            flash_message = """
            Thank you for the applcation. 
            """
            flash(flash_message)

            mail_message = Message("New Appointment",
                                   recipients=["   "])
            mail_message.body = """New appointment here:


            """ % (form.name.data, form.message.data,
                   form.date.data,
                   form.email.data,
                   form.start_time.data, form.end_time.data,
                   form.timezone.data)

            if form.email.data is not wpic_no_send_email:
                try:
                    mail.send(mail_message)
                except smtplib.SMTPException as e:
                    current_app.logger.debug("Send email faied, %s", e.message)

            return redirect(url_for('appointment.create'))

    elif request.method == 'GET':
        form = MakeAppointmentForm(formdata=request.args,
                                   next=request.args.get('next'))
 
        for key in form.data.keys():
            if key == "date":
                setattr(getattr(form, key), 'data',
                        datetime.strptime(request.args.get(key) or
                                          session.get(key) or
                                          datetime.today().strftime('%Y-%m-%d'),  # NOQA
                                          "%Y-%m-%d"))
            else:
                setattr(getattr(form, key), 'data',
                        request.args.get(key) or session.get(key))

        return render_template('appointment/create.html',
                               form=form,
                               horizontal=True)
    else:
        abort(405)
