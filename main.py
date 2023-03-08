import backend


def main():
    orgs = backend.get_orgs()

    # Counters
    x = 1
    y = 1
    z = 1

    # Get Orgs
    for i in orgs:
        print(f"{x}. {i['name']}")
        x = x + 1
    org_num = int(input("Select an organization by its number: "))
    org = orgs[org_num - 1]
    org_id = org['id']

    # Get Networks
    network = backend.get_networks(org_id)
    for i in network:
        print(f"{y}. {i['name']}")
        y = y + 1
    net_num = int(input("Select a network by its number: "))
    net = network[net_num - 1]
    net_id = net['id']

    # Get iPSK SSIDs
    my_ssids = backend.get_network_ssids(net_id)
    for i in my_ssids:
        print(f"{z}. {i['name']}")
        z = z + 1
    ssid_choice = int(input("Select the iPSK SSID by its number to apply the config: "))
    ssid = my_ssids[ssid_choice - 1]

    # apply the config
    backend.apply_ipskConfig(net_id, ssid['number'])


if __name__ == '__main__':
    main()
