import requests

# Your specific LodgeiT sandbox credentials
CLIENT_ID = "0dVauzHG3eUWpBGLxcHeDhi2lvsD"
CLIENT_SECRET = "603db72b-2d30-4e49-8257-a929bcac06fd"
REDIRECT_URI = "http://localhost:8080"

# The code you just grabbed from the browser
AUTHORIZATION_CODE = "930487ed96af4de9bfbf0f351624e461"

def get_access_token():
    """Exchanges the authorization code for an OAuth 2.0 access token."""
    token_url = "https://test-api.service.hmrc.gov.uk/oauth/token"
    
    # Send parameters in the request body
    payload = {
        "client_secret": CLIENT_SECRET,
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": AUTHORIZATION_CODE
    }
    
    response = requests.post(token_url, data=payload)
    response.raise_for_status() 
    return response.json().get("access_token")

def test_hello_user(access_token):
    """Calls the user-restricted API using the new access token."""
    api_url = "https://test-api.service.hmrc.gov.uk/hello/user"
    
    # Use the token in the Authorization header
    headers = {
        "Accept": "application/vnd.hmrc.1.0+json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(api_url, headers=headers)
    
    print("\n--- API Result ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("------------------\n")

if __name__ == "__main__":
    try:
        print("Requesting access token...")
        token = get_access_token()
        print(f"Success! Access Token retrieved.")
        
        print("Calling Hello User API...")
        test_hello_user(token)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")