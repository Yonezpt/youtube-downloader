import pip

try:
    pip.main(['install', '--upgrade', 'pip'])
except:
    pass

try:
    pip.main(['install', '--upgrade', 'youtube_dl'])
except:
    pip.main(['install', 'youtube_dl'])

import os
import sys
import time
import youtube_dl

class YoutubeDownloader:
    def __init__(self):
        self.audio_only = None
    
    def downloadVideo(self, youtube_url):
        with youtube_dl.YoutubeDL({}) as ydl:
            return ydl.extract_info(youtube_url, download=True)

    def downloadAudio(self, youtube_url):
        ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(youtube_url, download=True)

class FolderSystem:
    def __init__(self):
        self.DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'downloads')
        self.LOG_DIRECTORY = os.path.join(os.getcwd(), 'logs')
        self.LIST_DIRECTORY = os.path.join(os.getcwd(), 'lists')

        if os.path.exists(self.DOWNLOAD_DIRECTORY) == False:
            os.mkdir(self.DOWNLOAD_DIRECTORY)

        if os.path.exists(self.LOG_DIRECTORY) == False:
            os.mkdir(self.LOG_DIRECTORY)

        if os.path.exists(self.LIST_DIRECTORY) == False:
            os.mkdir(self.LIST_DIRECTORY)
    
    def log(self, log_name, log_content):
        file = open(os.path.join(self.LOG_DIRECTORY, log_name), 'a')
        file.write(str(log_content))
        file.close()

    def movePlaylistAudio(self, playlist_name):
        audio_extension = '.mp3'
        DESTINATION_DIRECTORY = os.path.join(self.DOWNLOAD_DIRECTORY, playlist_name)

        for file in os.listdir(os.getcwd()):
            if file.endswith(audio_extension) and os.path.isfile(file):
                 os.rename(os.path.join(os.getcwd(), file), os.path.join(self.DOWNLOAD_DIRECTORY, playlist_name, file))

    def movePlaylistVideo(self, playlist_name):
        video_extension = ['.mp4', '.mkv', '.webm', '.3gp']
        DESTINATION_DIRECTORY = os.path.join(self.DOWNLOAD_DIRECTORY, playlist_name)

        for file in os.listdir(os.getcwd()):
            for extension in video_extension:
                if file.endswith(extension) and os.path.isfile(file):
                    os.rename(os.path.join(os.getcwd(), file), os.path.join(self.DOWNLOAD_DIRECTORY, playlist_name, file))


if __name__ == '__main__':
    youtube_downloader = YoutubeDownloader()
    folder_system = FolderSystem()

    os.system('cls')
    text_file_directory = input('File containing links : ')
    audio_only = eval(input('Audio Only ? (True/False) : '))
    print('Starting . . .')

    try:
        file = open(os.path.join(folder_system.LIST_DIRECTORY, text_file_directory), 'r')
    except FileNotFoundError:
        print('File is not found, exiting program.')
        sys.exit()
    else:
        for youtube_url in file.read().split('\n'):
            if youtube_url != '':
                try:
                    if audio_only == True:
                        meta_data = youtube_downloader.downloadAudio(youtube_url)
                    else:
                        meta_data = youtube_downloader.downloadVideo(youtube_url)
                except Exception as exception_message:
                    localtime = time.asctime(time.localtime())

                    folder_system.log('download_failure_log.txt','[' + localtime + '] ' + youtube_url + '\n')
                    folder_system.log('failure_exception.txt', '[' + localtime + '] ' + str(exception_message) + '\n')
                    print('Something wrong occured.')

            if 'entries' in meta_data:
                playlist_name = meta_data['entries'][0]['playlist']
                if os.path.exists(os.path.join(folder_system.DOWNLOAD_DIRECTORY, playlist_name)) == False:  
                    os.mkdir(os.path.join(folder_system.DOWNLOAD_DIRECTORY, playlist_name))

                if audio_only == True:
                    folder_system.movePlaylistAudio(playlist_name)
                else:
                    folder_system.movePlaylistVideo(playlist_name)
            else:
                if audio_only == True:
                    folder_system.movePlaylistAudio('')
                else:
                    folder_system.movePlaylistVideo('')

        file.close()