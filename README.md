# netlify-dns-client
Netlify DNS updater

This is a simple script that you can use to update the 'A' record on Netlify's DNS service.

The primary use for this is running on a raspberry pi (Debian Stretch). It's also only really used for dynamic home IP's. I may try to expand it into a full-fledged client.

## Usage
- ```export NETLIFY_API_TOKEN="<YOUR_TOKEN>"```
- ```export NETLIFY_URL="www.example.com"```
- Run the script. You can also run it as cron job.

## Future
- Expand the client to support more domains other than ```.com```
- Add ability for CNAME, MX records etc.
- Better usability
## Contributions
- Fork it
- Make changes
- Submit Pull Request
- I will merge
