from requests import get

data = get("http://localhost:3689/api/outputs").json()
print("Id                   Name")
print("--                   ----")
for item in data["outputs"]:
    id = item["id"]
    name = item["name"]
    print(f"{id:<20} {name}")

