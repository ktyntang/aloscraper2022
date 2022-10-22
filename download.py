import requests  # download html
from bs4 import BeautifulSoup  # get data from html
from generate_linkset import generate_linkset
import youtube_dl
import pprint
from getclasslinks import getclasslinks
import os

email = ''
password = ''

pp = pprint.PrettyPrinter(indent=4)
                
def make_series_folder(series):
    linkset = series[0]
    if len(linkset) == 2:
        firstlink = linkset[0] 
    else:
        firstlink = linkset
    folder_name = firstlink.split("/series")[1].split("workouts")[0].replace("/","")
    path = os.path.join(os.getcwd(), folder_name)
    os.mkdir(path)
    return path

def download_txt_mp4(list_of_linkset, path):
    for i,linkset in enumerate(list_of_linkset):
        if len(linkset) > 2: 
            res = requests.get(linkset)
            soup = BeautifulSoup(res.text, 'html.parser')
            videotitle = soup.find("div", class_="workoutTitle").get_text().replace(':','').strip()
            videodescription = soup.find("div", class_="workout-information").get_text()

            with open(f"{path}/{str(i)} {videotitle}.txt", "w") as file:
                file.write(videodescription)
                
        elif len(linkset) == 2 :
            [url,videoURL] = linkset
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            videotitle = soup.find("div", class_="workoutTitle").get_text().replace(':','').strip()
            videodescription = soup.find("div", class_="workout-information").get_text()
            outtmpl = f"{path}/{str(i)} {videotitle}.%(ext)s"

            ydl_opts = {
            'outtmpl': outtmpl,
            'noplaylist' : True}

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([videoURL])
            with open(f"{path}/{str(i)} {videotitle}.txt", "w") as file:
                file.write(videodescription)


def main():
    serieslist = getclasslinks(email, password)

    serieslist = []

    for no,series in enumerate(serieslist):
        folder_path = make_series_folder(series)
        UNIQUE = range(len(series)) 
        # change to list of class indices if there are repeats.
        newlinks = []
        for i, link in enumerate(series):
            if i in UNIQUE:
                try:
                    linkset = generate_linkset(link, email, password)
                except:
                    raise Exception('ERROR CONNECTING. TRY AGAIN.')
                else:
                    newlinks.append(linkset)
                finally:
                    pp.pprint(newlinks)
            else:
                newlinks.append(link)

        pp.pprint(newlinks)
        print(f"VIDEO LINKS GENERATED FOR {no+1}/{len(serieslist)+1} SERIES. DOWNLOADING {len(newlinks)} VIDEOS NOW....")
        download_txt_mp4(newlinks, folder_path)

if __name__ == '__main__':
    main()

