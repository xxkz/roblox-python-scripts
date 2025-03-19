import requests

ROBLOSECURITY_COOKIE = "COOKIE"
NEW_BIO = input("Your new bio: ")

UPDATE_BIO_URL = "https://accountinformation.roblox.com/v1/description"

headers = {
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY_COOKIE}",
    "Content-Type": "application/json",
    "Referer": "https://www.roblox.com",
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
csrf_request = session.post(UPDATE_BIO_URL, headers=headers)
csrf_token = csrf_request.headers.get("x-csrf-token")

if not csrf_token:
    print("Failed to retrieve X-CSRF-TOKEN. Ensure your cookie is valid.")
    exit()

headers["X-CSRF-TOKEN"] = csrf_token

response = session.post(UPDATE_BIO_URL, headers=headers, json={"description": NEW_BIO})

if response.status_code == 200:
    print("Successfully updated bio!")
else:
    print(f"Failed to update bio. Status code: {response.status_code}, Response: {response.text}")
