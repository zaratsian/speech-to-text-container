import requests
import argparse

def get_google_identity_token():
    try:
        import google.auth
        import google.auth.transport.requests
        creds, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        return creds.token
    except Exception as e:
        print(f'[ EXCEPTION ] {e}')

if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint",       required=True,  help="Endpoint URI")
    #ap.add_argument("--token",          required=True,  help="Google Identity token (gcloud auth print-identity-token)")
    ap.add_argument("--json_payload",   required=True,  help="JSON Payload for POST")
    args = vars(ap.parse_args())
    
    # Get Google Identity Token
    token = get_google_identity_token()
    
    url = args['endpoint']
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f'''[ INFO ] Endpoint:      {url}''')
    print(f'''[ INFO ] Token:         {token}''')
    print(f'''[ INFO ] Payload Type:  {type(args['json_payload'])}''')
    print(f'''[ INFO ] Payload:       {args['json_payload']}''')
    
    r = requests.post(url, headers=headers, json=args['json_payload'])
    
    print(f'[ INFO ] Status Code: {r.status_code}')
    print(f'[ INFO ] Response:    {r.content}')

