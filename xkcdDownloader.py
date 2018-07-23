import os, requests, bs4
import time

url = "http://xkcd.com"


os.makedirs('xkcd')

while not url.endswith('#'):
    print('Downloading page %s' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)

    comicElm = soup.select('#comic img')
    if comicElm == []:
        print('Could not load the comic')

    else:
        comicUrl = comicElm[0].get('src').strip("http://")
        comicUrl = "http://" + comicUrl
        if 'xkcd' not in comicUrl:
            comicUrl = comicUrl[:7] + 'xkcd.com/' + comicUrl[7:]
        print("comic url", comicUrl)
        print('Downloading image %s ' % (comicUrl))

        #Be nice, do not launch a DoS attack

        time.sleep(2)

        res = requests.get(comicUrl)
        res.raise_for_status()
        imageFIle = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFIle.write(chunk)
        imageFIle.close()
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print('Done')
