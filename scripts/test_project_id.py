
import json

with open(
    "secrets/gate-pass-system-9a932-firebase-adminsdk-fbsvc-6574629762.json",
    "r"
) as file:
    data = json.load(file)

print("Project ID:", data["project_id"])