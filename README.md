# tipster

Tired of copy and pasting IOCs from Slack/Discord/whatever to your TIP? Ever wanted to download somebody else's code that was incomplete and swear a bunch while trying to add your specific features to it?

Great! Clone this repo now!

This script spins up a helpfuly 'clippy' that will monitor your clipboard for IOCs and then, assuming I haven't added it, enable you to add code to a function so you can submit those IOCs (after editing them) to the TIP of your chosing.

Only tested on OS X.
* Requires GTK - `brew install pygtk pygobject3 gtk+3`
* python-iocextract - https://github.com/InQuest/python-iocextract `pip install iocextract`
