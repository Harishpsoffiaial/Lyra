import sqlite3

# Connect to the Lyra database
conn = sqlite3.connect('lyra.db')
cursor = conn.cursor()

# List of website names and URLs
websites = [
    ("GitHub", "https://github.com/"),
    ("GitLab", "https://gitlab.com/"),
    ("Bitbucket", "https://bitbucket.org/"),
    ("Stack Overflow", "https://stackoverflow.com/"),
    ("Reddit", "https://www.reddit.com/"),
    ("Quora", "https://www.quora.com/"),
    ("Medium", "https://medium.com/"),
    ("Substack", "https://substack.com/"),
    ("Tumblr", "https://www.tumblr.com/"),
    ("Pinterest", "https://www.pinterest.com/"),
    ("Instagram", "https://www.instagram.com/"),
    ("Twitter", "https://twitter.com/"),
    ("Facebook", "https://www.facebook.com/"),
    ("LinkedIn", "https://www.linkedin.com/"),
    ("Snapchat", "https://www.snapchat.com/"),
    ("TikTok", "https://www.tiktok.com/"),
    ("WhatsApp", "https://www.whatsapp.com/"),
    ("Skype", "https://www.skype.com/"),
    ("Zoom", "https://zoom.us/"),
    ("Slack", "https://slack.com/"),
    ("Discord", "https://discord.com/"),
    ("Telegram", "https://telegram.org/"),
    ("WeChat", "https://www.wechat.com/"),
    ("Viber", "https://www.viber.com/"),
    ("Signal", "https://signal.org/"),
    ("Microsoft Teams", "https://www.microsoft.com/en-us/microsoft-teams/group-chat-software"),
    ("Google Meet", "https://meet.google.com/"),
    ("GoToMeeting", "https://www.goto.com/meeting"),
    ("Webex", "https://www.webex.com/"),
    ("BlueJeans", "https://www.bluejeans.com/"),
    ("Trello", "https://trello.com/"),
    ("Asana", "https://asana.com/"),
    ("Basecamp", "https://basecamp.com/"),
    ("Notion", "https://www.notion.so/"),
    ("Monday.com", "https://monday.com/"),
    ("Airtable", "https://airtable.com/"),
    ("ClickUp", "https://clickup.com/"),
    ("Jira", "https://www.atlassian.com/software/jira"),
    ("Zapier", "https://zapier.com/"),
    ("IFTTT", "https://ifttt.com/"),
    ("Integromat", "https://www.make.com/"),
    ("HubSpot", "https://www.hubspot.com/"),
    ("Salesforce", "https://www.salesforce.com/"),
    ("Zendesk", "https://www.zendesk.com/"),
    ("Freshdesk", "https://freshdesk.com/"),
    ("Pipedrive", "https://www.pipedrive.com/"),
    ("Intercom", "https://www.intercom.com/"),
    ("Zoho CRM", "https://www.zoho.com/crm/"),
    ("Mailchimp", "https://mailchimp.com/"),
    ("Constant Contact", "https://www.constantcontact.com/"),
    ("SendGrid", "https://sendgrid.com/"),
    ("ConvertKit", "https://convertkit.com/"),
    ("ActiveCampaign", "https://www.activecampaign.com/"),
    ("GetResponse", "https://www.getresponse.com/"),
    ("Drip", "https://www.drip.com/"),
    ("OptinMonster", "https://optinmonster.com/"),
    ("Unbounce", "https://unbounce.com/"),
    ("Instapage", "https://www.instapage.com/"),
    ("Leadpages", "https://www.leadpages.net/"),
    ("ClickFunnels", "https://www.clickfunnels.com/"),
    ("Shopify", "https://www.shopify.com/"),
    ("BigCommerce", "https://www.bigcommerce.com/"),
    ("WooCommerce", "https://woocommerce.com/"),
    ("Squarespace", "https://www.squarespace.com/"),
    ("Wix", "https://www.wix.com/"),
    ("Weebly", "https://www.weebly.com/"),
    ("WordPress", "https://wordpress.com/"),
    ("GoDaddy", "https://www.godaddy.com/"),
    ("Bluehost", "https://www.bluehost.com/"),
    ("HostGator", "https://www.hostgator.com/"),
    ("DreamHost", "https://www.dreamhost.com/"),
    ("SiteGround", "https://www.siteground.com/"),
    ("A2 Hosting", "https://www.a2hosting.com/"),
    ("InMotion Hosting", "https://www.inmotionhosting.com/"),
    ("Liquid Web", "https://www.liquidweb.com/"),
    ("Kinsta", "https://kinsta.com/"),
    ("WP Engine", "https://wpengine.com/"),
    ("Cloudways", "https://www.cloudways.com/"),
    ("Amazon Web Services", "https://aws.amazon.com/"),
    ("Google Cloud", "https://cloud.google.com/"),
    ("Microsoft Azure", "https://azure.microsoft.com/"),
    ("IBM Cloud", "https://www.ibm.com/cloud"),
    ("DigitalOcean", "https://www.digitalocean.com/"),
    ("Heroku", "https://www.heroku.com/"),
    ("Linode", "https://www.linode.com/"),
    ("Vultr", "https://www.vultr.com/"),
    ("Alibaba Cloud", "https://www.alibabacloud.com/"),
    ("Oracle Cloud", "https://cloud.oracle.com/"),
    ("Salesforce", "https://www.salesforce.com/"),
    ("HubSpot", "https://www.hubspot.com/"),
    ("Zoho CRM", "https://www.zoho.com/crm/"),
    ("Pipedrive", "https://www.pipedrive.com/"),
    ("Freshsales", "https://freshsales.io/"),
    ("Intercom", "https://www.intercom.com/"),
    ("Zendesk", "https://www.zendesk.com/"),
    ("Freshdesk", "https://freshdesk.com/"),
    ("ServiceNow", "https://www.servicenow.com/"),
    ("ClickUp", "https://clickup.com/"),
    ("Monday.com", "https://monday.com/"),
    ("Airtable", "https://airtable.com/"),
    ("ClickFunnels", "https://www.clickfunnels.com/"),
    ("Leadpages", "https://www.leadpages.net/"),
]



# Insert the data into the web_command table
cursor.executemany('''
INSERT INTO web_command (name, url) VALUES (?, ?)
''', websites)

# Commit the transaction
conn.commit()

# Verify the data has been inserted
cursor.execute('SELECT * FROM web_command')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
