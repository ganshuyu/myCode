#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import chardet
import commands

reload(sys)
sys.setdefaultencoding('UTF-8')

def print_list_in_utf8(mlist, list_name):
  print "=========================="
  print "List: " + list_name
  for i in range(0, len(mlist)):
    print mlist[i].decode('UTF-8')
  print "++++++++++++++++++++++++++"

#Functional: Refer to the config file to Split mp3 and Rename the splited files. Or Edit the MP3 Tag of all the files in the input folder.
def MP3_edit(config_file, long_mp3_file, file_list, inputfolder, outputfolder):
  time_stamps = []
  song_names = []
  singers = []
  mp3_files = []

  config_f = open(config_file)
  for line in config_f.readlines():
    if len(line) > 2:
      try:
        time_stamps.append(line.strip().split('-')[0].strip())
      except:
        print "Waring: No time stamps in config file."

      try:
        line = line.strip().split('-')[1].strip()
      except:
        print "Waring: No time stamps in config file."

      song_names.append(line.strip().split('_')[0])
      singers.append(line.strip().split('_')[1])

  if len(long_mp3_file) > 0:#Split long mp3 file
    print "Long MP3: " + long_mp3_file
    total_length = commands.getstatusoutput("ffprobe -i " + long_mp3_file + " -show_entries format=duration -v quiet -of csv=\'p=0\' -sexagesimal")[1]
    time_stamps.append(total_length)
    print_list_in_utf8(time_stamps, "time_stamps")

    #Split files!
    for i in range(0, len(song_names)):
      outfile= outputfolder + '/' + str(i).rjust(2, "0") + ".mp3"
      start = time_stamps[i]
      end = time_stamps[i+1]
      print "Start: " + start
      print "End: " + end
      print "OutFile: " + outfile
      ret = commands.getstatusoutput("ffmpeg -nostdin -y -loglevel error -i " + long_mp3_file + " -ss " + start + " -to " + end + " -acodec copy " + outfile )
      print ret

    if len(file_list) == 0:
      file_list = os.listdir(outputfolder)
      file_list.sort()

    #If split MP3 file, the input folder is set as the outputfolder for renaming below.
    inputfolder = outputfolder

  print_list_in_utf8(file_list, "file_list")

  for i in range(0, len(file_list)):
    file_name = os.path.join(inputfolder, file_list[i])
    suffix_name = os.path.splitext(file_name)[-1]
    if suffix_name != ".mp3":
      continue
    mp3_files.append(file_name)

  if (len(mp3_files) != len(song_names)) or (len(song_names) != len(singers)):
    print "Error: file number and config content is not matching!"
    print "mp3_files number:" + str(len(mp3_files))
    print "song_names number:" + str(len(song_names))
    print "singers number:" + str(len(singers))
    exit()

  #Rename file and edit tag
  for index in range(0, len(mp3_files)):
    file = mp3_files[index]
    mp3 = MP3(file)
    if mp3.tags is None:
      mp3.add_tags()
    tags = mp3.tags
    mp3.save()

    #Edit Tags
    tags = EasyID3(file)
    print "Song: " + song_names[index]
    print "Singer: " + singers[index]
    tags['title'] = song_names[index]
    tags['artist'] = singers[index]
    tags.save()

    #Rename file
    dir_path = os.path.dirname(file)
    suffix_name = os.path.splitext(file_name)[-1]
    new_name = dir_path + '/' + song_names[index] + "_" + singers[index] + suffix_name
    print "Old: " + file
    print "New: " + new_name + "\n\r"
    os.rename(file, new_name.decode('UTF-8'))

#Functional: Rename/Edit all the files in input folder
def Rename_edit_files_name(file_list, inputfolder, start_num):
  new_name=''
  for i in range(0, len(file_list)):
    full_file_name = os.path.join(inputfolder, file_list[i])
    if os.path.isfile(full_file_name):
      print "full_file_name:" + full_file_name

      out_dir = os.path.dirname(full_file_name)
      base_name = os.path.basename(full_file_name)
      suffix_name = os.path.splitext(full_file_name)[-1]

      if len(start_num) == 0 :
        new_name = out_dir + '/' + addstr_begin + base_name.replace(removestr, '').replace(suffix_name, '') + addstr_end + suffix_name
      else: #Rename file with specify number sequence
        if len(start_num) == 1:
          start_num = '0' + start_num
        new_name = out_dir + '/' + start_num + suffix_name

        start_num = str(int(start_num)+1)
      print "Rename to:" + new_name + '\n'

      os.rename(full_file_name, new_name)

def print_help(script_name):
  print script_name + "\n -i <input folder or file>\n -r <remove_str>\n -b <add str at begin>\n -e <add str at end>\n" +\
                      "-c <config file>\n -R <Rename with a number sequence>\n -o <output folder>"
  exit()

def main(script_name, argv):
  input_folder_Or_file = ''
  removestr = ''
  addstr_begin = ''
  addstr_end = ''
  config_file = "" #For mp3 edit
  start_num = ''
  inputfolder = ''
  outputfolder = ''
  long_mp3_file = ''

  try:
    opts, args = getopt.getopt(argv,"hi:r:b:e:c:R:o:",["ifolder=", "rstr=", "abstr=", "aestr=","config=","start_number=","ofolder="])
  except getopt.GetoptError:
    print_help(script_name)
  for opt, arg in opts:
    if opt == '-h':
      print_help(script_name)
    elif opt in ("-i", "--ifolder"):
      input_folder_Or_file = arg
    elif opt in ("-o", "--ofolder"):
      outputfolder = arg
      if not os.path.isdir(outputfolder):
        commands.getstatusoutput("mkdir " + outputfolder)
    elif opt in ("-r", "--rstr"):
      removestr = arg
    elif opt in ("-b", "--abstr"):
      addstr_begin = arg
    elif opt in ("-e", "--aestr"):
      addstr_end = arg
    elif opt in ("-c", "--config"):
      print "Format: \"<Song_name>_<Singer>\" or \"<Start_time> - <Song_name>_<Singer>\""
      config_file = arg
    elif opt in ("-R", "--start_number"):
      start_num = arg

  inputfolder = os.path.dirname(input_folder_Or_file)
  if len(input_folder_Or_file) == 0:
    print "Error! Input file or folder is a MUST option!"
    exit()
  elif len(inputfolder) == 0:
    inputfolder = os.path.realpath(input_folder_Or_file)

  if len(outputfolder) == 0:
    outputfolder = inputfolder

  print "inputfolder: " + inputfolder
  print "outputfolder: " + outputfolder

  file_list = []
  if os.path.isdir(input_folder_Or_file):#Input is a folder name
    file_list = os.listdir(inputfolder)
    file_list.sort()
  else:#Input is a file name
    long_mp3_file = input_folder_Or_file

  #Print all input files
  print_list_in_utf8(file_list, "file_list")

  if len(config_file) > 0:
    MP3_edit(config_file, long_mp3_file, file_list, inputfolder, outputfolder)
  else:
    Rename_edit_files_name(file_list, inputfolder, start_num)

if __name__ == "__main__":
  main(sys.argv[0], sys.argv[1:])