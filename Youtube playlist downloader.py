__author__ = "mehdi alouane"
__lisence__ = "GNU General Public License ,Versio 2.0"
__GPL__ = "http://opensource.org/licenses/GPL-2.0"
import re
from urlparse import *
from urllib import *
import tkFileDialog

#got this from wikipedia
raw_data="""18   MP4 	360p 	H.264 	Baseline 	0.5 	AAC 	96
34 	FLV 	360p 	H.264 	Main 	0.5 	AAC 	128
43 	WebM 	360p 	VP8 	N/A 	0.5 	Vorbis 	128
82 	MP4 	360p 	H.264 	3D 	0.5 	AAC 	96
101 	WebM 	360p 	VP8 	3D 	N/A 	Vorbis 	192
100 	WebM 	360p 	VP8 	3D 	N/A 	Vorbis 	128
5 	FLV 	240p 	Sorenson H.263 	N/A 	0.25 	MP3 	64
6 	FLV 	270p 	Sorenson H.263 	N/A 	0.8 	MP3 	64
13 	3GP 	N/A 	MPEG-4 Visual 	N/A 	0.5 	AAC 	N/A
17 	3GP 	144p 	MPEG-4 Visual 	Simple 	0.05 	AAC 	24
22 	MP4 	720p 	H.264 	High 	2-2.9 	AAC 	152
35 	FLV 	480p 	H.264 	Main 	0.8-1 	AAC 	128
36 	3GP 	240p 	MPEG-4 Visual 	Simple 	0.17 	AAC 	38
37 	MP4 	1080p 	H.264 	High 	3-4.3 	AAC 	152
38 	MP4 	3072p 	H.264 	High 	3.5-5 	AAC 	152
44 	WebM 	480p 	VP8 	N/A 	1 	Vorbis 	128
45 	WebM 	720p 	VP8 	N/A 	2 	Vorbis 	192
46 	WebM 	1080p 	VP8 	N/A 	N/A 	Vorbis 	192
83 	MP4 	240p 	H.264 	3D 	0.5 	AAC 	96
84 	MP4 	720p 	H.264 	3D 	2-2.9 	AAC 	152
85 	MP4 	520p 	H.264 	3D 	2-2.9 	AAC 	152
102 	WebM 	720p 	VP8 	3D 	N/A 	Vorbis 	192
""".splitlines()

format_dict ={}

for lines in raw_data:
    l = lines.split()
    fmt = l.pop(0)
    format_dict[fmt] = l

#returns the downloadable video link of a video in all available formats. original source code from
#http://stackoverflow.com/questions/2678051/cant-download-youtube-video (the second last comment)
#modified it myself though
def yt_url(video_url):
    video_id = parse_qs(urlparse(video_url).query)['v'][0]
    get_vars = parse_qs(unquote(urlopen("http://www.youtube.com/get_video_info?video_id="+video_id).read()))
    newdict = {}
    for urls in get_vars['itag']:
        try:
            (fmt,link) =urls.split(',')
            link = link[4:]
            newdict[fmt] = link
        except:
            break
    return newdict

#given a playlist id, return the links of all videos
def get_all_videos_in_playlist(ID):
    playlist_url ="http://www.youtube.com/playlist?list="+ID
    html_content = urlopen(playlist_url).read()
    urls = re.findall(r'/watch.+&amp;list='+str(ID)+r'&amp;index=[0-9]+&amp;feature=plpp_video',html_content)
    newurls = ["http://www.youtube.com"+urlitem for urlitem in urls]
    return newurls


ID = raw_input("Enter the playlist id ")
print "Retrieving videos from the list. Please wait.."
videos = get_all_videos_in_playlist(ID)
print len(videos), " videos retrieved from the playlist"
print "Now generating the download url"
i = 1

formatlist = []
downloadlink_by_index = {}

for urls in videos:
    print "Generating download link for url ", i
    dictionary = yt_url(urls)
    for items in dictionary:
        if items not in formatlist:
            formatlist.append(items)
        downloadlink_by_index[i] = dictionary
    i+=1

print
print "All dowload links generated. Printing information..."
print "There are a total of ", len(formatlist), " formats available"
for formats in formatlist:
    format_info = format_dict[formats]
    format_string = format_info[0] +'/' + format_info[1] +'/'+format_info[6] +'/'
    print formats, "  ", format_string

wantedformat = raw_input("Enter formatnumber eg. \"f1 f2 f3\" (without quotes). Video will be stored in f1 if available, else in f2 and so on").split()
for formats in formatlist:
    if formats not in wantedformat:
        wantedformat.append(formats)

downloadlinks = ""
for index in range(1,len(videos)+1):
    dictionary = downloadlink_by_index[index]
    #now determine the most nice available format
    for formats in wantedformat:
        if formats in dictionary:
            #save to file
            downloadlinks += dictionary[formats] + '\n'
            break

savefilename = tkFileDialog.asksaveasfilename(filetypes=[('text files','.txt')], initialfile='links.txt', title='Save download links')
file = open(savefilename,"w")
file.write(downloadlinks)
file.close
print "Done!!\nThanks for using this script!! So long!"
