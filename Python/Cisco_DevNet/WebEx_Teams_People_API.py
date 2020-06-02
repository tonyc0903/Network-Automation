import os
import requests

"""
    This is a sample Python code that uses REST API to communicate with Cisco WebEx Teams and perform certain functions regarding participants
"""

def get_person(source, headers):
    
    choice = input("Enter person's email: ")
    get_person_info = requests.get(f"{source}/people?email={choice}", headers=headers)
    get_person_info.raise_for_status()
    person = get_person_info.json()


    person_id_found = None
    for person_info in person['items']:
        if choice == person_info['emails'][0]:
            print(f'Person information:')
            print(f"Person name: {person_info['firstName']}\nID: {person_info['id']}\n")
            person_id_found = person_info['id']
            break

    return person_id_found

def get_person_details(source, headers, personID):
    
    if personID:
        get_person_details_resp = requests.get(f"{source}/people/{personID}", headers=headers)
        get_person_details_resp.raise_for_status()
        person_log = get_person_details_resp.json()
        print('Person details:')
        print(f"Person name: {person_log['firstName']} {person_log['lastName']}\nEmail: {person_log['emails'][0]}\nPhone number: {person_log['phoneNumbers']}\nCreated on {person_log['created']}")


def get_your_own_details(source, headers, personID):
    get_own_info = requests.get(f"{source}/people/me", headers=headers)
    get_own_info.raise_for_status()
    own_log = get_own_info.json()

    if personID:
        print('Your details:')
        print(f"Person name: {own_log['firstName']} {own_log['lastName']}\nEmail: {own_log['emails'][0]}\nPhone number: {own_log['phoneNumbers']}\nCreated on {own_log['created']}")


def main():
    # Set the environment variable WebEx_Token with its value beforehand (I did this in Windows)
    access_token = os.environ.get('WebEx_Token')
    source = 'https://webexapis.com/v1'
    
    if not access_token:
        raise ValueError("invalid or non presnet token")
    
    # In postman, this is under Authorization->type->Bearer Token, not headers, might be confusing
    headers = {"Authorization": f"Bearer {access_token}"}

    person_Id = get_person(source, headers)
    get_person_details(source, headers, person_Id)
    get_your_own_details(source, headers, person_Id)


if __name__ == "__main__":
    main()