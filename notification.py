"""
Daily notification system for the Verb-End Torture Chamber.

Approach for iMessage delivery:
1. Cron job (Render cron / GitHub Actions) hits /api/daily/send each morning
2. That prepares the daily message
3. An Apple Shortcut on your iPhone polls /api/daily and sends iMessage to yourself

Setup options:
A) Apple Shortcuts Automation (recommended, free, no Mac needed)
B) Mac-based AppleScript automation
C) Pushcut webhook (free tier available)

See setup_imessage() for instructions.
"""

import os
import json
from datetime import date, time


def get_daily_payload(base_url):
    """Generate the daily notification payload."""
    from sentences import get_daily_sentence
    from database import store_daily_message, get_daily_message

    today = date.today().isoformat()
    msg = get_daily_message(today)

    if not msg:
        template = get_daily_sentence()
        store_daily_message(today, template["text"])
        msg = {"sentence_text": template["text"], "message_date": today}

    sentence = msg["sentence_text"] if isinstance(msg, dict) else str(msg)

    return {
        "date": today,
        "sentence": sentence,
        "exercise_url": f"{base_url}/exercise",
        "imessage_text": (
            f"Verb-End Torture Chamber\n\n"
            f"Heute: {sentence}\n\n"
            f"Kannst du das Verb richtig platzieren?\n"
            f"{base_url}/exercise"
        )
    }


SHORTCUTS_SETUP = """
═══════════════════════════════════════════════════════════════
  iMessage Daily Notification Setup — Apple Shortcuts Method
═══════════════════════════════════════════════════════════════

This approach uses the free Apple Shortcuts app on your iPhone.
No Mac required. Runs automatically each morning.

STEP 1: Create the Shortcut
─────────────────────────────
1. Open the Shortcuts app on your iPhone
2. Tap "+" to create a new shortcut
3. Name it "German Verb Exercise"
4. Add these actions in order:

   a) "Get Contents of URL"
      URL: {base_url}/api/daily
      Method: GET

   b) "Get Dictionary Value"
      Key: "message"
      From: Contents of URL

   c) "Send Message"
      To: [your phone number or your own contact]
      Message: Dictionary Value

STEP 2: Set Up Daily Automation
─────────────────────────────────
1. Go to Shortcuts > Automation tab
2. Tap "+" > "Create Personal Automation"
3. Choose "Time of Day"
4. Set to your preferred morning time (e.g., 7:00 AM)
5. Repeat: Daily
6. Add action: "Run Shortcut" > select "German Verb Exercise"
7. Turn OFF "Ask Before Running"
8. Done!

The shortcut will:
- Fetch today's sentence from your app
- Send it to you as an iMessage
- Include the exercise link
══════════════════════════════════════════════════════════════
"""


MAC_APPLESCRIPT_SETUP = """
═══════════════════════════════════════════════════════════════
  iMessage Daily Notification Setup — Mac AppleScript Method
═══════════════════════════════════════════════════════════════

If you have a Mac that's always on, you can use this approach.

1. Save this as ~/german_notify.sh:

   #!/bin/bash
   MSG=$(curl -s {base_url}/api/daily | python3 -c "import sys,json; print(json.load(sys.stdin)['message'])")

   osascript -e '
   tell application "Messages"
       set targetService to 1st account whose service type = iMessage
       set targetBuddy to participant "{phone}" of targetService
       send "'"$MSG"'" to targetBuddy
   end tell'

2. Make it executable:
   chmod +x ~/german_notify.sh

3. Add a cron job (crontab -e):
   0 7 * * * ~/german_notify.sh

Replace {phone} with your phone number (e.g., +1234567890).
══════════════════════════════════════════════════════════════
"""


def print_setup_instructions(base_url, phone="YOUR_PHONE_NUMBER"):
    print(SHORTCUTS_SETUP.format(base_url=base_url))
    print()
    print(MAC_APPLESCRIPT_SETUP.format(base_url=base_url, phone=phone))


if __name__ == "__main__":
    base_url = os.environ.get("BASE_URL", "https://your-app.onrender.com")
    print_setup_instructions(base_url)
