import requests
import argparse

if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint",       required=True,  help="Endpoint URI")
    ap.add_argument("--token",          required=True,  help="Google Identity token (gcloud auth print-identity-token)")
    ap.add_argument("--json_payload",   required=True,  help="JSON Payload for POST")
    args = vars(ap.parse_args())
    
    url = args['endpoint']
    headers = {"Authorization": f"Bearer {args['token']}"}
    
    r = requests.post(url, headers=headers, json=args['json_payload'])
    
    print(f'[ INFO ] Status Code: {r.status_code}')
    print(f'[ INFO ] Response:    {r.content}')

