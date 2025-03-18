import requests

ROBLOSECURITY_COOKIE = ("Your Roblox Cookie: ")

HEADERS = {
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY_COOKIE}",
    "Content-Type": "application/json",
    "User-Agent": "RobloxGroupLeaveScript"
}

def get_csrf_token():
    response = requests.post("https://auth.roblox.com/v2/logout", headers=HEADERS)
    if "x-csrf-token" in response.headers:
        return response.headers["x-csrf-token"]
    else:
        print("Failed to get X-CSRF-TOKEN. Check your cookie.")
        return None

def get_user_id():
    response = requests.get("https://users.roblox.com/v1/users/authenticated", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("Failed to get User ID. Check your cookie.")
        return None

def get_groups(user_id):
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Failed to get groups. Status:", response.status_code)
        return []

def leave_group(group_id, csrf_token):
    url = f"https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}"
    headers = HEADERS.copy()
    headers["X-CSRF-TOKEN"] = csrf_token

    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Successfully left group ID: {group_id}")
    else:
        print(f"Failed to leave group ID: {group_id}. Status: {response.status_code} - Response: {response.text}")

csrf_token = get_csrf_token()
if csrf_token:
    user_id = get_user_id()
    if user_id:
        groups = get_groups(user_id)
        if groups:
            print(f"Found {len(groups)} groups. Leaving them now...")
            for group in groups:
                leave_group(group["group"]["id"], csrf_token)
        else:
            print("You are not in any groups!")
    else:
        print("Could not retrieve user information.")
else:
    print("Could not get CSRF token. Try again.")

