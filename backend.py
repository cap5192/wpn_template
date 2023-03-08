import meraki
import os
from dotenv import load_dotenv
import json
import pandas as pd

file_name = 'WPN_Template.csv'

# load all environment variables
load_dotenv()


def get_orgs():
    """Gets the list of all orgs (name and id) that admin has access to"""
    orgs = []
    dict = {"id": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizations()

    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        orgs.append(dict)
        dict = {"id": "", "name": ""}

    return orgs


def get_networks(org_id):
    """Get a list of networks and returns dict with net IDs and names"""
    nets = []
    dict = {"id": "", "name": ""}
    # collect network names
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all'
    )
    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        nets.append(dict)
        dict = {"id": "", "name": ""}

    return nets


def get_network_ssids(network_id):
    """Returns IPSK SSID number and Name dictionary"""
    ipsk_ssids = []
    dict = {"number": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.wireless.getNetworkWirelessSsids(
        network_id
    )
    for i in response:
        if i['authMode'] == "ipsk-without-radius":
            dict["number"] = i["number"]
            dict["name"] = i["name"]
            ipsk_ssids.append(dict)
            dict = {"number": "", "name": ""}

    return ipsk_ssids


def get_groupPolicies(network_id):
    """Returns group policy id and name"""
    groupPolicies = []
    dict = {"id": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)

    response = dashboard.networks.getNetworkGroupPolicies(
        network_id
    )
    for i in response:
        dict["id"] = i["groupPolicyId"]
        dict["name"] = i["name"]
        groupPolicies.append(dict)
        dict = {"id": "", "name": ""}

    return groupPolicies


def apply_ipskConfig(network_id, ssid_num):
    """Applies the configuration of IPSK using a CSV File"""
    flag = False
    # Reads csv file
    df = pd.read_csv(file_name)

    config = []
    # store csv data into a list
    for index, rows in df.iterrows():
        my_list = [rows.IPSK_Name, rows.Passphrase, rows['Group Policy']]
        config.append(my_list)

    group_policies = get_groupPolicies(network_id)

    #replaces group policy name to its group policy ID
    #code runs only if group policy exists on the network
    group_policy_names = []
    for i in group_policies:
        group_policy_names.append(i['name'])

    for i in config:
        if i[2] in group_policy_names:
            for x in group_policies:
                if i[2] == x['name']:
                    i[2] = x['id']
        else:
            print("One of the group policy from the template does not exist on the network")
            flag = True

    #apply the configuration
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)

    count = 1
    if not flag:
        for i in config:
            network_id = network_id
            number = ssid_num
            name = i[0]
            group_policy_id = i[2]

            response = dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id, number, name, group_policy_id,
                passphrase=i[1]
            )
            print(f"iPSK created - {count}")
            count = count + 1