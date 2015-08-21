__author__ = 'jgarman'

import unittest
from ConfigParser import SafeConfigParser
import os
from hashlib import md5

from cbopensource.connectors.cyphort.bridge import CyphortProvider
from cbopensource.connectors.cyphort import bridge


class CyphortTest(unittest.TestCase):
    def setUp(self):
        bridge_file = bridge.__file__
        config_path = os.path.join(os.path.dirname(os.path.abspath(bridge_file)), "testing.conf")

        self.test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "putty.exe")
        self.config = SafeConfigParser()
        self.config.read(config_path)

        self.cyphort_provider = CyphortProvider(self.config.get("bridge", "cyphort_url"),
                                                self.config.get("bridge", "cyphort_api_key"))

    def test_submit_md5sum(self):
        print self.cyphort_provider.check_result_for('8ddbea365fac80b17e6046c312db52f6')

    def test_submit_binary(self):
        file_data = open(self.test_file, 'rb')
        md5sum = md5(file_data.read()).hexdigest()
        file_data.seek(0)
        print self.cyphort_provider.analyze_binary(md5sum, file_data)

    def test_submitted_binary(self):
        print self.cyphort_provider.check_result_for('354d9abefa0ed67a08bd056324284d6e')
