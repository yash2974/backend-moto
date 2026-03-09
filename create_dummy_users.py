import requests
import json

# API endpoint
BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/api/users/register/"

# Dummy user data
dummy_users = [
    {"username": "alex_rider", "email": "alex.rider@example.com", "password": "SecurePass123!", "first_name": "Alex", "last_name": "Rider"},
    {"username": "sarah_connor", "email": "sarah.connor@example.com", "password": "SecurePass123!", "first_name": "Sarah", "last_name": "Connor"},
    {"username": "mike_jones", "email": "mike.jones@example.com", "password": "SecurePass123!", "first_name": "Mike", "last_name": "Jones"},
    {"username": "emily_stone", "email": "emily.stone@example.com", "password": "SecurePass123!", "first_name": "Emily", "last_name": "Stone"},
    {"username": "david_chen", "email": "david.chen@example.com", "password": "SecurePass123!", "first_name": "David", "last_name": "Chen"},
    {"username": "lisa_brown", "email": "lisa.brown@example.com", "password": "SecurePass123!", "first_name": "Lisa", "last_name": "Brown"},
    {"username": "james_wilson", "email": "james.wilson@example.com", "password": "SecurePass123!", "first_name": "James", "last_name": "Wilson"},
    {"username": "maria_garcia", "email": "maria.garcia@example.com", "password": "SecurePass123!", "first_name": "Maria", "last_name": "Garcia"},
    {"username": "robert_taylor", "email": "robert.taylor@example.com", "password": "SecurePass123!", "first_name": "Robert", "last_name": "Taylor"},
    {"username": "jennifer_lee", "email": "jennifer.lee@example.com", "password": "SecurePass123!", "first_name": "Jennifer", "last_name": "Lee"},
    {"username": "chris_martin", "email": "chris.martin@example.com", "password": "SecurePass123!", "first_name": "Chris", "last_name": "Martin"},
    {"username": "amanda_white", "email": "amanda.white@example.com", "password": "SecurePass123!", "first_name": "Amanda", "last_name": "White"},
    {"username": "daniel_harris", "email": "daniel.harris@example.com", "password": "SecurePass123!", "first_name": "Daniel", "last_name": "Harris"},
    {"username": "jessica_clark", "email": "jessica.clark@example.com", "password": "SecurePass123!", "first_name": "Jessica", "last_name": "Clark"},
    {"username": "kevin_rodriguez", "email": "kevin.rodriguez@example.com", "password": "SecurePass123!", "first_name": "Kevin", "last_name": "Rodriguez"},
    {"username": "laura_lewis", "email": "laura.lewis@example.com", "password": "SecurePass123!", "first_name": "Laura", "last_name": "Lewis"},
    {"username": "thomas_walker", "email": "thomas.walker@example.com", "password": "SecurePass123!", "first_name": "Thomas", "last_name": "Walker"},
    {"username": "nicole_hall", "email": "nicole.hall@example.com", "password": "SecurePass123!", "first_name": "Nicole", "last_name": "Hall"},
    {"username": "brian_young", "email": "brian.young@example.com", "password": "SecurePass123!", "first_name": "Brian", "last_name": "Young"},
    {"username": "rachel_king", "email": "rachel.king@example.com", "password": "SecurePass123!", "first_name": "Rachel", "last_name": "King"},
]

def create_users():
    successful = 0
    failed = 0
    
    print("Creating 20 dummy users...")
    print("-" * 50)
    
    for i, user_data in enumerate(dummy_users, 1):
        try:
            response = requests.post(REGISTER_URL, json=user_data)
            
            if response.status_code == 201:
                successful += 1
                print(f"✓ User {i}/20: {user_data['username']} created successfully")
            else:
                failed += 1
                print(f"✗ User {i}/20: {user_data['username']} failed - {response.json()}")
        
        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Cannot connect to {BASE_URL}")
            print("   Make sure the Django server is running (python manage.py runserver)")
            return
        except Exception as e:
            failed += 1
            print(f"✗ User {i}/20: {user_data['username']} failed - {str(e)}")
    
    print("-" * 50)
    print(f"Summary: {successful} successful, {failed} failed")
    print(f"Total users created: {successful}")

if __name__ == "__main__":
    create_users()
