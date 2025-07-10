#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.api.v1.places import api as place_namespace
from flask_restx import Api


class TestPlaceAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(place_namespace, path='/places')
        self.client = self.app.test_client()

    @patch('app.api.v1.places.HBnBFacade.create_place')
    def test_post_place_success(self, mock_create):
        mock_place = MagicMock()
        mock_place.to_dict.return_value = {
            'id': '1',
            'title': 'Appartement',
            'price': 120.0,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner_id': 'u1',
            'description': 'Belle vue',
            'amenities': ['a1']
        }
        mock_create.return_value = mock_place

        payload = {
            'title': 'Appartement',
            'description': 'Belle vue',
            'price': 120.0,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner_id': 'u1',
            'amenities': ['a1']
        }

        res = self.client.post('/places/', json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['title'], 'Appartement')

    @patch('app.api.v1.places.HBnBFacade.get_all_places')
    def test_get_all_places(self, mock_get_all):
        mock_place = MagicMock()
        mock_place.to_dict.return_value = {
            'title': 'Maison',
            'price': 80.0,
            'latitude': 43.0,
            'longitude': 1.3,
            'owner_id': 'u1',
            'description': '',
            'amenities': []
        }
        mock_get_all.return_value = [mock_place]

        res = self.client.get('/places/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Maison', res.get_data(as_text=True))

    @patch('app.api.v1.places.HBnBFacade.get_place')
    def test_get_place_by_id(self, mock_get):
        mock_place = MagicMock()
        mock_place.to_dict.return_value = {
            'title': 'Villa',
            'price': 200.0,
            'latitude': 40.0,
            'longitude': -3.0,
            'owner_id': 'u2',
            'description': 'Piscine privée',
            'amenities': []
        }
        mock_get.return_value = mock_place

        res = self.client.get('/places/123')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Villa', res.get_data(as_text=True))

    @patch('app.api.v1.places.HBnBFacade.get_place')
    @patch('app.api.v1.places.Place.save')
    def test_put_place_success(self, mock_save, mock_get):
        mock_place = MagicMock()
        mock_get.return_value = mock_place

        payload = {
            'title': 'Modifié',
            'price': 150.0,
            'latitude': 45.0,
            'longitude': 5.0,
            'description': 'Nouveau'
        }

        res = self.client.put('/places/123', json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn('updated', res.get_data(as_text=True))

    @patch('app.api.v1.places.HBnBFacade.get_place')
    def test_get_place_not_found(self, mock_get):
        mock_get.return_value = None
        res = self.client.get('/places/999')
        self.assertEqual(res.status_code, 404)
        self.assertIn('not found', res.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
