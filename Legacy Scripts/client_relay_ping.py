import urllib.request
import urllib.error
import json

URL = "http://localhost:8021/api/v1/evaluate"

print("=== CLIENT RELAY: REQUESTING SBRM PROOF FROM LODGEIT API ===")
try:
    # 1. Attempt to query the engine for free
    req = urllib.request.Request(URL)
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    if e.code == 402:
        auth_header = e.headers.get('WWW-Authenticate')
        print(f"[SERVER RESPONSE] HTTP 402 Payment Required")
        print(f"[L402 HEADER] {auth_header}")
        
        print("\n... Simulating Lightning Network Payment (1000 sats) ...")
        print("... Payment complete. Cryptographic Preimage unlocked.\n")
        
        # 2. Extract Macaroon and combine with Preimage
        macaroon = auth_header.split('macaroon="')[1].split('"')[0]
        preimage = "00112233445566778899aabbccddeeff"
        
        print("=== CLIENT RELAY: RE-SENDING REQUEST WITH L402 PROOF ===")
        auth_token = f"L402 {macaroon}:{preimage}"
        req2 = urllib.request.Request(URL)
        req2.add_header('Authorization', auth_token)
        
        # 3. Receive the Paid Proof
        response = urllib.request.urlopen(req2)
        data = json.loads(response.read().decode())
        print(f"[SERVER RESPONSE] HTTP 200 OK")
        print(f"[SETTLEMENT] Paid {data['settlement']}")
        print("\n=== DECRYPTED PAYLOAD (EVALUATOR STDOUT) ===")
        print(data['proof_output'])