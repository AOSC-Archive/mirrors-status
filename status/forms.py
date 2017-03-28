from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms import validators
#
from .models import Mirror
#
#
# class LoginForm(Form):
#     username = TextField(u'Username', validators=[validators.required()])
#     password = PasswordField(u'Password', validators=[validators.optional()])
#
#     def validate(self):
#         check_validate = super(LoginForm, self).validate()
#
#         # if our validators do not pass
#         if not check_validate:
#             return False
#
#         # Does our the exist
#         user = User.query.filter_by(username=self.username.data).first()
#         if not user:
#             self.username.errors.append('Invalid username or password')
#             return False
#
#         # Do the passwords match
#         if not user.check_password(self.password.data):
#             self.username.errors.append('Invalid username or password')
#             return False
#
#         return True

class MirrorUpdateForm(Form):
    area = StringField(u'Where is the mirror?', validators=[validators.required()])
    name = StringField(u"What's the name of the mirror?", validators=[validators.required()])
    url = StringField(u"What's the url to the mirror?", validators=[validators.required(), validators.url()])
    last_update_url = StringField(u"What's the url to the last_update file?", validators=[validators.required(), validators.url()])

    def validate(self):
        check_validate = super(MirrorUpdateForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        if len(Mirror.query.filter_by(url=self.url.data).all()) != 0:
            self.url.errors.append('Already existed.')
            return False

        return True