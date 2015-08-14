__author__ = 'jgarman'

from cbopensource.connectors.cyphort.bridge import CyphortProvider
import cbopensource.connectors.cyphort.bridge
import unittest
from ConfigParser import SafeConfigParser
import os


class CyphortTest(unittest.TestCase):
    def setUp(self):
        bridge_file = cbopensource.connectors.cyphort.bridge.__file__
        config_path = os.path.join(os.path.dirname(os.path.abspath(bridge_file)), "testing.conf")
        self.config = SafeConfigParser()
        self.config.read(config_path)

        self.cyphort_provider = CyphortProvider(self.config.get("bridge", "cyphort_url"),
                                                self.config.get("bridge", "cyphort_api_key"))

    def test_submit_md5sum(self):
        print self.cyphort_provider.check_result_for('8ddbea365fac80b17e6046c312db52f6')

