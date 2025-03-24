import requests

BASE_URL = "https://30d1-129-205-124-243.ngrok-free.app/api/recommend/"

def get_recommendations(liked_course):
    try:
        payload = {"liked_course": liked_course}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token 9bb628049b95f9b7feef7ed68cf3d178284ea0ca"
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json().get("recommended_courses", [])
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
