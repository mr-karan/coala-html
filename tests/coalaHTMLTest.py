import os
import re
import shutil
import sys
import unittest

from multiprocessing import Process

from coalahtml import Constants
from coalahtml.helper import get_file
from coalahtml import coala_html
from coalib.misc.ContextManagers import prepare_file
from TestUtilities import execute_coala

ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                    "coalahtml", Constants.COALA_HTML_BASE)


class coalaHTMLTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.result_file = get_file(Constants.CONFIGS['results_file'], ROOT)

    def tearDown(self):
        sys.argv = self.old_argv

    def test_output_file(self):
        update_file = ""
        noupdate_file = ""
        with prepare_file(["#todo this is todo"], None) as (lines, filename):
            p_update = Process(target=execute_coala, args=(coala_html.main,
                                                           "coala-html",
                                                           "-c", os.devnull,
                                                           "-b", "LineCountBear",
                                                           "-f", re.escape(filename),
                                                           "--nolaunch"))
            p_update.start()
            p_update.join(10)

            with open(self.result_file, 'r') as fp:
                update_file = fp.read()
            p_noupdate = Process(target=execute_coala, args=(coala_html.main,
                                                             "coala-html",
                                                             "-c", os.devnull,
                                                             "-b", "LineCountBear",
                                                             "-f",
                                                             re.escape(
                                                                 filename),
                                                             "--noupdate",
                                                             "--nolaunch"))
            p_noupdate.start()
            p_noupdate.join(10)

            with open(self.result_file, 'r') as fp:
                noupdate_file = fp.read()

        self.assertEqual(update_file, noupdate_file)
        shutil.rmtree('coalahtmlapp', ignore_errors=True)
