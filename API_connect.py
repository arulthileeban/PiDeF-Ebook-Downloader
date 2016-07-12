from googleapiclient.discovery import build
import json

def scrap(search_term,num_requests):
    """Function to get Google search results"""
    search_term="ext:pdf "+search_term
    output_dir = ''
    output_fname='output'
    output_ext='.json'
    search_engine_id = '002418565633053671293:rwtbuojhuju'
    api_key = ' AIzaSyAfxMcI8jYYQr7ISMcnNwExD05Q7yqpAUo '
    service = build('customsearch', 'v1', developerKey=api_key)
    collection = service.cse()

    for i in range(0, num_requests):
        output_f = open(output_fname+str(i)+output_ext, 'wb')
        start_val = 1 + (i * 10)
        request = collection.list(q=search_term,num=10,start=start_val,cx=search_engine_id)
        response = request.execute()
        output = json.dumps(response, sort_keys=True, indent=2)
        output_f.write(output)
        output_f.close()
