import os
import sys
import unittest

sys.path.append(os.path.abspath('../'))
from dmweb import create_app


class TestDeskMeter(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):

    	dmapp = create_app()
    	self.client = dmapp.test_client()
    	self.client.testing = True

    def tearDown(self):
        pass 

    # test method
    def test_home_status_code(self):
        result = self.client.get('/') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 


# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()