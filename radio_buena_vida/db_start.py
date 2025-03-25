import requests
from decouple import config

# Load Dropbox credentials
APP_KEY = config("DROPBOX_APP_KEY")
APP_SECRET = config("DROPBOX_APP_SECRET")
REDIRECT_URI = config("DROPBOX_REDIRECT_URI")

# Manually generate the auth URL
auth_url = f"https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&fromDws=True&response_type=code&redirect_uri={REDIRECT_URI}"
print("1. Go to the following URL to authenticate:")
print(auth_url)
print("2. Click 'Allow' and then copy the authorization code.")

# Get the authorization code from the user
auth_code = input("3. Enter the authorization code here: ")

# Prepare the data for the POST request to exchange the code for an access token
token_url = "https://api.dropbox.com/oauth2/token"
token_data = {
    "code": auth_code,
    "grant_type": "authorization_code",
    "client_id": APP_KEY,
    "client_secret": APP_SECRET,
    "redirect_uri": REDIRECT_URI  # Add your redirect URI here if it's used
}

# Make the POST request to exchange the authorization code for an access token
response = requests.post(token_url, data=token_data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON and get the access token
    token_info = response.json()
    access_token = token_info["access_token"]
    print("Access token:", access_token)
else:
    print("Error getting access token:", response.status_code, response.text)
