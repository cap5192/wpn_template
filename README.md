# wpn_template
This demo WPN Template script applies iPSK configuration from a CSV file to a WPN enabled SSID. 

- In order to run this script, add your Meraki API key under .env file.
- Then edit the IPSK configuration that you'd like to apply inside the WPN_Templates.csv file.
- Create group policy(es) matching the names that were used in the templates on the dashboard by going under Network-wide > Group Policy.
- Create a WPN SSID on the dashboard. More information can be found here - https://documentation.meraki.com/MR/Encryption_and_Authentication/Wi-Fi_Personal_Network_(WPN)#Configuration
- Run the script and apply the configuration to a targeted network and WPN-enabled SSID.
