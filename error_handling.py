import requests

# Try requesting:
# - A valid endpoint: `https://api.github.com/users/github`
# - An invalid endpoint: `https://api.github.com/users/DEFINITELY_NOT_A_REAL_USER_123456789`
# - A malformed URL: `https://api.github.com/this/does/not/exist`

# For each, print:
# - The status code
# - Whether the request was successful (`response.ok` is a boolean)
# - A user-friendly message based on the status code


#--------------------------- (A valid endpoint)
url = "https://api.github.com/users/github"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:    
    print("Request Successfull")
else:
    print('Source not found.')

#--------------------------- (An invalid endpoint)

url = 'https://api.github.com/users/DEFINITELY_NOT_A_REAL_USER_123456789'

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:    
    print("Request Successfull")
else:
    print('Source not found.')

#--------------------------- (A malformed URL)


url = "https://api.github.com/this/does/not/exist"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:    
    print("Request Successfull")
else:
    print('Source not found.')


