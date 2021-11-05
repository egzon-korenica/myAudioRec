args = [{'text': 'country', 'location': [30, 37], 'entities': [{'type': 'GeopoliticalEntity', 'text': 'country', 'disambiguation': {'subtype': ['Country']}}]}, {'text': 'south', 'location': [41, 46], 'entities': [{'type': 'Location', 'text': 'europe'}]}]

for arg in args:
    print(arg[str(list(arg.keys())[0])])
    
