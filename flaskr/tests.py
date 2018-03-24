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
        self.assertEqual(rv.status_code, 200)

    def test_img_upload(self):
        
        with open('img.test.png', 'rb') as img:
            rv = self.app.post('/', buffered=True, content_type='multipart/form-data', data={'file': img}, follow_redirects=True)
            self.assertEqual(rv.status_code, 200)
            self.assertIn('image', rv.content_type)

if __name__ == '__main__':
    unittest.main()