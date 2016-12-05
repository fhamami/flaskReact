import os
import unittest

from webapp import app, db

TEST_DB = 'test.db'

class webappTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # helper
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Welcome to the Flask React WebApp!', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Log In', response.data)

    def test_add_post_page_header(self):
        response = self.app.get('/add', follow_redirects=True)
        self.assertIn(b'Add a New Post', response.data)

    def test_add_recipe(self):
        response = self.app.post(
            '/add',
            data=dict(post_title='Post test',
                      post_description='This is just a post test, guys'),
            follow_redirects=True)
        # self.assertIn(b'New post, Post test, added!', response.data)

    def test_add_invalid_recipe(self):
        response = self.app.post(
            '/add',
            data=dict(post_title='',
                      post_description='This is just a post test, guys'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Post was not added.', response.data)
        # self.assertIn(b'This field is required.', response.data)

if __name__ == '__main__':
    unittest.main()
