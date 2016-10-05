from secrets import STEAM_API_KEY

import json, urllib2, time

TEST_MESSAGES = True

def user_info(steamid):
    try:
        #TODO:rewrite with requests library instead of urllib2 (oh well)
        request = urllib2.Request('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+unicode(STEAM_API_KEY)+'&steamids='+unicode(steamid)+'&format=json')
        response = urllib2.urlopen(request)
        parsed = json.loads(response.read())
    except urllib2.HTTPError as e:
        print unicode(e)
        print type(e)
        return e
    if parsed['response']['players']:
        return parsed['response']['players'][0]
    else:
        return ['']

#get list of game appids from user
def scrape_user(steamid):
    try:
        request = urllib2.Request('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+unicode(STEAM_API_KEY)+'&steamid='+unicode(steamid)+'&format=json')
        response = urllib2.urlopen(request)
        parsed = json.loads(response.read())
    except urllib2.HTTPError as e:
        print unicode(e)
        print type(e)
        return e
    app_ids = []
    try:
        for x in parsed['response']['games']:
            app_ids.append(x['appid'])
    except:
        return parsed
    return app_ids

#get appid indie(or whatever) status, provide T/F and data
def check_genre(appid, genre='Indie'):
    if TEST_MESSAGES: 
        print appid
    trying = True
    tries = 0
    #how much info do you want?
    result = {
        'data':{},
        'appid':appid,
        'is_valid_genre': False,
        'invalid': False,
    }
    #dunno how to deal with throttling other than trying again...
    while trying:
        try:
            request = urllib2.Request('http://store.steampowered.com/api/appdetails/?appids=' + unicode(appid))
            response = urllib2.urlopen(request)
            parsed = json.loads(response.read())
        except urllib2.HTTPError as e:
            #throttled by unknown api limits(like, I'm not just lazy this time, it's literally not public info)
            if unicode(e.code) == '429':
                if TEST_MESSAGES:
                    print 'throttled, waiting'
                    time.sleep(15)
                    print '.'
                    time.sleep(15)
                    print '..'
                    time.sleep(15)
                    print '...'
                    time.sleep(15)
                    print 'attempting to resume'
                else:
                    time.sleep(60)
                continue
            tries += 1
            #let's not dwell on the unreachable forever
            if tries > 9:
                trying = False
            continue
        #invalid id
        if parsed[unicode(appid)]['success'] == False:
            result['invalid'] = True
            trying = False
        else:
            #blank data means invalid id or errored out, I guess
            result['data'] = parsed[unicode(appid)]['data']
            #go check for the genre we're looking for
            if 'genres' in parsed[unicode(appid)]['data']:
                for x in parsed[unicode(appid)]['data']['genres']:
                    if genre in x['description']:
                        result['is_valid_genre'] = True
            trying = False
    return result
