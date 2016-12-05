import os
import unittest

from webapp import app, db

TEST_DB = 'user.db'

class webappTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    # helper

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    # unit test

    def test_loginTest(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'Log In', response.data)

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)

    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('test@us.er', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertIn(b'Thanks for registering!', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('test@us.er', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/register', follow_redirects=True)
        response = self.register('test@us.er', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
        self.assertIn(b'ERROR! Email (test@us.er) already exists.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('test@us.er', 'FlaskIsAwesome', '')
        self.assertIn(b'This field is required.', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('test@us.er', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('test@us.er', 'FlaskIsAwesome')
        # self.assertIn(b'Welcome, test@us.er!', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('test@us.er', 'FlaskIsAwesome')
        self.assertIn(b'ERROR! Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('test@us.er', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('test@us.er', 'FlaskIsAwesome')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)


if __name__ == '__main__':
    unittest.main()
