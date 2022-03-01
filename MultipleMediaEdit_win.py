#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import chardet

reload(sys)
sys.setdefaultencoding('UTF-8')

def utf8_2_gbk(str):
  return str.decode('UTF-8').encode('gbk')

def main(script_name, argv):
  inputfolder = ''
  removestr = ''
  addstr_begin=''
  addstr_end=''
  config_file="" #For mp3 edit
  start_num=''
  try:
    opts, args = getopt.getopt(argv,"hi:r:b:e:c:R:",["ifolder=", "rstr=", "abstr=", "aestr=","config=","start_number="])
  except getopt.GetoptError:
    print script_name + ' -i <inputfolder> -r <remove_str> -b <addstr_begin> -e <addstr_end> -c <config file with UTF-8 coding> -R <Rename with number sequence>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print script_name + ' -i <inputfolder> -r <remove_str> -b <addstr_begin> -e <addstr_end> -c <config file with UTF-8 coding> -R <Rename with number sequence>'
      sys.exit()
    elif opt in ("-i", "--ifolder"):
      inputfolder = arg
    elif opt in ("-r", "--rstr"):
      removestr = arg
    elif opt in ("-b", "--abstr"):
      addstr_begin = arg
    elif opt in ("-e", "--aestr"):
      addstr_end = arg
    elif opt in ("-c", "--config"):
      #Format: <Song_name>_<Singer>
      #Coding: UTF-8
      config_file = arg
    elif opt in ("-R", "--start_number"):
      start_num = arg

  list_file = os.listdir(inputfolder)
  if (len(config_file)!=0):#MP3 Edit
    song_names = []
    singers = []
    mp3_files = []
    config_f = open(config_file)
    for line in config_f.readlines():
      print str(len(line))
      if len(line) > 2:
        print "Line:" + line.decode('UTF-8').encode('gbk')
        song_names.append(line.strip().split('_')[0])
        singers.append(line.strip().split('_')[1])

    for i in range(0, len(list_file)):
      file_name = os.path.join(inputfolder, list_file[i])
      suffix_name = os.path.splitext(file_name)[-1]
      if suffix_name != ".mp3":
        print "Error: 含有非mp3文件，请清理！--> ".decode('UTF-8').encode('gbk') + file_name
        exit()
      mp3_files.append(file_name)

    if (len(mp3_files) != len(song_names)) or (len(song_names) != len(singers)):
      print "Error: 文件数量与配置内容不符!　请检查。".decode('UTF-8').encode('gbk')
      print "mp3_files number:" + str(len(mp3_files))
      print "song_names number:" + str(len(song_names))
      print "singers number:" + str(len(singers))

    index = 0
    for file in mp3_files:
      print file
      
      mp3 = MP3(file)
      if mp3.tags is None:
        mp3.add_tags()
      tags = mp3.tags
      mp3.save()

      #Edit Tags
      tags = EasyID3(file)
      tags['title'] = song_names[index]
      tags['artist'] = singers[index]
      tags.save()

      #Rename file
      dir_path = os.path.dirname(file)
      suffix_name = os.path.splitext(file_name)[-1]
      new_name = dir_path + '\\' + song_names[index] + "_" + singers[index] + suffix_name
      print new_name.decode('UTF-8')
      os.rename(file, new_name.decode('UTF-8'))

      index = index+1

  else:#Rename file only
    new_name=''
    for i in range(0, len(list_file)):
      full_file_name = os.path.join(inputfolder, list_file[i])
      if os.path.isfile(full_file_name):
        print "full_file_name:" + full_file_name
        
        dir_path = os.path.dirname(full_file_name)
        base_name = os.path.basename(full_file_name)
        suffix_name = os.path.splitext(full_file_name)[-1]
        
        if len(start_num) == 0 :
          new_name = dir_path + "\\" + addstr_begin + base_name.replace(removestr, '').replace(suffix_name, '') + addstr_end + suffix_name
        else: #Rename file with specify number sequence
          if len(start_num) == 1:
            start_num = '0' + start_num
          new_name = dir_path + "\\" + start_num + suffix_name
          
          start_num = str(int(start_num)+1)
        print "Rename to:" + new_name + '\n'

        os.rename(full_file_name, new_name)

if __name__ == "__main__":
  main(sys.argv[0], sys.argv[1:])