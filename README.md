Facebook Message Scraper
========================

## Usage
```
python dumper.py {id} {chunk} < {headerfile}
```

Where `id` is the Facebook user id for which you want to download messages, `chunk` is the ≈2000 amount of messages to download at a time, and `headerfile` is the filename of the header file downloaded as per the **Details** section below.

## Details
Forked from [RaghavSood](https://github.com/RaghavSood/FBMessageScraper), but updated to use @tomer8007's [fix for timestamps](https://github.com/RaghavSood/FBMessageScraper/issues/3#issuecomment-168302782), and then **further** updated to allow you pass in a header, copied and pasted from the Facebook devtools console, in stdin. See instructions below for (simple) details!

1. In Chrome, open [facebook.com/messages](https://www.facebook.com/messages/) and open any conversation with a fair number of messages
2. Open the network tab of the Chrome Developer tools
3. Scroll up in the conversation until the page attempts to load previous messages
4. Look for the POST request to [thread\_info.php](https://www.facebook.com/ajax/mercury/thread_info.php)
5. Click and drag to copy *everything* inside the `Headers` pane. Paste this into a file. Save this as some filename you'll remember, such as `header`.
6. Run `python dumper.py {id} {chunk size} < header`, where `id` can be found using the instructions below, and chunk size is the size of JSON file to download (2000 is a good default).

![image](https://cloud.githubusercontent.com/assets/693511/16968876/74d3cab4-4ddf-11e6-9b97-fb6827bcc6ee.png)


## Getting a User's ID

1. Get the conversation ID for those messages by opening [http://graph.facebook.com/{username-of-chat-partner}](http://graph.facebook.com/{username_of_chat_partner})
2. Copy the `id` value from there

If that doesn't work, you can also check the secondary index of line ~48 in your headers file (should start with `messages[user_ids]`).

Messages are saved by default to `Messages/{id}/`
