#!/usr/bin/env/python
# conding: utf-8

import simplejson as json
import urllib2
import time
import logging
import pprint

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

URLCATEGORY="http://printdirect.ru/storefront/cat/Prazdniki_i_sobytiya/Den_Sv.Patrika_%2817.03%29"
URL = "http://printdirect.ru/index.php?mode=storefront&user_id=&categ_id=0&search_icat_color=0&search_icat_group=0&search_icat_style=0&search_icat_access=0&collection_id=0&bg=1&bg_start={start}&bg_limit={limit}"
USERNAME = "Marjorie"


def get_url(url, headers={}):

    request = urllib2.Request(url, headers=headers)

    start = time.time()
    data = urllib2.urlopen(request)
    return data, time.time() - start


def main():

    i = 0
    end = 5000
    limit = 40
    page = 1

    categoryfp, time_taken = get_url(URLCATEGORY)
    categoryfp.read()
    phpsessid = categoryfp.headers.getrawheader("Set-Cookie").split(";")[0].strip()
    phpsessid += ';'
    print "Got", phpsessid

    users = {}

    while i + limit <= end:

        url = URL.format(start=i, limit=limit)
        web_page_data, time_taken = get_url(url, {"Cookie": phpsessid})
        logging.debug("loaded {} in {} sec".format(url, time_taken))
        parsed_data = json.load(web_page_data)
        if len(parsed_data) == 0:
            print "empty data:", parsed_data
            break
        else:
            for itemi, item in enumerate(parsed_data):
                if item["username"] == USERNAME:
                    print USERNAME, "item at place", i + itemi, "approx on page", page
                if not users.get(item["username"]):
                    users[item["username"]] = 1
                else:
                    users[item["username"]] += 1
        i += limit
        page += 1

    print "Finished."

    print
    print "Top 20:"

    users_sorted = sorted(users.keys(), key = lambda x: users[x])
    users_sorted.reverse()
    users_sorted = users_sorted[:20]

    for user in users_sorted:
        print "\t", user, users[user]


if __name__ == "__main__":
    main()