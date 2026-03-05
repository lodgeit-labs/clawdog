import http.server
import socketserver
import json
import subprocess

PORT = 8021
MOCK_MACAROON = "AgEEbHNhdA_LodgeiT_Gateway_Token_x9f"
MOCK_INVOICE = "lnbc10u1p3j...[Lightning_Invoice]...000sats"
VALID_PREIMAGE = "00112233445566778899aabbccddeeff"

class L402Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v1/evaluate':
            auth_header = self.headers.get('Authorization')
            
            # Step 1: Intercept unauthenticated requests and issue Lightning Invoice
            if not auth_header or not auth_header.startswith('L402'):
                self.send_response(402)
                self.send_header('WWW-Authenticate', f'L402 macaroon="{MOCK_MACAROON}", invoice="{MOCK_INVOICE}"')
                self.end_headers()
                self.wfile.write(b'{"error": "Payment Required", "cost": "1000 sats"}')
                print("\n[L402 GATEWAY] 402 Payment Required - Lightning Invoice Issued.")
                return

            # Step 2: Validate the cryptographic preimage
            parts = auth_header.split(' ')
            if len(parts) == 2:
                token = parts[1]
                try:
                    macaroon, preimage = token.split(':')
                except ValueError:
                    self.send_error(400, "Malformed L402 Token")
                    return
                
                if macaroon == MOCK_MACAROON and preimage == VALID_PREIMAGE:
                    print("\n[L402 GATEWAY] Cryptographic Payment Verified (1000 Sats).")
                    print("[L402 GATEWAY] Booting SWI-Prolog Engine for Proof Execution...")
                    
                    # Execute the deterministic logic engine
                    result = subprocess.run(['python', 'evaluate_oim_report.py'], capture_output=True, text=True)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    payload = {
                        "status": "success",
                        "settlement": "1000 sats",
                        "proof_output": result.stdout
                    }
                    self.wfile.write(json.dumps(payload).encode())
                    return
                    
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized / Invalid Lightning Preimage"}')

print(f"=== LODGEIT GLOBAL: L402 PAYMENT GATEWAY ONLINE (Port {PORT}) ===")
print("Awaiting ClientRelay requests...")
with socketserver.TCPServer(("", PORT), L402Handler) as httpd:
    httpd.serve_forever()