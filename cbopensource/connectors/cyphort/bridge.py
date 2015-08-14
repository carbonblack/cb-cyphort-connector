__author__ = 'jgarman'

from cbint.utils.detonation import DetonationDaemon
from cbint.utils.detonation.binary_analysis import (BinaryAnalysisProvider, AnalysisPermanentError,
                                                    AnalysisTemporaryError, AnalysisResult)
import cbint.utils.feed
import logging
import requests


log = logging.getLogger(__name__)


class CyphortProvider(BinaryAnalysisProvider):
    def __init__(self, cyphort_url, cyphort_apikey):
        super(CyphortProvider, self).__init__('cyphort')         # TODO: should be based on self.name (of the connector)
        self.cyphort_url = cyphort_url
        self.cyphort_apikey = cyphort_apikey
        self.headers = {'Authorization': self.cyphort_apikey}

    def check_result_for(self, md5sum):
        """
        query the cyphort api to get a report on an md5
        returns a dictionary
            status_code: the cyphort api status code
            malware: 1 if determined to be malware, otherwise 0
        """
        status = {'severity': 0, 'status_code': 0, 'completed': False}
        r = ""

        url = "%s%s" % (self.cyphort_url, "/cyadmin/api.php?op=analysis_details")
        hash_type = "md5sum"
        hash = md5sum
        url += "&get_components=0&%s=%s" % (hash_type, hash.lower())

        try:
            log.debug("Checking: %s" % url)
            r = requests.get(url, headers=self.headers, verify=False)
            j = r.json()
            status_code = j.get('status', -1)
            if status_code == 0:
                severity = j.get('analysis_array', [{}])[0].get('malware_severity', -1)
                status['completed'] = True
                severity = float(severity)
                log.info("RESULT: %s %f" % (hash, severity))
                status['severity'] = severity
                print j

        except Exception as e:
            if r:
                log.info("%s %d %s" % (url, r.status_code, r.headers))
                log.info("%s %s" % (url, r.content))
            log.error("query_cyphort: an exception occurred while querying cyphort: %s" % e)

        return status

    def analyze_binary(self, md5sum, binary_file_stream):
        pass

class CyphortConnector(DetonationDaemon):
    @property
    def num_quick_scan_threads(self):
        return 1

    @property
    def num_deep_scan_threads(self):
        return 0

    def get_provider(self):
        # TODO: complete
        pass

    def get_metadata(self):
        return cbint.utils.feed.generate_feed(self.name, summary="Cyphort",
                        tech_data="There are no requirements to share any data with Carbon Black to use this feed.",
                        provider_url="http://cyphort.com/", icon_path='',
                        display_name="Cyphort hits", category="Connectors")


if __name__ == '__main__':
    import os

    my_path = os.path.dirname(os.path.abspath(__file__))
    temp_directory = "/tmp/cyphort"

    config_path = os.path.join(my_path, "testing.conf")
    daemon = CyphortConnector('cyphort', configfile=config_path, work_directory=temp_directory,
                                logfile=os.path.join(temp_directory, 'test.log'), debug=True)
    daemon.start()
