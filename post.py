#!/usr/bin/python 

import urllib,urllib2
import MultipartPostHandler
import json
import sys

# mixi Graph API Settings
CONSUMER_KEY    = '__please_change_your_setting__'
CONSUMER_SECRET = '__please_change_your_setting__'
REDIRECT_URL    = '__please_change_your_setting__'

if __name__ == '__main__':
    
    # auth

    auth_base = 'https://mixi.jp/connect_authorize.pl'
    auth_params = {
        'client_id'         : CONSUMER_KEY,
        'response_type'     : 'code',
        'scope'             : 'w_voice',
        'display'           : 'pc'
    }
    auth_url = auth_base + '?' + urllib.urlencode(auth_params)
    
    print "Aauthorize request in this page :"
    print auth_url
    print "Please input redirest url's 'code' parameter :"
    
    code = sys.stdin.readline().replace('\n','')

    # get token

    token_params = {
        'grant_type'    : 'authorization_code',
        'client_id'     : CONSUMER_KEY,
        'client_secret' : CONSUMER_SECRET,
        'code'          : code,
        'redirect_uri'  : REDIRECT_URL
    }
    token_res = urllib.urlopen(
            'https://secure.mixi-platform.com/2/token',
             urllib.urlencode(token_params)
             ).read()
    token_dic = json.loads(token_res)

    # post
    post_opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
    post_base = "http://api.mixi-platform.com/2/voice/statuses/update?oauth_token=%s" % token_dic['access_token']
    post_params = {
        'status'    :   'voice post from python',
        'photo'     :   open('sample.jpg', 'rb')
    }
    post_res = post_opener.open(post_base,post_params).read()
    token_dic = json.loads(post_res)

    if token_dic.has_key('created_at') :
        print 'done. created at ' + token_dic['created_at']

