import datetime

from flask.ext.wtf import Form
from wtforms import (Field, HiddenField, TextField,
                     TextAreaField, SubmitField, DateField, SelectField)
from wtforms.validators import Required, Length, Email
from flask.ext.wtf.html5 import EmailField

from ..utils import (USERNAME_LEN_MIN, USERNAME_LEN_MAX)

EMAIL_LEN_MIN = 4
EMAIL_LEN_MAX = 64

MESSAGE_LEN_MIN = 16
MESSAGE_LEN_MAX = 1024

TIMEZONE_LEN_MIN = 1
TIMEZONE_LEN_MAX = 64

TIMEZONES = {
    "TZ1": [("-8.00", "(GMT -8:00) Pacific Time (US & Canada)"),
            ("-7.00", "(GMT -7:00) Mountain Time (US & Canada)"),
            ("-6.00", "(GMT -6:00) Central Time (US & Canada), Mexico City"),
            ("-5.00", "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima")],
   }

class SelectOptgroupField(SelectField):

    def pre_validate(self, form):
        return True

class TimeRangeSliderField(Field):
    pass

class MakeAppointmentForm(Form):
    next = HiddenField()

    name = TextField(u'Name',
                     [Required(),
                      Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    time_range = TimeRangeSliderField(u'Time Range')
    start_time = HiddenField(u'start_time')
    end_time = HiddenField(u'end_time')
    email = EmailField(u'Email',
                       [Email(),
                        Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)])
    date = DateField(u'Date',
                     [Required()],
                     default=datetime.date.today())
    timezone = SelectOptgroupField(u'Timezone',
                                   [Required(),
                                    Length(TIMEZONE_LEN_MIN,
                                           TIMEZONE_LEN_MAX)],
                                   choices=TIMEZONES)
    message = TextAreaField(u'Message',
                            [Required(),
                             Length(MESSAGE_LEN_MIN, MESSAGE_LEN_MAX)],
                            description={'placeholder'})
    submit = SubmitField('OK')
