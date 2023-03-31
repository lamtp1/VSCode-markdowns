import requests

# array of people names
names = ['a', 'b', 'c']

# call the API
response = requests.get('https://example.com/api')

# parse the response
json_response = response.json()

# loop through the response and check if each name in the array is present
for person in json_response:
    if person['name'] in names:
        print(f"{person['name']} is present in the response")
