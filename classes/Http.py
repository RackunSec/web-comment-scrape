#!/usr/bin/env python3
## Http Class for WCS Tool
## 2022 Douglas Berdeaux (@RackunSec)
import requests  ## To make HTTP requests
from classes.Style import Style  ## My Terminal Theme
from re import match  ## Matching substrings using regexp
from sys import exit
class Http:
    def __init__(self):
        self._headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}  ## HTTP Headers to send with request
        self._style = Style()  ## My Theme class

    def get_dom(self,url):
        self._style.ok(f"Accessing URL: {url}")
        try:
            _req_data = requests.get(url,headers=self._headers)  ## Make the HTTP request and get the data
        except Exception as e:
            self._style.fail(f"Error accessing url: {url}\n  {self._style.arrow()}{e}")
            exit(1)  ## bye no reponse from whatever is pointing to that URL
        _mlc = False
        for i,line in enumerate(_req_data.iter_lines()):  ## Iterate over the lines in the HTTP response
            _decoded = line.decode("utf-8")
            if match(".*(<!--.*|/\*).*",_decoded) and not match(".*(-->|\*/).*",_decoded): ## We have a multiline comment:
                _mlc = True  ## Tracking multiline comments - I tried using do while, but line is a bytes-like obj
            if _mlc and not match(".*(-->|\*/).*",_decoded):  ## Continue the multiline comment:
                print(f"{self._style.brackets(i)}: {_decoded}")
            elif _mlc and match(".*(-->|\*/).*",str(line)):  ## Finish the multiline comment
                _mlc = False
                print(f"{self._style.brackets(i)}: {_decoded}\n")  ## Thsi can be a newline too.
            if match(r'^.*([^:>A-Za-z0-9"-]//|/\*[^\*]+\*/).*',_decoded):  ## Single line comment using //
                print(f"{self._style.brackets(i)}: {_decoded}\n")  ## This is a single line and can be separated with \n
                #pass
