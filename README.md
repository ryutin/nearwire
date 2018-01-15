# NearWire

Local News Skill
nearwire.co

## Getting Started

Returns headlines from a given location, by default the location of
the alexa.  But other locations can be specified on demand.

### Prerequisites

1. Alexa has the local info
https://developer.amazon.com/docs/custom-skills/device-address-api.html
2. Use WebHose API to get local news headlines
   (http://webhose.io/broadcast-api and  http://webhose.io/web-content-api)

```
 curl --get --include 'http://webhose.io/broadcastFilter?token=<webhose_token>&format=json&q=location%3Amaryland%20location%3Akensington' \
        -H 'Accept: text/plain'
 curl --get --include 'http://webhose.io/filterWebContent?token=<webhose_token>&format=json&sort=crawled&q=location%3Amaryland%20location%3Akensington' \
        -H 'Accept: text/plain'
```
3. Create schema with webhose.io included

4. How it works
- When the NearWire skill is invoked, check if the news was cached for
   that day.
- If not, generate web call from webhose.io and store data in
  database.
- Data is stored initially once each day.
- Aggregation count is used to determine the order of the headlines.
