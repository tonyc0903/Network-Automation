import os
import requests
import sys

"""
    This is a sample Python code that uses REST API to communicate with Cisco WebEx Teams and perform certain functions regarding rooms (or spaces)
    and messages
"""

def get_room(source, headers):
    
    get_rooms = requests.get(f"{source}/rooms", headers=headers)
    get_rooms.raise_for_status()
    rooms = get_rooms.json()

    room_id_found = None
    room_name = input('Enter name of room: ')
    for room in rooms['items']:
        if room_name == room['title']:
            print(f'Room information:')
            print(f"Room name: {room['title']}\nID: {room['id']}\n")
            room_id_found = room['id']
            break

    return room_id_found


def post_msg(source, headers, roomID):
     
    message_text = input(f'Enter message to be posted: ')
    if roomID:
        body = {"roomId": roomID, "text": message_text}
        post_message_resp = requests.post(f"{source}/messages", headers=headers, data=body)
        post_message_resp.raise_for_status()
        log = post_message_resp.json()
        print(f"Message posted: {log['text']}\n")


def create_room(source, headers):
    
    create_room_name = input('What name do you want the room to be? ')
    body = {"title": create_room_name}
    create_room_resp = requests.post(f"{source}/rooms", headers=headers, data=body)
    create_room_resp.raise_for_status()
    print(f"Room {create_room_name} has succesfully been created\n")


def get_room_details(source, headers, roomID):

    if roomID:
        get_room_details_resp = requests.get(f"{source}/rooms/{roomID}", headers=headers)
        get_room_details_resp.raise_for_status()
        log = get_room_details_resp.json()
        print('Room details:')
        print(f"Room name: {log['title']}\n")


def get_room_meeting_details(source, headers, roomID):
    
    if roomID:
        get_room_meeting_details_resp = requests.get(f"{source}/rooms/{roomID}/meetingInfo", headers=headers)
        get_room_meeting_details_resp.raise_for_status()
        log = get_room_meeting_details_resp.json()
        print('Room meeting details:')
        print(f"Room name: {log['meetingLink']}\nSIP Address: {log['sipAddress']}\nmeetingNumber: {log['meetingNumber']}\n")


def update_room_details(source, headers, roomID):

    update_room_name = input('Enter the new room name you wish to update to: ')
    if roomID:
        body = {"title": update_room_name }
        get_room_details_resp = requests.put(f"{source}/rooms/{roomID}", headers=headers, data=body)
        get_room_details_resp.raise_for_status()
        log = get_room_details_resp.json()
        print(f"Room name has been succesffuly updated to {log['title']}\n")


def delete_room(source, headers, roomID):
    
    #Ask user for input if they want to delete the room
    confirm = input('Are you sure about deleting this room? (y/n):')
    if confirm == 'y':
        del_room_resp = requests.delete(f"{source}/rooms/{roomID}", headers=headers)
        del_room_resp.raise_for_status()
        print(f"Successfully deleted the room!\n")
        
    else:
        print("You changed your mind? Come on man!\n")
        

def main():
    # Set the environment variable WebEx_Token with its value beforehand (I did this in Windows)
    access_token = os.environ.get('WebEx_Token') 
    source = 'https://webexapis.com/v1'
    
    if not access_token:
        raise ValueError("invalid or non presnet token")
    
    # In postman, this is under Authorization->type->Bearer Token, not headers, might be confusing
    headers = {"Authorization": f"Bearer {access_token}"}
    room_Id = get_room(source, headers)

    isTrue = True
    while(isTrue):
        
        if room_Id is not None:
            print("Please type the number that corresponds to the action you want to perform on the room\n"\
                "1. Post message\n2. Create_room\n3. Update room\n4. Get room details\n5. Get room meeting details\n6. Delete room\n7. Exit\n")
            input_ans = int(input("Your input: "))
            
            if input_ans == 1:
                post_msg(source, headers, room_Id)
            elif input_ans == 2:
                create_room(source, headers)
            elif input_ans == 3:
                update_room_details(source, headers, room_Id)
            elif input_ans == 4:
                get_room_details(source, headers, room_Id)
            elif input_ans == 5:
                get_room_meeting_details(source, headers, room_Id)
            elif input_ans == 6:
                delete_room(source, headers, room_Id)
            elif input_ans == 7:
                sys.exit(1)
            else:
                print('Invalid input')
        else:
            print('No such room exist! Try again!')
            room_Id = get_room(source, headers)

if __name__ == "__main__":
    main()