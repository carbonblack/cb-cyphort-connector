__author__ = 'jgarman'

from cbint.utils.detonation import DetonationDaemon, ConfigurationError
from cbint.utils.detonation.binary_analysis import (BinaryAnalysisProvider, AnalysisPermanentError,
                                                    AnalysisTemporaryError, AnalysisResult)
import cbint.utils.feed
import logging
import requests
from time import sleep

try:
    import simplejson as json
except ImportError:
    import json


log = logging.getLogger(__name__)


class CyphortProvider(BinaryAnalysisProvider):
    def __init__(self, cyphort_url, cyphort_apikey):
        super(CyphortProvider, self).__init__('cyphort')         # TODO: should be based on self.name (of the connector)
        self.cyphort_url = cyphort_url
        self.cyphort_apikey = cyphort_apikey
        self.headers = {'Authorization': self.cyphort_apikey}
        self.session = requests.Session()

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
            r = self.session.get(url, headers=self.headers, verify=False)
            j = r.json()
            status_code = j.get('status', -1)
            if status_code != 0:
                return None
            else:
                severity = float(j.get('analysis_array', [{}])[0].get('malware_severity', -1))
        except Exception as e:
            log.error("query_cyphort: an exception occurred while querying cyphort: %s" % e)
            raise AnalysisTemporaryError(message=e.message, retry_in=120)
        else:
            if severity > 0:
                malware_details = j.get('analysis_details', {})
                malware_name = malware_details.get('malware_name', '')
                return AnalysisResult(message="Found malware (%s)" % malware_name,
                                      extended_message=malware_details,
                                      analysis_version=1, score=int(severity*100))
            else:
                return AnalysisResult(score=0)

        return None


    def analyze_binary(self, md5sum, binary_file_stream):
        log.info("Submitting binary %s to Cyphort" % md5sum)
        try:
            filesdict = { 'file': binary_file_stream.read() } # open(file, 'rb')}
            file_meta_json = { 'file_name': md5sum }
            payload = {'file_meta_json': json.dumps(file_meta_json)}
            url = "%s%s" % (self.cyphort_url, "/cyadmin/cgi-bin/file_submit")

            res = self.session.post(url, headers=self.headers, files=filesdict, data=payload, verify=False)
            log.info("Submitted: %s HTTP CODE: %d" % (md5sum, res.status_code)) #, res.headers))

            if res.status_code == 200:
                j = res.json()
                print j
                print res.content

        except Exception as e:
            log.error("an exception occurred while submitting to cyphort: %s %s" % (md5sum, e))
            raise AnalysisTemporaryError(message=e.message, retry_in=120)

        retries = 20
        while retries:
            sleep(10)
            result = self.check_result_for(md5sum)
            if result:
                return result
            retries -= 1

        raise AnalysisTemporaryError("Maximum retries (20) exceeded submitting to Cyphort", retry_in=120)


class CyphortConnector(DetonationDaemon):
    @property
    def num_quick_scan_threads(self):
        return 1

    @property
    def num_deep_scan_threads(self):
        return 1

    def get_provider(self):
        return CyphortProvider(self.cyphort_url, self.cyphort_api_key)

    def get_metadata(self):
        return cbint.utils.feed.generate_feed(self.name, summary="Cyphort",
                        tech_data="There are no requirements to share any data with Carbon Black to use this feed.",
                        provider_url="http://cyphort.com/", icon_path='',
                        display_name="Cyphort hits", category="Connectors")

    def validate_config(self):
        super(CyphortConnector, self).validate_config()

        self.check_required_options(["cyphort_url", "cyphort_api_key"])
        self.cyphort_url = self.get_config_string("cyphort_url", None)
        self.cyphort_api_key = self.get_config_string("cyphort_api_key", None)

        return True


if __name__ == '__main__':
    import os

    my_path = os.path.dirname(os.path.abspath(__file__))
    temp_directory = "/tmp/cyphort"

    config_path = os.path.join(my_path, "testing.conf")
    daemon = CyphortConnector('cyphort', configfile=config_path, work_directory=temp_directory,
                                logfile=os.path.join(temp_directory, 'test.log'), debug=True)
    daemon.start()

