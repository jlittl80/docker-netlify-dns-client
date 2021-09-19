# netlify-dns-client
Netlify DNS updater

This is a simple script that you can use to update any record on Netlify's DNS service.

It's also only really used for dynamic home IP's. I may try to expand it into a full-fledged client.

## Usage
- ```docker build -t jlitt80/docker-netlify-dns-client  https://github.com/jlittl80/docker-netlify-dns-client.git```
- ```docker run -d --name netlify-ddns -v $(pwd)/logfolder:/logs -e NETLIFY_API_TOKEN=<API token here> -e NETLIFY_URL=web_example_io jlitt80/docker-netlify-dns-client```
This will build a local image, and run the script in a detached container.

If you want to get the logs out either:
- View the logs inside the volume externally
- Connect to the container and cat them out like ```docker exec -it netlify-ddns cat /logs/netlifydns.log```

## Future
- Better usability
## Contributions
- Fork it
- Make changes
- Submit Pull Request
- I will merge
