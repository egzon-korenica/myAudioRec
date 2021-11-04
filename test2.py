mydict = {'GeopoliticalEntity': ['country', 'country', 'europe', 'German', 'country'], 'Location': ['europe'], 'Person': ['Health Minister', 'Health Minister', 'we', 'their'], 'EventCommunication': ['report', 'report'], 'Facility': ['structures'], 'Organization': ['offices']}

new_dict = {}
for key, value in mydict.items():
    new_dict[key] = list(set(value))
    
#print(new_dict)

ents=[]
vals=[]
for key in new_dict.keys():
    ents.append(key)
    for i in new_dict.get(key):
        vals.append(i)
    

print(ents, vals)
