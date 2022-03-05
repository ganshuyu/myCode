myCode
================================================================================================
./MultipleMediaEdit_linux.py -h
 -i <input folder or file>
 -r <remove_str>
 -b <add str at begin>
 -e <add str at end>
 -c <config file>
 -R <Rename with a number sequence>
 -o <output folder>

Env:
  Linux
  Python 2.7.15

Functional:
  1. Rename files in a input folder
    1.1 Remove sub string from the files' nam
 
      MultipleMediaEdit.py -i <inputfolder> -r <remove_str> 
    
    1.2 Add sub string at the begin or the end of the files' name
    
      MultipleMediaEdit.py -i <inputfolder> -b <addstr_begin> -e <addstr_end>
    
    1.3 Rename the files with a number sequence
    
      MultipleMediaEdit.py -i <inputfolder> -R 1(or the started number you want)

  2. Edit MP3 file tags, the title and artist. And then renambe the mp3 files with title.
    
     MultipleMediaEdit.py -i <inputfolder> -c config.txt
  
  3. Split long MP3 file tags, then rename the file name + title + artist of the output files.
    
     MultipleMediaEdit.py -i long.mp3 -c config.txt
================================================================================================
