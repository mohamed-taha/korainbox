# Add `Get Started` button
```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "get_started": {"payload": "{\"action\": \"get_started_button\"}"}
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=<ACCESS_TOKEN>"
```