import urwid
import threading
import  time
import os,sys
import datetime
import psutil
import yaml
import pyperclip



with open('setting.yaml','r') as config:
    setting=yaml.safe_load(config)
Loop=None               #使用loop来承载 self.loop 对象
exterfonts=None         #原始外部font 可以使用_get_widget_list 或者 _set_widget_list方法来修改一整个按钮列表
original_buttons=None   #主要是exterfonts下的_ge_widget_list获取的按钮列表  代表筛选前的按钮列表
views=None
file_list=[]            #用于承载选择的文件列表
pop_up=None


class SwitchingPadding(urwid.Padding):
    def padding_values(self, size, focus):
        maxcol = size[0]
        width, ignore = self.original_widget.pack(size, focus=focus)
        if maxcol > width:
            self.align = "left"
        else:
            self.align = "right"
        return urwid.Padding.padding_values(self, size, focus)

def ctrl_opeater(opeater):
    '''
    用于显示快捷键提示 操作列表重新写入之后该函数自动操作添加到列表中
    :param opeater: 操作字典
    :return: oper_list
    '''
    oper_list=[]
    oper_list.append(urwid.Divider())
    for i in opeater:
        ctrls = urwid.Text(i)
        oper_list.append(ctrls)
    return oper_list
def count_str(text):
    s=len(text.encode('gbk'))
    text_len=35-s
    return text_len*' '
def file_dir():
    '''
    对文件的处理 调用这个函数可以得到file, dir 这两个参数分别文件列表，和目录列表
    是ls过后 判断一行是文件还是目录如果是其中一个就放入到函数中
    :return:
    '''
    # getFileInfo('/home/wlw/PycharmProjects/pythonProject')
    with open('dir.yaml', 'r') as f:
        datas = yaml.safe_load(f)
    dir_path=datas['Dir']
    if setting['show_hide_files']:
        output = os.popen(f"ls -lAhF '{dir_path}'")
    else:
        output = os.popen(f"ls -lhF '{dir_path}'")
    # print(output)
    dir = []
    file = []
    for i in output:
        if i.strip().split(' ')[0] == 'total':
            continue
        output_list = i.strip().split(' ')
        output_list = [ii for ii in output_list if (len(str(ii)) != 0)]  # 去除列表空值
        if output_list[0][0] == 'd':
            dir.append(output_list)
        elif output_list[0][0] == 'l' and output_list[-1][-1] == '/':
            # os.system(f'echo {output_list} >> 123')
            dir.append(output_list)
        elif output_list[0][0] == 'l' and output_list[-1][-1] != '/':
            file.append(output_list)
        elif  output_list[0][0] == 'c' or output_list[0][0] == 'b':
            os.system(f"echo '{output_list}' > 123")
            output_list[4:-1]=[' ',' ',' ',' ',' ']
            # output_list[-2] = 'None'
            file.append(output_list)
        else:
            file.append(output_list)
    return file, dir


def reload_dir():
    font_buttons = create_button_list(*file_dir())
    exterfonts._set_widget_list(font_buttons)
    global original_buttons
    global file_list
    original_buttons = exterfonts._get_widget_list()
    file_list = []
    return exterfonts

def create_button_list(file, dir):
    font_buttons=[]
    '''
    该方法是用于处理文件、目录按钮的把这些按钮都放入到font_buttons中，然后显示到页面上
    打开目录就会调用这个方法来显示，如果缺少目录或者文件就会创建空按钮
    '''
    if file == [] and dir == []:  # 如果file和dir列表为空
        file = dir = [' ']
    elif file == []:
        file = [' ']
    elif dir == []:  # 1 如果dir为空的话 那么创建一个file按钮
        for i in [' ']:
            rb = create_file_button(i)
            font_buttons.append(rb)
    for i in dir:
        rb = create_dir_button(i)  #创建dir按钮
        font_buttons.append(rb)
    for i in file:

        rb = create_file_button(i) #创建file按钮
        if dir == []:  # 1 如果dir为空的话 那么创建一个file按钮追加到空白按钮的前面
            font_buttons.insert(0, rb)
        else:
            font_buttons.append(rb)
    return font_buttons

def filename_handling(name):
    if name[-2] == '->':
        # os.system(f'echo {name} >> 123')
        file = name[-1] + ' ' + name[-2] + ' ' + name[-3]
    else:
        # os.system(f'echo {name} >> 123')
        file = name[-1]
    user_group = name[2] + '/' + name[3]
    chmod = name[0]
    file_size = name[4]
    if len(name[6]) == 2 and len(name[5]) == 3:
        dates = name[5] + name[6] + '日' + ' ' + name[7]
    elif len(name[5]) < 3 and len(name[6]) < 2:
        dates = '0' + name[5] + '0' + name[6] + '日' + ' ' + name[7]
    elif len(name[6]) < 2:
        dates = name[5] + '0' + name[6] + '日' + ' ' + name[7]
    elif len(name[5]) < 3:
        dates = '0' + name[5] + name[6] + '日' + ' ' + name[7]
    return f' {file[:30]}{count_str(file[:30])}{user_group}{count_str(user_group)}{chmod}{count_str(chmod)}{file_size}{count_str(file_size)}{dates}'

def create_dir_button(name):
    '''
        #处理按钮的显示页面部分，显示按钮的文字内容再通过调用传递创建按钮类中
        :param name: 得到ls后的文本内容
        :return: 已处理好的按钮对象
    '''
    #w = urwid.RadioButton(g, name, False, on_state_change=fn)
    if name!=' ':
        w=DirButton(filename_handling(name))
        w=w.create_appwarp(w) #对按钮创建Attrwarp
    else:
        w = urwid.Button(' ')
        w = urwid.AttrWrap(w,'button normal', 'dir button select')
    #os.system(f"echo '{w.set_focus_attr()} '> 123")
    return w

def create_file_button(name):
    '''
    #处理按钮的显示页面部分，显示按钮的文字内容再通过调用传递创建按钮类中
    :param name: 得到ls后的文本内容
    :return: 已处理好的按钮对象
    '''
    if name != ' ':
        Attrwarp=FileButton(filename_handling(name))
        w = ThingWithAPopUp(Attrwarp)
        w = Attrwarp.create_appwarp(w)  #对按钮创建Attrwarp样式
    else:
        w = urwid.Button(' ')
        w = urwid.AttrWrap(w, 'button normal', 'file button select')
    return w

#创建同种button按钮的按键可以做到不一样的效果
#目录按钮的重写类用于对按钮进行逻辑操作
class DirButton(urwid.Button):

    def create_appwarp(self,w):
        self.attrwarp=urwid.AttrWrap(w,'button normal', 'dir button select')
        return self.attrwarp


    def keypress(self, size, key):
        file_data = [ii for ii in self.label.strip().split(" ") if (len(str(ii)) != 0)]
        dirname = file_data[0]

        if key ==setting['short_key']['chmod']:
            user_group = file_data[1]
            permission = file_data[2][1:]
            Chmod(views, Loop,dirname,user_group,permission)
        if key in ('enter',) :
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            with open('dir.yaml', 'w') as f:
                datas['Dir']=datas["Dir"] + dirname
                yaml.dump(datas,f)
                #os.system(f'ls -alh {datas["Dir"]}{self.label.strip().split(" ")[0]} > file.txt')
            # font_buttons = create_button_list(*file_dir())
            # global exterfonts
            # exterfonts._set_widget_list(font_buttons)
            # exterfonts.set_focus(0)
            # global original_buttons
            # original_buttons = exterfonts._get_widget_list()
            fonts=reload_dir()
            fonts.set_focus(0)
            #self._emit('click')
        elif key == setting['short_key']['selectedFile']:  #空格选取
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+dirname
            #os.system(f"echo '{file_list}' >> 123")
            if self.attrwarp.get_attr() == 'select':
                self.attrwarp.set_attr('button normal')
                file_list.remove(file_path)
            else:
                self.attrwarp.set_attr('select')
                file_list.append(file_path)
        # elif key == setting['short_key']['cancelSelected']:
        #     self.attrwarp.set_attr('dir button select')
                #urwid.AttrWrap(self,'button normal', 'delete')
        else:
            return key

#文件按钮的重写类用于对按钮进行逻辑操作
class FileButton(urwid.Button):
    # def __init__(self, abc):
    #     self.abc = abc
    def create_appwarp(self, w):
        self.attrwarp = urwid.AttrWrap(w, 'button normal', 'file button select')
        return self.attrwarp

    def keypress(self, size, key):
        global Loop
        global views
        # if key in ('ctrl p',) :
        #     os.system(f'echo {self.label.strip().split(" ")[-1]} > wulinwei1.py')

        #user_group = self.label.strip().split(" ")[1]
        file_data= [ii for ii in self.label.strip().split(" ") if (len(str(ii)) != 0)]
        filename=file_data[0].strip('*')

        # os.system(f"echo '{permission}' > 123")
        if key ==setting['short_key']['chmod']:
            user_group = file_data[1]
            permission = file_data[2][1:]
            Chmod(views, Loop,filename,user_group,permission)
        elif key == setting['short_key']['unzip']:
            # Zipfile(self.view,self.loop)
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            if filename.split('.')[-1] == 'tgz' or  filename.split('.')[-1]=='gz' and filename.split('.')[-2]=='tar' :
                #os.system(f"echo {datas['Dir']}{filename} >123")
                os.system(f'tar -zxf {datas["Dir"]}{filename} -C {datas["Dir"]} ')
                # global original_buttons
                # font_buttons = create_button_list(*file_dir())
                # exterfonts._set_widget_list(font_buttons)
                # original_buttons = exterfonts._get_widget_list()
                reload_dir()
            if filename.split('.')[-1] == 'zip' :
                os.system(f'unzip  {datas["Dir"]}{filename} -d {datas["Dir"]}  2>&1 > /dev/null ')
                reload_dir()
            return
        elif key == setting['short_key']['tail']:

            tail_term=Showfile(views,filename,'tail')
            exit = urwid.LineBox(tail_term)
            exit = urwid.Overlay(exit, views, 'center', 150, 'middle', 150)
            Loop.widget = exit

        elif key == setting['short_key']['less']:
            less_term=Showfile(views,filename,'less')
            exit = urwid.LineBox(less_term)
            exit = urwid.Overlay(exit, views, 'center', 150, 'middle', 150)
            Loop.widget = exit
        elif  key == setting['short_key']['backUpfile']:  # 一键备份文件
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            backup_file=datas['Dir']+filename+'.bak'
            current_file=datas['Dir']+filename
            os.system(f"cp -af '{current_file}' '{backup_file}' ")
            #exterfonts._set_widget_list()
            #global original_buttons

            # font_buttons = create_button_list(*file_dir())
            # exterfonts._set_widget_list(font_buttons)
            # original_buttons = exterfonts._get_widget_list()
            reload_dir()


        elif  key ==setting['short_key']['copyContent']:  # 一键复制文件内容
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+filename
            with open(f'{file_path}') as f:
                file_content = f.read()
            pyperclip.copy(file_content)
        elif key in ('enter',):
            # self._emit('click') #点击文件按钮发送click信号给按钮本身 模拟点击操作
            pop_up()
        elif key == setting['short_key']['selectedFile']:
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+filename
            #os.system(f"echo '{file_list}' >> 123")
            if self.attrwarp.get_attr()=='select':  #如果是已经选择了则回到正常状态
                self.attrwarp.set_attr('button normal')
                file_list.remove(file_path)
            else:
                self.attrwarp.set_attr('select')
                file_list.append(file_path)
        # elif key ==  setting['short_key']['cancelSelected']:
        #     self.attrwarp.set_attr('file button select')
        else:
            return key

class Showfile(urwid.Terminal):
    def __init__(self,view,filename,exec):
        self.view = view
        urwid.set_encoding('utf8')
        with open('dir.yaml', 'r') as f:
            datas = yaml.safe_load(f)
        #os.system(f"echo '{filename}' > 123")
        if exec == 'tail':
            self.__super.__init__(('tail','-f', '-n 300',f'{datas["Dir"]+filename}'), encoding='utf-8') #创建一个终端
        elif exec == 'less':
            self.__super.__init__(('less','-N','-m',f'{datas["Dir"] + filename}'), encoding='utf-8')  # 创建一个终端
        self.main_loop=Loop   #这一步让终端流畅运行
    def keypress(self, size, key):

        if key == setting['short_key']['quitTerm'] :  # 判断是否为ctrl q 按钮

            Loop.widget = self.view

        if self.terminated:
            return key

        if key == "window resize":
            width, height = size
            self.touch_term(width, height)
            return

        if (self.last_key == self.escape_sequence
                and key == self.escape_sequence):
            # escape sequence pressed twice...
            self.last_key = key
            self.keygrab = True
            # ... so pass it to the terminal
        elif self.keygrab:
            if self.escape_sequence == key:
                # stop grabbing the terminal
                self.keygrab = False
                self.last_key = key
                return
        else:
            if key == 'page up':
                self.term.scroll_buffer()
                self.last_key = key
                self._invalidate()
                return
            elif key == 'page down':
                self.term.scroll_buffer(up=False)
                self.last_key = key
                self._invalidate()
                return
            elif (self.last_key == self.escape_sequence
                  and key != self.escape_sequence):
                # hand down keypress directly after ungrab.
                self.last_key = key
                return key
            elif self.escape_sequence == key:
                # start grabbing the terminal
                self.keygrab = True
                self.last_key = key
                return
            elif self._command_map[key] is None or key == 'enter':
                # printable character or escape sequence means:
                # lock in terminal...
                self.keygrab = True
                # ... and do key processing
            else:
                # hand down keypress
                self.last_key = key
                return key

        self.last_key = key

        self.term.scroll_buffer(reset=True)
        from urwid.compat import ord2, chr2, B, bytes, PYTHON3, xrange

        # EOF = B('')
        ESC = chr(27)

        KEY_TRANSLATIONS = {
            'enter': chr(13),
            'backspace': chr(127),
            'tab': chr(9),
            'esc': ESC,
            'up': ESC + '[A',
            'down': ESC + '[B',
            'right': ESC + '[C',
            'left': ESC + '[D',
            'home': ESC + '[1~',
            'insert': ESC + '[2~',
            'delete': ESC + '[3~',
            'end': ESC + '[4~',
            'page up': ESC + '[5~',
            'page down': ESC + '[6~',

            'f1': ESC + '[[A',
            'f2': ESC + '[[B',
            'f3': ESC + '[[C',
            'f4': ESC + '[[D',
            'f5': ESC + '[[E',
            'f6': ESC + '[17~',
            'f7': ESC + '[18~',
            'f8': ESC + '[19~',
            'f9': ESC + '[20~',
            'f10': ESC + '[21~',
            'f11': ESC + '[23~',
            'f12': ESC + '[24~',
        }

        KEY_TRANSLATIONS_DECCKM = {
            'up': ESC + 'OA',
            'down': ESC + 'OB',
            'right': ESC + 'OC',
            'left': ESC + 'OD',
            'f1': ESC + 'OP',
            'f2': ESC + 'OQ',
            'f3': ESC + 'OR',
            'f4': ESC + 'OS',
            'f5': ESC + '[15~',
        }
        if key.startswith("ctrl "):
            if key[-1].islower():
                key = chr(ord(key[-1]) - ord('a') + 1)
            else:
                key = chr(ord(key[-1]) - ord('A') + 1)
        else:
            if self.term_modes.keys_decckm and key in KEY_TRANSLATIONS_DECCKM:
                key = KEY_TRANSLATIONS_DECCKM.get(key)
            else:
                key = KEY_TRANSLATIONS.get(key, key)

        # ENTER transmits both a carriage return and linefeed in LF/NL mode.
        if self.term_modes.lfnl and key == "\x0d":
            key += "\x0a"

        if PYTHON3:
            key = key.encode(self.encoding, 'ignore')

        os.write(self.master, key)

class TermPop(urwid.Terminal):
    '''
    终端函数可以自主退出终端弹窗窗口
    '''
    def __init__(self, view):
        self.view = view
        urwid.set_encoding('utf8')
        self.__super.__init__(None, encoding='utf-8')  # 创建一个终端
        self.main_loop = Loop  # 这一步让终端流畅运行

    def keypress(self, size, key):

        if key == setting['short_key']['quitTerm'] :  # 判断是否为ctrl q 按钮

            Loop.widget = self.view

        if self.terminated:
            return key

        if key == "window resize":
            width, height = size
            self.touch_term(width, height)
            return

        if (self.last_key == self.escape_sequence
                and key == self.escape_sequence):
            # escape sequence pressed twice...
            self.last_key = key
            self.keygrab = True
            # ... so pass it to the terminal
        elif self.keygrab:
            if self.escape_sequence == key:
                # stop grabbing the terminal
                self.keygrab = False
                self.last_key = key
                return
        else:
            if key == 'page up':
                self.term.scroll_buffer()
                self.last_key = key
                self._invalidate()
                return
            elif key == 'page down':
                self.term.scroll_buffer(up=False)
                self.last_key = key
                self._invalidate()
                return
            elif (self.last_key == self.escape_sequence
                  and key != self.escape_sequence):
                # hand down keypress directly after ungrab.
                self.last_key = key
                return key
            elif self.escape_sequence == key:
                # start grabbing the terminal
                self.keygrab = True
                self.last_key = key
                return
            elif self._command_map[key] is None or key == 'enter':
                # printable character or escape sequence means:
                # lock in terminal...
                self.keygrab = True
                # ... and do key processing
            else:
                # hand down keypress
                self.last_key = key
                return key

        self.last_key = key

        self.term.scroll_buffer(reset=True)
        from urwid.compat import ord2, chr2, B, bytes, PYTHON3, xrange

        # EOF = B('')
        ESC = chr(27)

        KEY_TRANSLATIONS = {
            'enter': chr(13),
            'backspace': chr(127),
            'tab': chr(9),
            'esc': ESC,
            'up': ESC + '[A',
            'down': ESC + '[B',
            'right': ESC + '[C',
            'left': ESC + '[D',
            'home': ESC + '[1~',
            'insert': ESC + '[2~',
            'delete': ESC + '[3~',
            'end': ESC + '[4~',
            'page up': ESC + '[5~',
            'page down': ESC + '[6~',

            'f1': ESC + '[[A',
            'f2': ESC + '[[B',
            'f3': ESC + '[[C',
            'f4': ESC + '[[D',
            'f5': ESC + '[[E',
            'f6': ESC + '[17~',
            'f7': ESC + '[18~',
            'f8': ESC + '[19~',
            'f9': ESC + '[20~',
            'f10': ESC + '[21~',
            'f11': ESC + '[23~',
            'f12': ESC + '[24~',
        }

        KEY_TRANSLATIONS_DECCKM = {
            'up': ESC + 'OA',
            'down': ESC + 'OB',
            'right': ESC + 'OC',
            'left': ESC + 'OD',
            'f1': ESC + 'OP',
            'f2': ESC + 'OQ',
            'f3': ESC + 'OR',
            'f4': ESC + 'OS',
            'f5': ESC + '[15~',
        }
        if key.startswith("ctrl "):
            if key[-1].islower():
                key = chr(ord(key[-1]) - ord('a') + 1)
            else:
                key = chr(ord(key[-1]) - ord('A') + 1)
        else:
            if self.term_modes.keys_decckm and key in KEY_TRANSLATIONS_DECCKM:
                key = KEY_TRANSLATIONS_DECCKM.get(key)
            else:
                key = KEY_TRANSLATIONS.get(key, key)

        # ENTER transmits both a carriage return and linefeed in LF/NL mode.
        if self.term_modes.lfnl and key == "\x0d":
            key += "\x0a"

        if PYTHON3:
            key = key.encode(self.encoding, 'ignore')

        os.write(self.master, key)

class PopUpDialog(urwid.Terminal):
    #signals = ['closed']
    #term=urwid.Terminal(None,encoding='utf-8')
    def __init__(self,filename):
        urwid.set_encoding('utf8')
        with open('dir.yaml', 'r') as f:
            datas = yaml.safe_load(f)

        self.__super.__init__((setting['editor'],f'{datas["Dir"]+filename.strip("*")}'), encoding='utf-8') #创建一个终端
        self.main_loop=Loop   #这一步让终端流畅运行
    def keypress(self, size, key):
        #self.kp(size,key)
        if key == setting['short_key']['quitTerm']: #判断是否为ctrl q 按钮
           self._emit("closed")      #是的话就发出closed信号 关闭弹窗
           #self._emit("close")
        if self.terminated:
            return key

        if key == "window resize":
            width, height = size
            self.touch_term(width, height)
            return

        if (self.last_key == self.escape_sequence
            and key == self.escape_sequence):
            # escape sequence pressed twice...
            self.last_key = key
            self.keygrab = True
            # ... so pass it to the terminal
        elif self.keygrab:
            if self.escape_sequence == key:
                # stop grabbing the terminal
                self.keygrab = False
                self.last_key = key
                return
        else:
            if key == 'page up':
                self.term.scroll_buffer()
                self.last_key = key
                self._invalidate()
                return
            elif key == 'page down':
                self.term.scroll_buffer(up=False)
                self.last_key = key
                self._invalidate()
                return
            elif (self.last_key == self.escape_sequence
                  and key != self.escape_sequence):
                # hand down keypress directly after ungrab.
                self.last_key = key
                return key
            elif self.escape_sequence == key:
                # start grabbing the terminal
                self.keygrab = True
                self.last_key = key
                return
            elif self._command_map[key] is None or key == 'enter':
                # printable character or escape sequence means:
                # lock in terminal...
                self.keygrab = True
                # ... and do key processing
            else:
                # hand down keypress
                self.last_key = key
                return key

        self.last_key = key

        #self.term.scroll_buffer(reset=True)  #bug scroll_buffer为none
        from urwid.compat import ord2, chr2, B, bytes, PYTHON3, xrange

        #EOF = B('')
        ESC = chr(27)

        KEY_TRANSLATIONS = {
            'enter': chr(13),
            'backspace': chr(127),
            'tab': chr(9),
            'esc': ESC,
            'up': ESC + '[A',
            'down': ESC + '[B',
            'right': ESC + '[C',
            'left': ESC + '[D',
            'home': ESC + '[1~',
            'insert': ESC + '[2~',
            'delete': ESC + '[3~',
            'end': ESC + '[4~',
            'page up': ESC + '[5~',
            'page down': ESC + '[6~',

            'f1': ESC + '[[A',
            'f2': ESC + '[[B',
            'f3': ESC + '[[C',
            'f4': ESC + '[[D',
            'f5': ESC + '[[E',
            'f6': ESC + '[17~',
            'f7': ESC + '[18~',
            'f8': ESC + '[19~',
            'f9': ESC + '[20~',
            'f10': ESC + '[21~',
            'f11': ESC + '[23~',
            'f12': ESC + '[24~',
        }

        KEY_TRANSLATIONS_DECCKM = {
            'up': ESC + 'OA',
            'down': ESC + 'OB',
            'right': ESC + 'OC',
            'left': ESC + 'OD',
            'f1': ESC + 'OP',
            'f2': ESC + 'OQ',
            'f3': ESC + 'OR',
            'f4': ESC + 'OS',
            'f5': ESC + '[15~',
        }
        if key.startswith("ctrl "):
            if key[-1].islower():
                key = chr(ord(key[-1]) - ord('a') + 1)
            else:
                key = chr(ord(key[-1]) - ord('A') + 1)
        else:
            if self.term_modes.keys_decckm and key in KEY_TRANSLATIONS_DECCKM:
                key = KEY_TRANSLATIONS_DECCKM.get(key)
            else:
                key = KEY_TRANSLATIONS.get(key, key)

        # ENTER transmits both a carriage return and linefeed in LF/NL mode.
        if self.term_modes.lfnl and key == "\x0d":
            key += "\x0a"

        if PYTHON3:
            key = key.encode(self.encoding, 'ignore')

        os.write(self.master, key)

class ThingWithAPopUp(urwid.PopUpLauncher):
    def __init__(self,button):
        self.button=button
        self.__super.__init__(self.button)   #传递按钮对象到弹窗进行处理
        # urwid.connect_signal(self.original_widget, 'click',
        #     lambda button: self.open_pop_up())     #模拟一旦某个按钮对象收到click信号则触发弹窗
        global pop_up
        pop_up=self.open_pop_up
        #FileButton(self.open_pop_up)

    def create_pop_up(self):
        pop_up = PopUpDialog(self.button.get_label().strip().split(" ")[0])  #发送文件名到弹窗终端里
        urwid.connect_signal(pop_up, 'closed',
                             lambda button: self.close_pop_up())              #假如收到弹窗关闭信号就关闭弹窗
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':300, 'overlay_height':100}  #定位弹窗大小

class Jump_dir(urwid.WidgetWrap):
    def jumpop(self,widget):
        with open('dir.yaml', 'r') as f:
            datas = yaml.safe_load(f)
        if self.dir.get_edit_text()[-1] == '/':
            datas["Dir"]=self.dir.get_edit_text()
        else:
            datas["Dir"] = self.dir.get_edit_text()+'/'
        with open('dir.yaml', 'w') as f:
            yaml.dump(datas, f)
        # font_buttons = create_button_list(*file_dir())
        # exterfonts._set_widget_list(font_buttons)
        # global original_buttons
        # original_buttons = exterfonts._get_widget_list()
        fonts=reload_dir()
        fonts.set_focus(0)
        self.loop_widget.widget = self.view


        # change dir
    def closepop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def __init__(self, view,loop_widget):
        self.view = view
        self.loop_widget=loop_widget
        choose_dir = urwid.Text("Input Dir：\n")
        self.dir= urwid.Edit(edit_text="")
        dir=urwid.AttrWrap(self.dir, 'body')
        confirm_button = urwid.Button("Go")
        confirm= urwid.AttrWrap(confirm_button, 'button normal', 'dir button select')
        closed_button = urwid.Button("Quit")
        closed= urwid.AttrWrap(closed_button, 'button normal', 'delete')
        self.jump_list = urwid.Pile([
            choose_dir,
            dir,
            urwid.Divider(),
            urwid.Divider(),
            confirm,
            closed,
        ])
        pop_warp=urwid.LineBox(self.jump_list)
        fill = urwid.Filler(pop_warp)
        self.exit = urwid.LineBox(fill)
        urwid.AttrWrap(self.exit, 'body')
        self.loop_widget.widget = urwid.Overlay(self.exit, self.view, 'center', 62, 'middle', 20)
        urwid.connect_signal(confirm_button, 'click',
                             self.jumpop)
        urwid.connect_signal(closed_button, 'click',
                             self.closepop)

#删除文件或者目录
class Delfile(urwid.WidgetWrap):
    def  delete_file_or_dir(self,widget):
            global file_list
            files=[ f"'{i.strip('*')}'"  for i in file_list]  #给命令加上单引号用于剥夺特殊符号的含义
            files = " ".join(files)
            command_stat = os.system(f"rm -rf  {files}  ")
            if command_stat != 0:
                self.pile._get_widget_list().append(urwid.Text(' Failed! Please check permissions '))
            else:
                # file_list=[]
                # font_buttons = create_button_list(*file_dir())
                # exterfonts._set_widget_list(font_buttons)
                # global original_buttons
                # original_buttons = exterfonts._get_widget_list()
                reload_dir()
                self.loop_widget.widget = self.view
    def delpop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def __init__(self, view,loop_widget):
        self.view = view
        self.loop_widget=loop_widget
        filename_txt = urwid.Text("Delete Confirm：\n")
        self.filename = urwid.Text("")
        # for i in file_list:  #删掉列表中出现两次以上的元素
        #     counts=file_list.count(i)
        #     if counts >= 2:
        #         for ii in range(counts):
        #             file_list.remove(i)
        global file_list
        files='\n'.join(file_list)
        self.filename.set_text(files)
        filename=urwid.AttrWrap(self.filename, 'body')
        delete_button = urwid.Button("Delete")
        del_button=urwid.AttrWrap(delete_button, 'button normal', 'dir button select')
        close_button = urwid.Button("Quit")
        closed_button = urwid.AttrWrap(close_button, 'button normal', 'delete')
        self.pile = urwid.Pile([
                          filename_txt,
                           filename,
                           urwid.Divider(),
                           urwid.Divider(),
                           del_button,
                           closed_button])
        pop_warp=urwid.LineBox(self.pile)
        fill = urwid.Filler(pop_warp)
        self.exit = urwid.LineBox(fill)
        urwid.AttrWrap(self.exit, 'body')
        self.loop_widget.widget = urwid.Overlay(self.exit, self.view, 'center', 62, 'middle', 32)
        urwid.connect_signal(delete_button, 'click',
                             self.delete_file_or_dir)
        urwid.connect_signal(close_button, 'click',
                             self.delpop)
#压缩文件
class Zipfile(urwid.WidgetWrap):

    def  zip_file_or_dir(self,widget):
            for i in self.bgroup:
                if i.state == True:
                    suffix = i.get_label()
            global file_list
            files=[ f"'{i.strip('*')}'"  for i in file_list]  #给命令加上单引号用于剥夺特殊符号的含义
            files = " ".join(files)
            dirname=self.Dir.get_edit_text()
            zipname=self.zipname.get_edit_text()
            if suffix == 'tgz' or suffix ==  'tar.gz':
                compress_command=os.system(f"tar -zcf  {dirname}{zipname}.{suffix}  {files}")
            elif suffix == 'rar':
                check_rar = os.system(f"rar -v 2> /dev/null")
                #os.system(f" echo '{check_rar}' >> 123")
                if check_rar != 0:
                    self.pile._get_widget_list().append(urwid.Text(' Not install rar!'))
                    compress_command=1
                else:
                    compress_command = os.system(f"rar a  {dirname}{zipname}.{suffix}  {files}")
            elif suffix == 'zip':
                check_rar = os.system(f"zip -v 2> /dev/null")
                if check_rar != 0:
                    self.pile._get_widget_list().append(urwid.Text(' Not install Zip!'))
                    compress_command = 1
                else:
                    compress_command = os.system(f"zip -q -r  {dirname}{zipname}.{suffix}  {files}")
            elif suffix == 'tar':
                compress_command = os.system(f"tar -cf  {dirname}{zipname}.{suffix}  {files}")

            if compress_command != 0:

                    # self.pile._get_widget_list()[-1] = urwid.Text(' Compress Failed!')
                    self.pile._get_widget_list().append(urwid.Text(' Compress Failed!'))

            else:
                # file_list=[]
                # font_buttons = create_button_list(*file_dir())
                # exterfonts._set_widget_list(font_buttons)
                # global original_buttons
                # original_buttons = exterfonts._get_widget_list()
                reload_dir()
                self.loop_widget.widget = self.view

    def zipop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def __init__(self, view,loop_widget):
        self.view = view
        self.loop_widget=loop_widget
        filename_txt = urwid.Text("Compress these files：\n")
        self.filename = urwid.Text("")
        global file_list
        files='\n'.join(file_list)
        self.filename.set_text(files)
        filename=urwid.AttrWrap(self.filename, 'body')

        with open('dir.yaml','r') as f:
            datas=yaml.safe_load(f)
        dir_name = urwid.Text('Save:')
        self.Dir = urwid.Edit(edit_text=datas["Dir"])  #目录
        Dir = urwid.AttrWrap(self.Dir, 'body')
        zip_name_txt=urwid.Text('Package name')
        self.zipname = urwid.Edit("")                 #压缩名
        zipname = urwid.AttrWrap(self.zipname, 'body')
        self.bgroup = []
        choose = urwid.Text("Choose mode：\n")
        tar= urwid.RadioButton(self.bgroup, 'tar')
        tar_gz=urwid.RadioButton(self.bgroup, 'tar.gz')
        tgz=urwid.RadioButton(self.bgroup, 'tgz')
        zip=urwid.RadioButton(self.bgroup, 'zip')
        #bzip2 = urwid.RadioButton(self.bgroup, 'bzip2')
        rar=urwid.RadioButton(self.bgroup, 'rar')
        compress_button = urwid.Button("Compress")
        compress=urwid.AttrWrap(compress_button, 'button normal', 'dir button select')
        close_button = urwid.Button("Quit")
        closed_button = urwid.AttrWrap(close_button, 'button normal', 'delete')
        self.pile = urwid.Pile([
            filename_txt,
            filename,
            urwid.Divider(),
            zip_name_txt,
            zipname,
            urwid.Divider(),
            dir_name,
            Dir,
            urwid.Divider(),
            choose,
            tar,tar_gz,tgz,rar,zip,
            urwid.Divider(),
            compress,
            closed_button])
        pop_warp=urwid.LineBox(self.pile)
        fill = urwid.Filler(pop_warp)
        self.exit = urwid.LineBox(fill)
        urwid.AttrWrap(self.exit, 'body')
        self.loop_widget.widget = urwid.Overlay(self.exit, self.view, 'center', 62, 'middle', 32)
        urwid.connect_signal(compress_button, 'click',
                             self.zip_file_or_dir)
        urwid.connect_signal(close_button, 'click',
                             self.zipop)

#创建文件或者目录
class TouchFile(urwid.WidgetWrap):
    signals = ['close']
    def delpop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def touch_file_or_dir(self,widget):
        for i in self.bgroup:
            if i.state == True:
                file_or_dir=i.get_label()
        if self.Dir.get_text()[0].strip()[-1] == '/':
            dir_path = self.Dir.get_text()[0].strip()[:-1]
        else:
            dir_path = self.Dir.get_text()[0].strip()
        if file_or_dir =='File':
           #os.system(f"echo '{dir_path}' > 1234 ")
            command_stat=os.system(f"touch '{dir_path}/{self.filename.get_text()[0]}' 2> /dev/null ")
        else:
            command_stat = os.system(f"mkdir -p '{dir_path}/{self.filename.get_text()[0]}' 2> /dev/null ")
        if command_stat!=0:
            self.pile._get_widget_list().append(urwid.Text(' Failed! Please check permissions or dir not exist '))
        else:
            # font_buttons = create_button_list(*file_dir())
            # exterfonts._set_widget_list(font_buttons)
            # global original_buttons
            # original_buttons = exterfonts._get_widget_list()
            reload_dir()
            self.loop_widget.widget = self.view

    def __init__(self, view,loop_widget):
        self.view = view
        self.loop_widget=loop_widget
        self.bgroup = []
        choose = urwid.Text("File or Dir：\n")
        fileradio = urwid.RadioButton(self.bgroup,'File')
        dirradio= urwid.RadioButton(self.bgroup, 'Dir')

        filename_txt=urwid.Text("Name：\n")
        Dir_txt=urwid.Text("Location：\n")
        with open('dir.yaml','r') as f:
            datas=yaml.safe_load(f)
        self.Dir=urwid.Edit(edit_text=datas["Dir"])
        Dir = urwid.AttrWrap(self.Dir, 'body')
        self.filename = urwid.Edit("")
        filename=urwid.AttrWrap(self.filename, 'body')
        touch_button = urwid.Button("Create")
        #delete

        create_button=urwid.AttrWrap(touch_button, 'button normal', 'dir button select')
        # urwid.AttrWrap(self.exit, 'body')
        close_button = urwid.Button("Quit")
        closed_button = urwid.AttrWrap(close_button, 'button normal', 'delete')
        self.pile = urwid.Pile([choose,

            fileradio,dirradio,urwid.Divider(),
                          filename_txt,
                           filename,
                           urwid.Divider(),
                           Dir_txt,
                           Dir,
                           urwid.Divider(),
                           urwid.Divider(),
                           create_button,
                           closed_button])
        pop_warp=urwid.LineBox(self.pile)
        fill = urwid.Filler(pop_warp)
        self.exit = urwid.LineBox(fill)
        urwid.AttrWrap(self.exit, 'body')
        self.loop_widget.widget = urwid.Overlay(self.exit, self.view, 'center', 60, 'middle', 20)

        urwid.connect_signal(touch_button, 'click',
                             self.touch_file_or_dir)
        urwid.connect_signal(close_button, 'click',
                             self.delpop)


class Chmod(urwid.WidgetWrap):
    signals = ['close']
    def delpop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def chmod_file_or_dir(self,widget):
        # for i in self.bgroup:
        #     if i.state == True:
        #         file_or_dir=i.get_label()
        # if self.Dir.get_text()[0].strip()[-1] == '/':
        #     dir_path = self.Dir.get_text()[0].strip()[:-1]
        # else:
        #     dir_path = self.Dir.get_text()[0].strip()
        with open('dir.yaml','r') as f:
            datas=yaml.safe_load(f)
        dir_path=datas['Dir']

        self.chmod_name=self.chmod_name.strip('*')


        def permission_change(permit):
            chmod_str = ""
            for i in permit:
                num = 0
                if i[0]: #read
                    num = num + 4
                if i[1]:  #write
                    num = num + 2
                if i[2]:  #exe
                    num = num + 1
                chmod_str=chmod_str+str(num)
            return chmod_str


        update_permit=[
        [self.owner_read.get_state(),self.owner_write.get_state(),self.owner_execute.get_state()],
        [self.group_read.get_state(),self.group_write.get_state(),self.owner_execute.get_state()],
        [self.others_read.get_state(),self.others_write.get_state(),self.others_execute.get_state()]
         ]

        permit_num=permission_change(update_permit)
        #os.system(f"echo '{permit_num}' > 123")
        chmod_command = os.system(f"chmod  {permit_num} '{dir_path}{self.chmod_name}' 2> /dev/null ")
        chown_command=os.system(f"chown '{self.user.get_text()[0].strip()}' '{dir_path}{self.chmod_name}' 2> /dev/null ")
        chgrp_command = os.system( f"chgrp  '{self.grouper.get_text()[0].strip()}'  '{dir_path}{self.chmod_name}' 2> /dev/null ")
        if chown_command!=0 or chmod_command!=0 or chgrp_command !=0:
            self.pile._get_widget_list().append(urwid.Text(' Failed! Do you have root permission or the user exist?'))
        else:
            reload_dir()
            self.loop_widget.widget = self.view

    def __init__(self, view,loop_widget,chmod_name,user_group,permission):
        def split_permission(permission):
            process_permissions = {'read': False, 'write': False, 'exe': False}
            if '-' not in permission:
                process_permissions = {'read': True, 'write': True, 'exe': True, }
                return process_permissions
            if 'r' in permission:
                process_permissions['read']=True
            if 'w' in permission:
                process_permissions['write']=True
            if 'x' in permission:
                process_permissions['exe']= True
            return process_permissions

        self.chmod_name=chmod_name
        self.view = view
        self.loop_widget=loop_widget
        self.ownerlist = []



        owner = urwid.Text("Owner：\n")
        self.own_pms=split_permission(permission[0:3])
        self.owner_read = urwid.CheckBox('Read',self.own_pms['read'])
        self.owner_write= urwid.CheckBox('Write',self.own_pms['write'])
        self.owner_execute = urwid.CheckBox('Execute', self.own_pms['exe'])


        # os.system(f"echo '{owner_read.get_state()}' > 123")

        group=urwid.Text("Group：\n")
        self.group_pms = split_permission(permission[3:6])
        self.group_read = urwid.CheckBox('Read', self.group_pms['read'])
        self.group_write = urwid.CheckBox('Write', self.group_pms['write'])
        self.group_execute = urwid.CheckBox('Execute', self.group_pms['exe'])


        others = urwid.Text("Others：\n")
        self.other_pms = split_permission(permission[6:9])
        self.others_read = urwid.CheckBox('Read', self.other_pms['read'])
        self.others_write = urwid.CheckBox('Write', self.other_pms['write'])
        self.others_execute = urwid.CheckBox('Execute',self.other_pms['exe'])


        user=urwid.Text('User:')

        self.user= urwid.Edit(edit_text=user_group.split('/')[0])
        filename=urwid.AttrWrap(self.user, 'body')
        change_button = urwid.Button("Change")
        chmod_button = urwid.AttrWrap(change_button, 'button normal', 'dir button select')
        #delete
        grouper = urwid.Text('Group:')
        self.grouper = urwid.Edit(edit_text=user_group.split('/')[1])
        grouper_text = urwid.AttrWrap(self.grouper, 'body')

        # urwid.AttrWrap(self.exit, 'body')
        close_button = urwid.Button("Quit")
        closed_button = urwid.AttrWrap(close_button, 'button normal', 'delete')
        self.pile = urwid.Pile([owner,

            self.owner_read,self.owner_write,self.owner_execute,urwid.Divider(),
            group,self.group_read,self.group_write,self.group_execute,urwid.Divider(),
            others,self.others_read,self.others_write,self.others_execute,
                                user,
                           filename,
                                grouper,
                                grouper_text,
                           urwid.Divider(),
                           urwid.Divider(),
                           chmod_button,
                           closed_button])
        self.pile.set_focus(15)
        pop_warp=urwid.LineBox(self.pile)
        fill = urwid.Filler(pop_warp)
        self.exit = urwid.LineBox(fill)
        urwid.AttrWrap(self.exit, 'body')
        self.loop_widget.widget = urwid.Overlay(self.exit, self.view, 'center', 80, 'middle', 40)

        urwid.connect_signal(change_button, 'click',
                             self.chmod_file_or_dir)
        urwid.connect_signal(close_button, 'click',
                             self.delpop)


class BigTextDisplay:
    palette = [

        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'brown',   'bold'),
        ('button normal','light gray', 'dark gray', 'standout'),
        ('file button select','white',      'dark blue'),
        ('dir button select', 'white', 'dark green'),
        ('button disabled','dark gray','dark blue'),
        ('edit',         'light gray', 'black'),
        # ('bigtext',      'black',      'dark magenta'),
        ('chars',        'light gray', 'black'),
        # ('chars_bg', 'light gray', 'dark magenta'),
        ('exit',         'white',      'dark cyan'),
        ('delete', 'black', 'dark red'),
        ('select', 'black', 'yellow'),
        ]
    try:
        skin=setting['choose_skin']
        palette.append(setting['skin'][skin]['bigtext'])  #
        palette.append(setting['skin'][skin]['chars_bg'])
    except:
        palette.append(setting['skin']['gray_black']['bigtext'])
        palette.append(setting['skin']['gray_black']['chars_bg'])

    def create_disabled_radio_button(self, name):
        w = urwid.Text("    " + name + " (UTF-8 mode required)")
        w = urwid.AttrWrap(w, 'button disabled')
        return w

    def create_edit(self, label, text, fn):
        edit = urwid.Edit(label, text)
        urwid.connect_signal(edit, 'change', fn)
        #fn(w)
        w = urwid.AttrWrap(edit, 'edit')
        return w

    def set_font_event(self, w, state):
        if state:
            self.bigtext.set_font(w.font)
            self.chars_avail.set_text(w.font.characters())
    
    def edit_change_event(self, widget,label):
        '''
        
        :param widget: 传入widget对象
        :param label: 用户的筛选输入
        :return: None
        '''
        # self.bigtext.set_text(text)
        font_buttons = []
        global original_buttons
        for buttons in original_buttons:
            try:
                button_label = buttons.get_w().get_label()
            except:
                try:
                    button_label = buttons.get_w().original_widget.get_label()
                except:  #
                    button_label = ''#当上面都失败就是标志着未找到匹配项置为空
            #os.system(f"echo {button_label} >> 123")
            #
            import re
            if re.findall(f'(.*{label}.*)', button_label,re.IGNORECASE):  #匹配项目会出现在列表如匹配apache 列表为['apache']
                font_buttons.append(buttons)
        if font_buttons==[]:                  #在没有匹配项时添加两个空白的文件按钮
            font_buttons=[urwid.Button(''),urwid.Button(' ')]
        exterfonts._set_widget_list(font_buttons) #exterfonts外部来配置
        # original_buttons = self.fonts._get_widget_list()


        # urwid.AttrWrap.set_w

    def create_button(self):
        font_buttons = []
        global exterfonts
        font_buttons=create_button_list(*file_dir())
        chars = urwid.Divider()
        #os.system(f'echo {len(font_buttons)} > 123')
        self.fonts = urwid.Pile(font_buttons)
        global original_buttons
        original_buttons=self.fonts._get_widget_list()  #使用全局变量来承载创建时的所有按钮的原始列表，在变换字符的同时保证都是对原始目录的筛选，避免删除字符无法回退到之前目录下

        #os.system(f"echo {type(self.fonts)} > 123")
        #os.system(f"echo '{original_buttons._get_widget_list()}' > 123")

        exterfonts=self.fonts    #传递给外部函数或者全局需要使用self.fonts的地方
        self.col = urwid.Columns([('fixed', 0, chars), self.fonts], 0,
                            focus_column=1)




    def setup_view(self):
        fonts = urwid.get_all_fonts()
        # setup mode radio buttons

        #print(rb)
        for name, fontcls in fonts:
            font = fontcls()
            #self.create_radio_button(name)
            if fontcls == urwid.HalfBlock5x4Font:  #匹配标题字体输出
                #print(font)
                exit_font = font


        # Create BigText

        self.bigtext = urwid.BigText("Lin v1.0",exit_font)

        bt = SwitchingPadding(self.bigtext, 'left',None,left=6)

        bt = urwid.AttrWrap(bt, 'bigtext')

        bt = urwid.Filler(bt, 'middle',None)


#sed 可替换
        oper=(
            u'Ctrl+a  Copy the file contents ',
            u'Ctrl+w  Quit to destop',
            u'Ctrl+t  Term',
            u'Ctrl+q  Quit to Term',
            u'Ctrl+r  refresh',
            u'Ctrl+n  Create a file',
            u'Ctrl+d  Delete selected files',
            u'space   Selected files',
            u'?       Help'
        )

        controll_list=urwid.SimpleListWalker(
            ctrl_opeater(oper)
        )
        controll_list=urwid.ListBox(controll_list)
        controll_list = urwid.AttrMap(controll_list,'chars_bg')  #添加颜色属性
        controll_list = urwid.Padding(controll_list, 'right', left=10)  #增加左右偏移


        #ip = urwid.Text(f'192.168.1.1 :IP',align='right')
        self.cpu = urwid.Text(f'24% :Cpu',align='right')
        self.mem = urwid.Text(f'30% :Mem',align='right')
        self.In = urwid.Text(f' ',align='right')
        self.dates=urwid.Text(f'2022-01-01 01:01',align='right')
        info=urwid.SimpleListWalker([
            urwid.Divider(),
            self.cpu,
            self.mem,
            urwid.Divider(),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Divider(),
            self.In,
            self.dates,
        ])

        info=urwid.ListBox(info)
        info = urwid.AttrMap(info, 'chars_bg')
        system_info=urwid.Padding(info,align='right',width=('relative',80))

        #system_contorl = SwitchingPadding(system_info, 'right', None, left=4)
        files = urwid.Columns([bt,controll_list,system_info],0, focus_column=1)  #第一行的格局配置
        bt = urwid.BoxAdapter(files,10)
        bt = urwid.LineBox(bt)
        bt = urwid.AttrWrap(bt,'bigtext')


        # Create chars_avail

        #cah = urwid.Text("Characters Available:")
        self.chars_avail = urwid.Text("", wrap='any')
        #ca = urwid.AttrWrap(self.chars_avail, 'chars')

        #chosen_font_rb.set_state(True) # causes set_font_event call

        # Create Edit widget


        # ListBox
        self.create_button()
        edit = self.create_edit("", "",
                                self.edit_change_event)

        self.bt = urwid.Pile([bt, edit], focus_item=1)

        files = urwid.Text(f"   文件名称{count_str('文件名称')}用户/组{count_str('用户/组')}权限大小{count_str('权限大小')}文件大小{count_str('文件大小')}创建时间{count_str('创建时间')}")
        #pb = urwid.ProgressBar('Begin', 'END') #进度条
        last=urwid.Text(u' ')
        last=urwid.AttrMap(last,'edit')

        #fill = urwid.Padding(ThingWithAPopUp(), 'center',15)
        #fill=urwid.LineBox(fill)

        l = [self.bt,files,self.col,last]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        w = urwid.AttrWrap(w, 'body')
        hdr = urwid.Text("Lin v1.0 - F8 exits.")
        hdr = urwid.AttrWrap(hdr, 'header')
        w = urwid.Frame(header=hdr, body=w)

        # Exit message

        exit = urwid.BigText(('exit'," Quit? "), exit_font)
        exit = urwid.Overlay(exit, w, 'center', None, 'middle', None)

        return w, exit
    def change_data(self):
        while True:
            time.sleep(1)
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            self.In.set_text(f'【 {datas["Dir"]} 】：Location')
            dateTime_p = datetime.datetime.now()
            str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
            self.dates.set_text(str_p)
            self.cpu.set_text(str(psutil.cpu_percent(None))+'% :Cpu')
            self.mem.set_text(str(psutil.virtual_memory().percent) + '% :Mem')
            self.loop.draw_screen()


    def main(self):
        self.view, self.exit_view = self.setup_view()
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_input,pop_ups=True,handle_mouse=setting['mouse'])  #handle_mouse 开启鼠标点选模式，默认为真不能使用复制粘贴功能
        global Loop
        Loop=self.loop
        global views
        views=self.view
        threading.Thread(target=self.change_data, args=()).start()
        self.loop.run()



    def unhandled_input(self, key):
        self.copy=False
        global file_list
        global original_buttons
        # if key == 'M':
        #     pass
        # if key == 'G':
        #     pass
        # if key == 'S':
        #     pass

        if key == setting['short_key']['goTo']:
            Jump_dir(self.view,self.loop)
            file_list = []
            return


        if key == setting['short_key']['copyFile']:  # C
            font_buttons = create_button_list(*file_dir())
            self.fonts._set_widget_list(font_buttons)
            original_buttons = self.fonts._get_widget_list()
            self.copy_file_list=file_list
            file_list = []
            self.copy=True
            return
        if key == setting['short_key']['cut']: # X
            font_buttons = create_button_list(*file_dir())
            self.fonts._set_widget_list(font_buttons)
            original_buttons = self.fonts._get_widget_list()
            self.copy_file_list=file_list
            # os.system(f"echo '{self.copy_file_list}' > 123")
            file_list = []
            self.copy=False
            return
        if key == setting['short_key']['pasteFile']:  #复用
            try:
                with open('dir.yaml', 'r') as f:
                    datas = yaml.safe_load(f)
                current_path = datas['Dir']
                if self.copy_file_list!=[] and self.copy:
                    for file_path in self.copy_file_list:  #可以加入进度条模式
                        os.system(f"cp -af '{file_path.strip('*')}' '{current_path}' 2> /dev/null")
                elif  self.copy_file_list!=[] and self.copy==False:
                    for file_path in self.copy_file_list:  #可以加入进度条模式
                        os.system(f"mv '{file_path.strip('*')}' '{current_path}' 2> /dev/null")
                else:
                    return
                # font_buttons = create_button_list(*file_dir())
                # self.fonts._set_widget_list(font_buttons)
                # original_buttons = self.fonts._get_widget_list()
                # self.copy_file_list = file_list
                reload_dir()
            except:
                pass
            return
        if key == setting['short_key']['zip']:
            Zipfile(self.view,self.loop)
            return

        if key == setting['short_key']['deleteFile']:  #ctrl d
            Delfile(self.view,self.loop)
            return
        if key == setting['short_key']['createFile']:  #ctrl n
            TouchFile(self.view,self.loop)
            return
        if key == setting['short_key']['backdir']:  #回退目录重新读取按钮们

            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            Dir=[ii for ii in datas['Dir'].split('/') if (len(str(ii)) != 0)]

            with open('dir.yaml', 'w') as f:
                if Dir!=[]: #如果Dir不是根号的话，就进行目录处理
                    datas['Dir'] ='/'+'/'.join(Dir[:-1])+'/'   # 修复bug-102
                    if datas['Dir'] == '//':               #退到最后一个目录时由于头尾相加会造成//
                        datas['Dir'] = '/'
                    #datas['Dir'] = datas['Dir'].replace(Dir[-1]+'/','')  # bug-102: 下级目录中如果有同名目录会全部删除
                yaml.dump(datas, f)
            # font_buttons=create_button_list(*file_dir())
            # self.fonts._set_widget_list(font_buttons)
            # self.fonts.set_focus(0) #筛选回退显示在第一个上
            # #global file_list
            # file_list = []
            # original_buttons = self.fonts._get_widget_list()
            fonts=reload_dir()
            fonts.set_focus(0)
        if key == setting['short_key']['term']:
            '''
            按键ctrl+t 召唤终端使用overload覆盖层的方式让终端浮于view层上
            '''
            urwid.set_encoding('utf8')
            term=TermPop(self.view)
            exit = urwid.LineBox(term)
            exit = urwid.Overlay(exit, self.view, 'center', 300, 'middle', 300)  #这里300和300不设置会报错
            self.loop.widget = exit
            return

        if key == setting['short_key']['refresh']:  #刷新
            reload_dir()
            return
        if key == '?':
            def fn(view,loop,new):  #这里的传参为顺序传参 传多个参数最后一个一直都是要操作的对象 这里是button
                loop.widget=view
            #help_info=urwid.Text('Command Help')  #需要制作退出按钮

            quit_button = urwid.Button('Quit')
            urwid.connect_signal(quit_button,'click',fn,weak_args=[self.view,self.loop]) #传参数给fn函数
            #quit_button=urwid.Filler(quit_button,'top')
            self.oper = (
                u'Shortcuts Documentation:',
                ' ',
                u'    Ctrl+r  Refresh',
                u'    Ctrl+s  Compress a dir',
                u'    Ctrl+a  Copy the file contents ',
                u'    Ctrl+w  Quit to destop',
                u'    Ctrl+t  Term',
                u'    Ctrl+q  Quit to Term',
                u'    Ctrl+r  refresh',
                u'    Ctrl+n  Create a file',
                u'    Ctrl+d  Delete selected files',
                u'    shift+c  Copy selected files',
                u'    shift+v  Paste file',
                u'    shift+x  Cut selected file',
                u'    shift+o  Go to the directory' ,
                u'    space  selected files',
                u'    Ctrl+esc  Cancel selected files',
                u'    Esc  back to upper level directory ',
                ' ',
                u'?       Help',

            )
            l = ctrl_opeater(self.oper)
            l[-1] = quit_button
            help_info = urwid.ListBox(urwid.SimpleListWalker(l))
            help_info = urwid.Overlay(help_info, self.view, 'center', 300, 'middle', 300)  # 这里300和300不设置会报错
            self.loop.widget = help_info
            return
        #if key == 'f8':
        if key == setting['short_key']['quitDestop']:
            self.loop.widget = self.exit_view
            return True
        if self.loop.widget != self.exit_view:
            return
        if key in ('y', 'Y'):
            raise urwid.ExitMainLoop()
        if key in ('n', 'N'):
            self.loop.widget = self.view
            return True

def main():
    urwid.Button.button_left = urwid.Text("|")
    urwid.Button.button_right =urwid.Text("|")
    BigTextDisplay().main()

if '__main__'==__name__:
    main()