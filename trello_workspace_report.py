import requests
import csv
from datetime import datetime
import argparse

BASE_URL = "https://api.trello.com/1"
HEADERS = {"Accept": "application/json"}

def get_workspace_boards(api_key, api_token, workspace_url):
    """Get all boards in a Trello workspace"""
    workspace_name = workspace_url.split('/w/')[-1].split('/')[0]
    
    # Workspace ID
    org_url = f"{BASE_URL}/organizations/{workspace_name}"
    query = {'key': api_key, 'token': api_token}
    
    response = requests.get(org_url, headers=HEADERS, params=query)
    if response.status_code != 200:
        raise Exception(f"Error fetching workspace: {response.text}")
    
    org_id = response.json()['id']
    
    # Board Scrap
    boards_url = f"{BASE_URL}/organizations/{org_id}/boards"
    query = {
        'key': api_key,
        'token': api_token,
        'fields': 'name,url,dateLastActivity',
        'lists': 'none'
    }
    
    response = requests.get(boards_url, headers=HEADERS, params=query)
    if response.status_code != 200:
        raise Exception(f"Error fetching boards: {response.text}")
    
    return response.json()

def get_board_members(api_key, api_token, board_id):
    """Get all members of a Trello board with their roles"""
    members_url = f"{BASE_URL}/boards/{board_id}/members"
    query = {
        'key': api_key,
        'token': api_token,
        'fields': 'fullName,username',
        'member_fields': 'fullName,username'
    }
    
    response = requests.get(members_url, headers=HEADERS, params=query)
    if response.status_code != 200:
        raise Exception(f"Error fetching board members: {response.text}")
    
    # Get member roles
    memberships_url = f"{BASE_URL}/boards/{board_id}/memberships"
    response_memberships = requests.get(memberships_url, headers=HEADERS, params=query)
    if response_memberships.status_code != 200:
        raise Exception(f"Error fetching board memberships: {response_memberships.text}")
    
    memberships = response_memberships.json()
    
    # Combine member info with roles
    members_with_roles = []
    for member in response.json():
        for membership in memberships:
            if membership['idMember'] == member['id']:
                members_with_roles.append({
                    'id': member['id'],
                    'fullName': member['fullName'],
                    'username': member['username'],
                    'role': membership['memberType']
                })
                break
    
    return members_with_roles

def generate_report(api_key, api_token, workspace_url, output_file):
    """Generate CSV report of boards and their members"""
    print(f"Fetching boards for workspace: {workspace_url}")
    boards = get_workspace_boards(api_key, api_token, workspace_url)
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow([
            'Board Name', 
            'Board Link', 
            'Last Activity', 
            'Member Username', 
            'Member Full Name', 
            'Member Role'
        ])
        
        for board in boards:
            print(f"Processing board: {board['name']}")
            board_id = board['id']
            board_link = f"https://trello.com/b/{board_id}"
            
            try:
                members = get_board_members(api_key, api_token, board_id)
                
                if not members:
                    # Write board info even if no members
                    writer.writerow([
                        board['name'],
                        board_link,
                        board['dateLastActivity'],
                        '', '', ''
                    ])
                else:
                    for member in members:
                        writer.writerow([
                            board['name'],
                            board_link,
                            board['dateLastActivity'],
                            member['username'],
                            member['fullName'],
                            member['role']
                        ])
            except Exception as e:
                print(f"Error processing board {board['name']}: {str(e)}")
                # Write board info with error message
                writer.writerow([
                    board['name'],
                    board_link,
                    board['dateLastActivity'],
                    'ERROR',
                    str(e),
                    ''
                ])
    
    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Trello workspace report')
    parser.add_argument('--key', required=True, help='Trello API key')
    parser.add_argument('--token', required=True, help='Trello API token')
    parser.add_argument('--workspace', required=True, help='Trello workspace URL (e.g., https://trello.com/w/testbutler5)')
    parser.add_argument('--output', default='trello_report.csv', help='Output CSV file name')
    
    args = parser.parse_args()
    
    generate_report(args.key, args.token, args.workspace, args.output)
