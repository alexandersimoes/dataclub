# test_api.py
from dataviva.visualize.build_models import TreeMap, Stacked, Scatter, Network, Rings, Compare, GeoMap
from dataviva.visualize.build_list import buildList
import os
import json
import dataviva
import unittest
import time
import numpy as np
import itertools

def parse(url):
    if "rais" in url:
        api = "rais"
    elif "secex" in url:
        api = "secex"
    elif "/ei" in url:
        api = "ei"
    api_str = "/%s" % (api)
    return api_str + url.split(api_str)[1]


class APITest(unittest.TestCase):
    
    def setUp(self):
        dataviva.app.config['SQLALCHEMY_ECHO'] = False
        self.app = dataviva.app.test_client()
    

    def test_secex(self):
        key_names = ["bra_id", "hs_id", "wld_id"]
        keys = ["4mg030000", "a01113", "1113" ]
        my_nesting = [ [1,3,5,7,8,9], [2,6], [2,5] ]
        self.combo_helper(keys, key_names, my_nesting, "/secex")

    def test_rais(self):
        key_names = ["bra_id", "cnae_id", "cbo_id"]
        keys = ["4mg030000", "a01113", "1113" ]
        my_nesting = [ [1,3,5,7,8,9], [1,3,6], [1,4] ]
        self.combo_helper(keys, key_names, my_nesting, "/rais")

    def test_ei(self):
        key_names = ["bra_id_s", "cnae_id_s", "bra_id_r", "cnae_id_r", "hs_id"]
        keys = ["4mg030000", "b07", "4mg030000", "b07", "010101" ]
        my_nesting = [ [1,3,5,9], [1,3], [1,3,5,9], [1,3], [2,6] ]
        self.combo_helper(keys, key_names, my_nesting, "/ei")

    def combo_helper(self, keys, key_names, my_nesting, onlyshow):
        all_combos = itertools.product(*my_nesting)
        for combo in all_combos:
            params = { key_names[idx] : keys[idx][:depth] for idx, depth in enumerate(combo) }
            self.buildlist_helper(params, onlyshow=onlyshow)

    def buildlist_helper(self,params, onlyshow):
        builds  = buildList( params )
        urls = {}


        for build in builds:
            url = parse(build.url())
            if onlyshow in url:
                urls[url] = True

        # print "THESE urls", urls

        for url in urls:
            api_endpoint = url 
            print "Hitting", api_endpoint
            start = time.time()
            json_data = self.app.get(api_endpoint).data
            end = time.time()
            data = json.loads(json_data)
            self.assertNotEqual(len(data["data"]), 0)
            self.assertNotEqual(len(data["headers"]), 0)
        
            delta = end - start
            print "time taken", delta
            urls[url] = delta

        print "Avg time", np.mean(urls.values())


if __name__ == '__main__':
   

    unittest.main()
