# coding=utf-8
"""
ip.py - jenni IP Lookup Module
Copyright 2013, Michael Yanovich (yanovich.net)
Copyright 2011, Dimitri Molenaars (TyRope.nl)
Licensed under the Eiffel Forum License 2.

More info:
  * Willie: http://willie.dftba.net
  * jenni: https://github.com/myano/jenni/
  * Phenny: http://inamidst.com/phenny/

This module has been improted from Willie.
"""

import re
import web

def ip(jenni, input):
    """IP Lookup tool"""
    if not input.group(2):
        return jenni.reply("No search term.")
    query = input.group(2).encode('utf-8')
    uri = 'http://www.rscript.org/lookup.php?type=ipdns&ip='
    answer = web.get(uri + web.quote(query.replace('+', '%2B')))
    if answer:
        invalid = re.search("(?:INVALID: )([\S ]*)", answer)
        if invalid:
            response = "[IP/Host Lookup] "+invalid.group(1)
        else:
            #parse stuffs.
            host = re.search("(?:Hostname:[ ]?)([\S ]*)", answer)
            isp = re.search("(?:ISP:[ ]?)([\S ]*)", answer)
            org = re.search("(?:Organization:[ ]?)([\S ]*)(?:Services:)", answer)
            typ = re.search("(?:Type:[ ]?)([\S ]*)", answer)
            assign = re.search("(?:Assignment:[ ]?)([\S ]*)", answer)
            city = re.search("(?:City:[ ]?)([\S ]*)", answer)
            state = re.search("(?:State/Region:[ ]?)([\S ]*)", answer)
            country = re.search("(?:Country:[ ]?)([\S ]*)(?:  )", answer)

            if not host or not isp or not org or not typ or not assign or not city or not state or not country:
                response = "[IP/Host Lookup] Something went wrong, please try again."
            else:
                response = "[IP/Host Lookup] Hostname: "+host.group(1)
                response += " | ISP: "+isp.group(1)
                response += " | Organization: "+org.group(1)
                response += " | Type: "+typ.group(1)
                response += " | Assignment: "+assign.group(1)
                response += " | Location: "+city.group(1)
                response += ", "+state.group(1)
                response += ", "+country.group(1)+"."
        jenni.say(response)
    else:
        jenni.reply('Sorry, no result.')
ip.commands = ['iplookup','ip']
ip.example = '.iplookup 8.8.8.8'

if __name__ == '__main__':
    print __doc__.strip()
