import sys
import os
import hashlib
try: 
    import urllib2
except:
    import urllib.request as urllib2

if sys.version[0] == '3':
    raw_input = input

URL_SUBDB = "http://api.thesubdb.com/?action=download&hash={0}&language={1}"
USER_AGENT = "SubDB/1.0 (subbot/alpha; http://github.com/maldoinc/subtitle-downloader)"


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)

        # slight adjustment to the provided subdb function to not read if there's not enouh bytes
        # as to not throw an exception
        if size > readsize:
            f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def subdb_perform_request(f_hash, langs):
    endpoint = URL_SUBDB.format(f_hash, ",".join(langs))
    req = urllib2.Request(endpoint, headers={"User-Agent": USER_AGENT})
    try:
        res = urllib2.urlopen(req)
        return True, "OK", res.read()
    except urllib2.HTTPError as err:
        if err.code == 404:
            return False, "Error: Subtitles not found", ""
        elif err.code == 400:
            return False, "Error: Bad request", ""
        else:
            return False, "Unknown error", ""


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Missing required arguments")
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print("Requested file doesn't exist")
        sys.exit()

    filename = sys.argv[1]
    wait = len(sys.argv) > 2 and sys.argv[2] == '--wait'
    file_hash = get_hash(filename)
    sub_fn = "{0}.srt".format(os.path.splitext(filename)[0])

    success, message, subtitles = subdb_perform_request(file_hash, ['en'])

    if success:
        open(sub_fn, "wb").write(subtitles)
    elif wait:
        print(message)
        raw_input("")
