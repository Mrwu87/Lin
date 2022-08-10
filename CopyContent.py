import pyperclip
#sudo apt-get install xclip  #安装复制剪切工具包
#可以复制文本内容
with open('GA.py') as f:
    a=f.read()
pyperclip.copy(a)
#中间条输入是筛选文件的
#可以召唤出终端control + T
#使用ansible扩展工具内容