#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.api.v1.reviews import api as review_namespace
from flask_restx import Api


class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(review_namespace, path='/reviews')
        self.client = self.app.test_client()

    @patch('app.api.v1.reviews.facade.create_review')
    def test_post_review_success(self, mock_create):
        mock_create.return_value = {
            'id': '123',
            'text': 'Super séjour !',
            'rating': 5,
            'user_id': 'u1',
            'place_id': 'p1'
        }
        payload = {
            'text': 'Super séjour !',
            'rating': 5,
            'user_id': 'u1',
            'place_id': 'p1'
        }
        res = self.client.post('/reviews/', json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['text'], 'Super séjour !')

    @patch('app.api.v1.reviews.facade.create_review')
    def test_post_review_invalid(self, mock_create):
        mock_create.return_value = ({'error': 'Missing rating'}, 400)
        payload = {
            'text': 'Pas de note',
            'user_id': 'u1',
            'place_id': 'p1'
        }
        res = self.client.post('/reviews/', json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn('error', res.get_data(as_text=True))

    @patch('app.api.v1.reviews.facade.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all):
        mock_get_all.return_value = ([{
            'id': '123',
            'text': 'Parfait',
            'rating': 5
        }], 200)
        res = self.client.get('/reviews/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Parfait', res.get_data(as_text=True))

    @patch('app.api.v1.reviews.facade.get_review')
    def test_get_review_success(self, mock_get):
        mock_get.return_value = ({
            'id': '123',
            'text': 'Génial',
            'rating': 5
        }, 200)
        res = self.client.get('/reviews/123')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['text'], 'Génial')

    @patch('app.api.v1.reviews.facade.get_review')
    def test_get_review_not_found(self, mock_get):
        mock_get.return_value = ({'error': 'Review not found'}, 404)
        res = self.client.get('/reviews/999')
        self.assertEqual(res.status_code, 404)
        self.assertIn('not found', res.get_data(as_text=True))

    @patch('app.api.v1.reviews.facade.delete_review')
    def test_delete_review_success(self, mock_delete):
        mock_delete.return_value = {'message': 'Review deleted successfully'}
        res = self.client.delete('/reviews/123')
        self.assertEqual(res.status_code, 200)
        self.assertIn('deleted', res.get_data(as_text=True))

    @patch('app.api.v1.reviews.facade.delete_review')
    def test_delete_review_not_found(self, mock_delete):
        mock_delete.return_value = ({'error': 'Review not found'}, 404)
        res = self.client.delete('/reviews/999')
        self.assertEqual(res.status_code, 404)
        self.assertIn('not found', res.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
