import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_connect(self):
        rv = self.app.get('/')
        # print(rv, rv.data)

    def test_img_upload(self):
        
        with open('img.test.png', 'rb') as img:
            rv = self.app.post('/', buffered=True, content_type='multipart/form-data', data={'file': img}, follow_redirects=True)
            print(rv.status_code, type(rv.data), rv.content_type)
            self.assertEqual(rv.status_code, 200)
            self.assertIs(type(rv.data), bytes)

    # def test_empty_db(self):
    #     rv = self.app.get('/')
    #     print(rv.data)
    #     assert b'No entries here so far' in rv.data
    
    # def test_login_logout(self):
    #     rv = self.login('admin', 'default')
    #     assert b'You were logged in' in rv.data
    #     rv = self.logout()
    #     assert b'You were logged out' in rv.data
    #     rv = self.login('adminx', 'default')
    #     assert b'Invalid username' in rv.data
    #     rv = self.login('admin', 'defaultx')
    #     assert b'Invalid password' in rv.data

    # def test_messages(self):
    #     self.login('admin', 'default')
    #     rv = self.app.post('/add', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here'
    #     ), follow_redirects=True)
    #     print(rv)
    #     assert b'No entries here so far' not in rv.data
    #     assert b'&lt;Hello&gt;' in rv.data
    #     assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()