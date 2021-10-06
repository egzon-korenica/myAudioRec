from datetime import datetime

eventid = (datetime.now().strftime('%Y%m-%d%H-%M%S-')).replace('-', '')

print(eventid)
