myCode
================================================================================================
MultipleMediaEdit.py

MultipleMediaEdit.py -i <inputfolder> -r <remove_str> -b <addstr_begin> -e <addstr_end> -c <config file with UTF-8 coding> -R <Rename with number sequence>'

Developed with: 
Windows
Python 2.7.15

Functional:
1. Rename files in a input folder
  1.1 Remove sub string from the files' name
      MultipleMediaEdit.py -i <inputfolder> -r <remove_str> 
  1.2 Add sub string at the begin or the end of the files' name
      MultipleMediaEdit.py -i <inputfolder> -b <addstr_begin> -e <addstr_end>
  1.3 Rename the files with a number sequence
      MultipleMediaEdit.py -i <inputfolder> -R 1(or the started number you want)

2. Edit MP3 file tags, the title and artist. And renambe the mp3 files with title. Depends on the content which is provided by a config file.
  MultipleMediaEdit.py -i <inputfolder> -c config.txt
================================================================================================