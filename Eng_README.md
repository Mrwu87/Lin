# Lin - Use TUI style to manage files!

![image](https://github.com/Mrwu87/Lin/blob/master/linsc.png)

### [Lin](https://github.com/Mrwu87/Lin) as a file management terminal UI tool, in order to allow users to operate terminal files more quickly. Adhering to the principle of quick and practical, there are several shortcut keys to do a series of operations, you may feel uncomfortable at the beginning, and as you use it more often, I believe you will like the efficiency it brings

## Language
####  &nbsp; &nbsp;[中文](README.md) &nbsp; [English](Eng_README.md)

## Features

1. One click to copy file contents

2. One-click backup of files

3. automatically decompress multiple files/folders

4. compress multiple files/folders

5. graphical display of file list

6. support adding, deleting, moving and checking file contents

7. real-time view of file changes

8. terminal page

9. copy/cut multiple files/folders

10. filter file/folder function

11. cpu usage detection

12. memory usage detection

   ...............

## Upcoming Features
- File and folder modification permissions
- Remote file transfer function Remote file copy
- Automatic recognition of suffixes to run programs
- File content replacement and filtering
- Support mouse click function
- Global file search
- ......
## Shortcut Keys


| Action | Command |
|--------|---------|
| select file/folder | space |  
| undo selected files | ctrl esc |  
| Cut selected files/folders | X |
| refresh page | ctrl r |
| Copy File Contents | A |
| Exit Tools | ctrl w |
| call terminal | ctrl t |
| Quit Terminal | ctrl q |
| create file | ctrl n |
| Delete selected files/folders | ctrl d |
| Jump to directory | O |  
| Paste selected file | V |  
| enter | enter  
| Back to directory | esc |  
| Back up files | B | 
| Compress selected files/folders | Z | 
| unzip files | U | 
| view live changes | T | 
| View file contents in detail | L | 

---

## Installing dependency packages (optional)
#### pip install -r requirements.txt
## Run the program

#### python3 Lin.py
## Configuration file (optional)

#### Edit setting.yaml

```
editor: vi        #设定打开文件的编辑器
mouse: false      #开启鼠标模式（注意：这里开启之后就无法选取文字）
short_key:        #快捷键设置
  cut: X
  refresh: ctrl r
  copyContent: A
  quitDestop: ctrl w
  term: ctrl t
  quitTerm: ctrl q
  createFile: ctrl n
  deleteFile: ctrl d
  copyFile: C
  pasteFile: V
  goTo: O
  selectedFile: ' '
  cancelSelected: ctrl esc
  backdir: esc
  backUpfile: B
  zip: Z
  unzip: U
  tail: T
  less: L

```


## More Skins
#### Not yet online

