#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
  
def utf8_2_gbk(str):
  return str.decode('UTF-8').encode('gbk')

def main(script_name, argv):
  inputfolder = ''
  removestr = ''
  addstr_begin=''
  addstr_end=''
  try:
    opts, args = getopt.getopt(argv,"hi:r:b:e:",["ifolder=", "rstr=", "abstr=", "aestr="])
  except getopt.GetoptError:
    print script_name + ' -i <inputfolder> -r <remove_str> -ab <addstr_begin> -ae <addstr_end>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print script_name + ' -i <inputfolder> -r <remove_str> -ab <addstr_begin> -ae <addstr_end>'
      sys.exit()
    elif opt in ("-i", "--ifolder"):
      inputfolder = arg
    elif opt in ("-r", "--rstr"):
      removestr = arg
    elif opt in ("-b", "--abstr"):
      addstr_begin = arg
    elif opt in ("-e", "--aestr"):
      addstr_end = arg
  print '视频存放目录：'.decode('UTF-8').encode('gbk') + inputfolder
  print '删除的字符串：'.decode('UTF-8').encode('gbk') + removestr

  list_file = os.listdir(inputfolder)
  for i in range(0, len(list_file)):
    full_file_name = os.path.join(inputfolder, list_file[i])
    if os.path.isfile(full_file_name):
      print "full_file_name:" + full_file_name
      dir_path = os.path.dirname(full_file_name)
      base_name = os.path.basename(full_file_name)
      suffix_name=os.path.splitext(full_file_name)[-1]
      new_name = dir_path + "\\" + addstr_begin + base_name.replace(removestr, '').replace(suffix_name, '') + addstr_end + suffix_name
      print "base_name:" + base_name
      print "Rename to:" + new_name + '\n'

      os.rename(full_file_name, new_name)
    
if __name__ == "__main__":
  main(sys.argv[0], sys.argv[1:])