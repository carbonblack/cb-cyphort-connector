# Carbon Black - Cyphort Connector

Carbon Black now integrates with Cyphort for inspection, analysis and correlation of
suspicious binaries discovered at the endpoint. Now Carbon Black can submit unknown or
suspicious binaries to Cyphort Core--a secure threat analysis engine, which leverages
Cyphort's multi-method behavioral detection technology and threat intelligence--to
deliver threat scores used in Carbon Black to enhance detection, response and remediation
efforts.

The Cyphort connector submits binaries collected by Carbon Black to a Cyphort
appliance for binary analysis. The results are collected and placed into an Intelligence
Feed on your Carbon Black server. The feed will then tag any binaries executed on your
endpoints identified as malware by Cyphort. Only binaries submitted by the connector
for analysis will be included in the generated Intelligence Feed.

## Installation Quickstart

As root on your Carbon Black or other RPM based 64-bit Linux distribution server:
```
cd /etc/yum.repos.d
curl -O https://opensource.carbonblack.com/release/x86_64/CbOpenSource.repo
yum install python-cb-cyphort-connector
```

Once the software is installed via YUM, copy the `/etc/cb/integrations/cyphort/connector.conf.example` file to 
`/etc/cb/integrations/cyphort/connector.conf`. Edit this file and place your Carbon Black API key into the 
`carbonblack_server_token` variable and your Carbon Black server's base URL into the `carbonblack_server_url` variable.

Next, you will have to point the connector to the Cyphort appliance. Set the `cyphort_url` and `cyphort_api_key`
variables to the URL of the Cyphort appliance and your API key used to submit binaries.

Any errors will be logged into `/var/log/cb/integrations/cyphort/cyphort.log`.

## Troubleshooting

If you suspect a problem, please first look at the Cyphort connector logs found here: 
`/var/log/cb/integrations/cyphort/cyphort.log`
(There might be multiple files as the logger "rolls over" when the log file hits a certain size).

If you want to re-run the analysis across your binaries:

1. Stop the service: `service cb-cyphort-connector stop`
2. Remove the database file: `rm /usr/share/cb/integrations/cyphort/db/sqlite.db`
3. Remove the feed from your Cb server's Threat Intelligence page
4. Restart the service: `service cb-cyphort-connector start`

## Support

1. Use the [Developer Community Forum](https://community.carbonblack.com/t5/Developer-Relations/bd-p/developer-relations) to discuss issues and ideas with other API developers in the Carbon Black Community.
2. Report bugs and change requests through the GitHub issue tracker. Click on the + sign menu on the upper right of the screen and select New issue. You can also go to the Issues menu across the top of the page and click on New issue.
3. View all API and integration offerings on the [Developer Network](https://developer.carbonblack.com/) along with reference documentation, video tutorials, and how-to guides.
