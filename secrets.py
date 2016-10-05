import os

if os.getenv('STEAM_API_KEY'):
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
else:
    STEAM_API_KEY = 'this is totally not valid'
