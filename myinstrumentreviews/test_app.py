import unittest
import pytest
from app import app, db

class MyAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Instrument Reviews", response.data)

    def test_add_review_route(self):
        response = self.app.post('/add_review', data=dict(
            instrument='Test Instrument',
            review='Test Review'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Instrument", response.data)
        self.assertIn(b"Test Review", response.data)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Instrument Reviews" in response.data

def test_add_review_route(client):
    response = client.post('/add_review', data=dict(
        instrument='Test Instrument',
        review='Test Review'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Instrument" in response.data
    assert b"Test Review" in response.data

if __name__ == '__main__':
    unittest.main()
