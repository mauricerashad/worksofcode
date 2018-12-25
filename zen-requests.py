import requests
import json
import argparse

######################## Options and Help Menu ######################
usage = 'Create or update Zendesk tickets'
usage += '\nE.X.: zen-request.py -a update -t 123456 -s pending  -c "Private comment in double-quotes unless public with -p"'
parser = argparse.ArgumentParser(usage=usage)

# Mandatory flag(s)
parser.add_argument("-a", "--action", metavar='', type = str,
        help="Ticket actions: create, update, reassign, close")

# Conditional flags
parser.add_argument("-t", "--ticket_number", metavar='', type = int,
        help="Ticket number (omit when creating a new ticket)")

parser.add_argument("-s", "--status", metavar = '', type = str,
        help="Submitted ticket status: open, pending, solved. 'NEW' is the default when creating tickets with '-a create'")

parser.add_argument("-p", "--public", action='store_true',
        help="Post comment as public 'default is private comments'")

parser.add_argument("-c", "--comment", type=str, metavar='', nargs='+',
        help="\"Ticket comments\". \\n for line breaks.")

# Optional flags
parser.add_argument("-r", "--reassign", type=str, metavar='', nargs='+',
        help="Reassign the ticket: -r \"assignee or group name\"")

args = parser.parse_args()
######################## Options and Help Menu ######################

# Set the request parameters
global signature
global url
global user
global tkn


# Default error checking and formatting
if not args.action:
    print("Error: Flag '-a' or '--action' is required")
    exit(1)
elif args.action and not args.comment or not args.ticket_number:
    print("Error: Please supply values for '--ticket-number', '--comment', and '--status'")
    exit(1)
else:
    args.status = args.status.lower()
    if not args.status in {'open', 'pending', 'solved'}:
        print("Error: status must be 'open', 'pending', or 'solved'\nPlease retry")
        exit(1)
    args.action = args.action.lower()
    args.comment = ' '.join(args.comment)



# Globals and functions
def tck_update():
    sideLoad = '?include=users,groups'
    url = 'https://mauricerashad.zendesk.com/api/v2/tickets/%s.json%s' % (args.ticket_number, sideLoad)
    user = 'sysadmin@yourdomain.com/token'
    tkn = 'myLongASCIIpassword'
    headers = {'content-type': 'application/json'}
    tag = ' - Autobot'
    data = '{"ticket": {"status": "%s", "comment": {"public": "%s", "body": "%s\\n%s"}}}' % (args.status, args.public, args.comment, tag)

    query = 'type:user "maurice williams"'
    response = requests.get(url, auth=(user, tkn), data=data, headers=headers) 
    rtnData = response.json()
    new = {}
    new = str(rtnData["results"][0:1]).lstrip("[").rstrip("]")
    print(new.get("id"))
    exit()


    # Make the API call - this also sideloads users,groups in case it's needed
    global response
    response = requests.put(url, auth=(user, tkn), data=data, headers=headers) 
    rtnData = response.json()
    #print(rtnData)
    exit()

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        print(requests.get(url, auth=(user, tkn)))
        exit(2)
    else:
        print(response)
        exit()

if 'update' in args.action:
    tck_update()

# Decode the JSON response into a dictionary and use the data
data = response.json()

# Example 1: Print the name of the first group in the list
print(data)
print( 'First group = ', data['groups'][0]['name'] )

# Example 2: Print the name of each group in the list
group_list = data['groups']
for group in group_list:
    print(group['name'])

# References
# - https://help.zendesk.com/hc/en-us/articles/229136887-Making-requests-to-the-Zendesk-API (example API calls and formats)
# - https://developer.zendesk.com/rest_api/docs/core/requests (example API calls and formats)
# - https://curl.trillworks.com/#python (format curl to python's "requests" lib)
# - https://jsonformatter.curiousconcept.com/ (json format checker)
# - https://developer.zendesk.com/requests/new (test Zendesk API calls)

# Fixing Python 2.6 errors: 

# 1 - SNIMissingWarning and InsecurePlatformWarning
# https://stackoverflow.com/questions/29134512/insecureplatformwarning-a-true-sslcontext-object-is-not-available-this-prevent
# (as root) pip install pyopenssl ndg-httpsclient pyasn1

#scrap code

#The below curl command will also work to update tickets when run directly from the CLI
#curl https://mauricerashad.zendesk.com/api/v2/requests/123456.json -d '{"request": {"comment": {"body": "hello direct curl test"}}}' -v -u sysadmin@yourdomain.com/token:myLongASCIIpassword -X PUT -H "Content-Type: application/json"

