import requests

r = requests.get("https://api-open.data.gov.sg/v2/real-time/api/psi")
data = r.json()
print(data)
