import requests

common_codes = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden - You're not allowed to access this",
    404: "Not Found - That resource doesn't exist",
    429: "Too Many Requests - You're making requests too fast",
    500: "Internal Server Error - Something broke on the server",
    503: "Service Unavailable - Server is down or overloaded"
}


#--------------------------- (A valid endpoint)
url = "https://api.github.com/users/github"

response = requests.get(url)

# response.ok boolean indicates true or false if code is in range 200-299
print("\nRequest for: https://api.github.com/users/github")
if response.ok == True:
    print(f'Status Code: {response.status_code}')  
    print('Request successful. ')
else:    
    print(f'Request Failed. Status Code: {response.status_code} {common_codes[response.status_code]}')

#--------------------------- (An invalid endpoint)

url = 'https://api.github.com/users/DEFINITELY_NOT_A_REAL_USER_123456789'

response = requests.get(url)

print('\nRequest for: https://api.github.com/users/DEFINITELY_NOT_A_REAL_USER_123456789')
if response.ok == True:
    print(f'Status Code: {response.status_code}')    
    print('Request successful.')
else:    
    print(f'Request Failed. Status Code: {response.status_code} {common_codes[response.status_code]}')

#--------------------------- (A malformed URL)


url = "https://api.github.com/this/does/not/exist"

response = requests.get(url)
print("\nRequest for: https://api.github.com/this/does/not/exist")
if response.ok == True:
    print(f'Status Code: {response.status_code}')     
    print('Request successful.')
else:
    print(f'Request Failed. Status Code: {response.status_code} {common_codes[response.status_code]}')


