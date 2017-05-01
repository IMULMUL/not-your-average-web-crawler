# -*- coding: utf-8 -*-

# MIT License
# 
# Copyright (c) 2017 Tijme Gommers
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from nyawc.scrapers.JSONRegexLinkScraper import JSONRegexLinkScraper
from nyawc.Queue import Queue
from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response
from nyawc.Options import Options

import unittest
 
class TestScrapersJSONRegexLinkScraper(unittest.TestCase):
    """The TestScrapersJSONRegexLinkScraper class tests if the JSONRegexLinkScraper is working correctly.

    Attributes:
        __host (str): The host were the new URLs were found on
        __urls list(obj): The URLs that were found

    """

    __host = "https://example.ltd/"

    __urls = [
        {"url": """https://example.ltd/?unique=1""", "must_pass": True, "test": """[\"https://example.ltd/?unique=1\"]"""},
        {"url": """http://example.ltd/?unique=2""", "must_pass": True, "test": """{\"http://example.ltd/?unique=2\":\"\"}"""},
        {"url": """https://example.ltd/?unique=3""", "must_pass": True, "test": """{\"//example.ltd/?unique=3\":\"\"}"""},
        {"url": """https://example.ltd/aa/bb/?unique=4""", "must_pass": True, "test": """{\"/aa/bb/?unique=4\":\"\"}"""},
        {"url": """https://example.ltd/aa/bb/?unique=5""", "must_pass": True, "test": """{\"\":\"/aa/bb/?unique=5\"}"""},

        {"url": None, "must_pass": False, "test": """{\"\":\"asdfasdf/asdfasdf\"}"""},
    ]

    def test_xml_url_count(self):
        """Test if the amount of URLs found complies with the expected amount."""

        html = ""
        for url in self.__urls:
            html += "\n" + url["test"]

        finder = JSONRegexLinkScraper(Options(), QueueItem(Request(""), Response()))
        matches = finder.get_requests_from_content(self.__host, html)

        self.assertEqual(len(matches), 5)
 
    def test_xml_url_matches(self):
        """Test if all the URLs match the found URLs."""
        
        for url in self.__urls:
            finder = JSONRegexLinkScraper(Options(), QueueItem(Request(""), Response()))
            requests = finder.get_requests_from_content(self.__host, url["test"])

            if url["must_pass"]:
                self.assertEqual(requests[0].url, url["url"])
                self.assertEqual(len(requests), 1)
            else:
                self.assertEqual(len(requests), 0)
