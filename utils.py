
import re
import logging

log = logging.getLogger(__name__)

def parse_chrome_cookie_file(cookie_file):
    """
    Parse a copy/pasted cookies file (Chrome HTTP Cookie File)
    return a dictionary of key value pairs
    compatible with requests.
    :param cookie_file: a cookie file
    :return dict of cookies pairs
    """
    cookies = {}
    for line in cookie_file:
        if not re.match(r"^(#|$)", line):
            line_fields = line.strip().split("\t")
            try:
                cookies[line_fields[0]] = line_fields[1]
            except IndexError as e:
                log.error(e)        
    return cookies
