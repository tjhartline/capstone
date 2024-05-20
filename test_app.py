import unittest
from dash.testing.application_runners import import_app

class TestDashApp(unittest.TestCase):
    def setUp(self):
        self.app = import_app('app')

    def test_layout_components(self):
        # Test if the layout components are rendered correctly
        self.assertIn('Capstone Project Dashboard', self.app.layout.children[0].children)
        self.assertIn('Tammy Hartline\'s Grazioso Salvare DashBoard Final Project', self.app.layout.children[1].children)
        self.assertIn('All', self.app.layout.children[4].children[0].children[0].children)

    def test_update_dashboard_callback(self):
        # Test the update_dashboard callback
        with self.app.test_client() as client:
            # Simulate a button click
            response = client.post('/_dash-update-component', json={
                'output': ['bubble-plot', 'datatable-id.data', 'datatable-id.columns'],
                'inputs': [{'id': 'btn-all', 'property': 'n_clicks', 'value': 1}],
                'changedPropIds': ['btn-all.n_clicks']
            })

            # Check if the response contains the expected components
            self.assertEqual(response.status_code, 200)
            self.assertIn('bubble-plot', response.get_json()['response']['bubble-plot'])
            self.assertIn('data', response.get_json()['response']['datatable-id'])
            self.assertIn('columns', response.get_json()['response']['datatable-id'])

if __name__ == '__main__':
    unittest.main()
