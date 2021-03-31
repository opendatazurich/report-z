#!/usr/bin/env python3

import subprocess
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import certifi


def _download_request(url):
    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    headers = {'user-agent': 'Mozilla Firefox Mozilla/5.0; metaodi report-z'}
    r = http.get(url, headers=headers, verify=certifi.where(), timeout=10)
    r.raise_for_status()
    return r


def download(url, encoding='utf-8'):
    r = _download_request(url)
    if encoding:
        r.encoding = encoding
    return r.text


def download_content(url):
    r = _download_request(url)
    return r.content


def download_file(url, path):
    r = _download_request(url, True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)


def download_pdf(url):
    r = _download_request(url)
    return pdftotext(r.content)


def pdftotext(pdf, encoding='utf-8', raw=False, layout=False, page=None, rect=None, fixed=None):
    pdf_command = ['pdftotext']
    if raw:
        pdf_command += ['-raw']
    if layout:
        pdf_command += ['-layout']
    if page:
        pdf_command += ['-f', str(page), '-l', str(page)]
    if rect:
        pdf_command += ['-x', str(rect[0]), '-y', str(rect[1]), '-W', str(rect[2]), '-H', str(rect[3])]
    if fixed:
        pdf_command += ['-fixed', str(fixed)]
    pdf_command += ['-', '-']
    p = subprocess.Popen(pdf_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(input=pdf)[0]
    return out.decode(encoding)