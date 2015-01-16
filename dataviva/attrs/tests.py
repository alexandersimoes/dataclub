import os
import json
import dataviva
import unittest

class AttrViewsTest(unittest.TestCase):
    attr_type = "hs"
    attr = "020901"
    depths = [2,4,6]
    order_col = "export_val"
    limit = 9
    
    def setUp(self):
        dataviva.app.config['SQLALCHEMY_ECHO'] = False
        self.app = dataviva.app.test_client()
    
    def test_all(self):
        url = '/attrs/{0}/'.format(self.attr_type)
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        self.assertNotEqual(len(data["header"]), 0)
        self.assertNotEqual(len(data["data"]), 0)
    
    def test_attr(self):
        url = '/attrs/{0}/{1}/'.format(self.attr_type, self.attr)
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        self.assertNotEqual(len(data["header"]), 0)
        self.assertEqual(len(data["data"]), 1)
    
    def test_attr_depths(self):
        attr = self.attr[:self.depths[0]]
        url = '/attrs/{0}/{1}.show.{2}/'.format(self.attr_type, attr, self.depths[-1])
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        id_index = data["header"].index("id")
        data_depths = [len(item[id_index]) for item in data["data"]]
        data_ids = [item[id_index][:self.depths[0]] for item in data["data"]]
        self.assertEqual(len(set(data_depths)), 1)
        self.assertEqual(set(data_ids), set([attr]))
    
    def test_depths(self):
        for d in self.depths:
            url = '/attrs/{0}/?depth={1}'.format(self.attr_type, d)
            json_data = self.app.get(url).data
            data = json.loads(json_data)
            id_index = data["header"].index("id")
            data_depths = [len(item[id_index]) for item in data["data"]]
            self.assertEqual(len(set(data_depths)), 1)
    
    def test_limit(self):
        url = '/attrs/{0}/?limit={1}'.format(self.attr_type, self.limit)
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        self.assertEqual(len(data["data"]), self.limit)
    
    def test_order_asc(self):
        url = '/attrs/{0}/?order={1}'.format(self.attr_type, self.order_col)
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        order_col_index = data["header"].index(self.order_col)
        sorted_data = json.loads(json_data)["data"]
        sorted_data = sorted(sorted_data, key=lambda k: k[order_col_index], reverse=False)
        self.assertEqual(data["data"], sorted_data)
    
    def test_order_desc(self):
        url = '/attrs/{0}/?order={1}.desc'.format(self.attr_type, self.order_col)
        json_data = self.app.get(url).data
        data = json.loads(json_data)
        order_col_index = data["header"].index(self.order_col)
        sorted_data = json.loads(json_data)["data"]
        sorted_data = sorted(sorted_data, key=lambda k: k[order_col_index], reverse=True)
        self.assertEqual(data["data"], sorted_data)

if __name__ == '__main__':
    # unittest.main()
    ''' BRA 
    AttrViewsTest.attr_type = "bra"
    AttrViewsTest.attr = "mg030000"
    AttrViewsTest.depths = [2,4,6,7,8]
    AttrViewsTest.order_col = "pop"
    '''
    
    ''' WLD 
    AttrViewsTest.attr_type = "wld"
    AttrViewsTest.attr = "aschn"
    AttrViewsTest.depths = [2,5]
    AttrViewsTest.order_col = "export_val"
    '''
    
    ''' CNAE 
    AttrViewsTest.attr_type = "cnae"
    AttrViewsTest.attr = "a01113"
    AttrViewsTest.depths = [1,3,6]
    AttrViewsTest.order_col = "num_emp"
    '''
    
    ''' CBO 
    AttrViewsTest.attr_type = "cbo"
    AttrViewsTest.attr = "2542"
    AttrViewsTest.depths = [1,4]
    AttrViewsTest.order_col = "num_emp"
    '''
    
    AttrViewsTest.attr_type = "cbo"
    AttrViewsTest.attr = "2542"
    AttrViewsTest.depths = [1,4]
    AttrViewsTest.order_col = "num_emp"
        
    unittest.main()