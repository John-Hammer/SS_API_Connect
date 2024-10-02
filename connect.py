import requests, json, os
from dotenv import load_dotenv

load_dotenv()

# Step 1: Obtain the access token
url = "https://schoolsoft-api-ee9752799b47.herokuapp.com/api/token/"
data = {
    "username": os.environ.get('ATEA_USER_NAME'),
    "password": os.environ.get('ATEA_USER_PASSWORD')
}

response = requests.post(url, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Content: {response.text}")

if response.status_code == 200:
    try:
        tokens = response.json()
        access_token = tokens['access']
        print(f"Access Token: {access_token}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("Response content is not valid JSON")
        exit()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()

# Step 2: Use the access token to make authenticated requests
headers = {
    "Authorization": f"Bearer {access_token}"
}

def get_all_staff(url, headers):
    all_staff = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                all_staff.extend(data)
                url = None  # No pagination, we're done
            elif 'results' in data:
                all_staff.extend(data['results'])
                url = data.get('next')  # Get the next page URL if it exists
            else:
                print("Unexpected data structure in the response")
                return None
        else:
            print(f"Error fetching staff: {response.status_code}")
            print(response.text)
            return None
    return all_staff

staff_url = "https://schoolsoft-api-ee9752799b47.herokuapp.com/api/staff/"
all_staff = get_all_staff(staff_url, headers)

if all_staff is not None:
    # Save all staff data to a JSON file with proper encoding
    with open('all_staff.json', 'w', encoding='utf-8') as f:
        json.dump(all_staff, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully extracted {len(all_staff)} staff members to all_staff.json")
    
    # Optionally, print the first few staff members
    print("\nFirst few staff members:")
    print(json.dumps(all_staff[:3], ensure_ascii=False, indent=2))
else:
    print("Failed to retrieve staff data")

# Optionally, you can also print the total number of staff members
print(f"\nTotal number of staff members: {len(all_staff)}")