# Aloscraper 2022

Download courses from <https://www.alomoves.com> automatically.

A quick update to gatekeepr's code to make it work for me. 
Gets the individual class links, HAR file, then video link, then downloads video and txt of class description.

Not much error catching. Just watch the screen occasionally and re-run if any issues grabbing the video.m3u8 from the class site. If the page isn't fully loaded, you will end up getting the preview intro video or nothing at all (code will crash if no video.m3u8 in the HAR file).

## Installation

1. `pip3 install -r requirements.txt`
2. Navigate to Lib\site-packages\haralyzer\assets.py
At line 367, add an "else:" so the script looks like this...

else:
   for page in raw_data["pages"]:
         if page["id"] == self.page_id:
            valid = True
            self.title = page.get("title", "")
            self.startedDateTime = page["startedDateTime"]
            self.pageTimings = page["pageTimings"]

2. Download Chrome Webdriver according to your Version (probably 80) [HERE](https://chromedriver.chromium.org/downloads) and place into your working folder next to the .py (or add it to your PATH)
3. Make sure you have a valid alomoves account on hand (Trial accounts are fine).
4. Place the links of courses you want to download in **downloadlinks.txt**, one per line.
   - Example: <https://www.alomoves.com/series/COURSENAME/workouts>
   - You find these links by navigating to the course page and find the Classes tab (where all the individual videos are shown with thumbnails)
5. Edit the download.py file with your email and password.

## Variables to set in sourcecode

- UNIQUE: list of unique class index. default assumption is that all vids in all series are unique.

e.g. 30 day workout series only has 6 unique videos (how to vid + day 1-5 vids) then this set repeats the rest of the month. Only other special exception is day 15 (intro to new skill) and day 30 (final test?).
   UNIQUE = [0,1,2,3,4,5,15,30]
Selective downloading using UNIQUE will be applied to all series in the downloadlinks.txt so use sparingly.


## Usage

1.  `python downloader.py`

## Notes from me:
This code is my first try at scraping with selenium so it's not perfect and I ran into many issues along the way. Please do what you want with it and I'd be more than happy to listen if you have feedback or advice :)

Issues I ran into:
- have to login and logout for every video. got an error if i logged in once and tried downloading multiple vids.
- not sure how to make sure page is fully loaded with main video before downloading har file. just ended up making time.sleep() really long
