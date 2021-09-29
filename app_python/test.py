import requests
import argparse
import json

if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint",       required=True,  help="Endpoint URI")
    ap.add_argument("--token",          required=True,  help="Google Identity token (gcloud auth print-identity-token)")
    ap.add_argument("--json_payload",   required=True,  help="JSON (as STRING type)")
    args = vars(ap.parse_args())
    
    url = args['endpoint']
    headers = {"Authorization": f"Bearer {args['token']}"}
    
    print(f'[ INFO ] Headers: {headers}')
    print(f'[ INFO ] URL:     {url}')
    
    payload = json.loads(args['json_payload'])
    print(f'[ INFO ] Payload Type: {type(payload)}')
    print(f'[ INFO ] Payload:      {payload}')
    
    r = requests.post(url, headers=headers, json=payload)
    
    print(f'[ INFO ] Status Code:  {r.status_code}')
    print(f'[ INFO ] Response:     {r.content}')

