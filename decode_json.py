import json

def decode_json(no_files):
    """Function to decode json"""
    input_file='output'
    input_ext='.json'
    links=[]
    title=[]
    for i in range(0,no_files):
        with open(input_file+str(i)+input_ext) as data_file:
            data = json.load(data_file)
            for i in data["items"]:
                links.append(i["link"])
                title.append(i["title"])
    return dict(zip(title,links))
