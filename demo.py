import urwid
import threading
import  time
import os,sys
import datetime
import psutil
import yaml
import pyperclip

Loop=None
exterfonts=None
ed='vi'
mouse=False
original_buttons=None
delete_list=[]



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
    # getFileInfo('/home/wlw/PycharmProjects/pythonProject')
    with open('dir.yaml', 'r') as f:
        datas = yaml.safe_load(f)
    output = os.popen(f'ls -lAhF {datas["Dir"]}')
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
        else:
            file.append(output_list)
    return file, dir
def create_button_list(file, dir):
    font_buttons=[]
    '''
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

def create_dir_button(name):
    #w = urwid.RadioButton(g, name, False, on_state_change=fn)
    if name!=' ':

        if name[-2] == '->':
           # os.system(f'echo {name} >> 123')
            file = name[-1] + ' ' + name[-2] +' ' + name[-3]
        else:
           # os.system(f'echo {name} >> 123')
            file = name[-1]
        user_group=name[2]+'/'+name[3]
        chmod=name[0]
        file_size=name[4]
        dates=name[5]+name[6]+'日'+' '+name[7]
        w=DirButton(f' {file[:30]}{count_str(file[:30])}{user_group}{count_str(user_group)}{chmod}{count_str(chmod)}{file_size}{count_str(file_size)}{dates}')
        w=w.create_appwarp(w)
    else:
        w = urwid.Button(' ')
        w = urwid.AttrWrap(w,'button normal', 'dir button select')
    #os.system(f"echo '{w.set_focus_attr()} '> 123")
    return w
def create_file_button(name):
    if name != ' ':
        if name[-2] == '->':
            file = name[-1] + ' ' + name[-2] +' ' + name[-3]
        else:
            file = name[-1]
        user_group = name[2] + '/' + name[3]
        chmod = name[0]
        file_size = name[4]
        dates = name[5] + name[6] + '日' + ' ' + name[7]
        Attrwarp=FileButton(
            f' {file[:30]}{count_str(file[:30])}{user_group}{count_str(user_group)}{chmod}{count_str(chmod)}{file_size}{count_str(file_size)}{dates}')
        w = ThingWithAPopUp(Attrwarp)
        w = Attrwarp.create_appwarp(w)

    else:
        w = urwid.Button(' ')
        w = urwid.AttrWrap(w, 'button normal', 'file button select')
    return w


#同种button按钮的按键可以做到不一样的效果
class DirButton(urwid.Button):

    def create_appwarp(self,w):
        self.attrwarp=urwid.AttrWrap(w,'button normal', 'dir button select')
        return self.attrwarp


    def keypress(self, size, key):
        if key in ('enter',) :
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            with open('dir.yaml', 'w') as f:
                datas['Dir']=datas["Dir"] + self.label.strip().split(" ")[0]
                yaml.dump(datas,f)
                #os.system(f'ls -alh {datas["Dir"]}{self.label.strip().split(" ")[0]} > file.txt')
            font_buttons = create_button_list(*file_dir())
            global exterfonts
            exterfonts._set_widget_list(font_buttons)
            global original_buttons
            original_buttons = exterfonts._get_widget_list()
            self._emit('click')
        elif key == ' ':  #空格选取
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+self.label.strip().split(" ")[0]
            #os.system(f"echo '{delete_list}' >> 123")
            if self.attrwarp.get_attr() == 'select':
                self.attrwarp.set_attr('button normal')
                delete_list.remove(file_path)
            else:
                self.attrwarp.set_attr('select')
                delete_list.append(file_path)
        elif key =='ctrl esc':
            self.attrwarp.set_attr('dir button select')
                #urwid.AttrWrap(self,'button normal', 'delete')
        else:
            return key


class FileButton(urwid.Button):
    # def __init__(self, abc):
    #     self.abc = abc
    def create_appwarp(self, w):
        self.attrwarp = urwid.AttrWrap(w, 'button normal', 'file button select')
        return self.attrwarp

    def keypress(self, size, key):
        if key in ('ctrl p',) :
            os.system(f'echo {self.label.strip().split(" ")[-1]} > wulinwei1.py')
        elif  key == 'ctrl a':  # 一键复制文件内容
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+self.label.strip().split(" ")[0]
            with open(f'{file_path}') as f:
                file_content = f.read()
            pyperclip.copy(file_content)
        elif key in ('enter',):   #点击文件按钮发送click信号给按钮本身 模拟点击操作
            self._emit('click')
        elif key == ' ':
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            file_path=datas['Dir']+self.label.strip().split(" ")[0]
            #os.system(f"echo '{delete_list}' >> 123")
            if self.attrwarp.get_attr()=='select':
                self.attrwarp.set_attr('button normal')
                delete_list.remove(file_path)
            else:
                self.attrwarp.set_attr('select')
                delete_list.append(file_path)
        elif key =='ctrl esc':
            self.attrwarp.set_attr('file button select')
        else:
            return key


class Termpop(urwid.Terminal):
    '''
    终端函数可以自主退出终端窗口
    '''
    def __init__(self, view):
        self.view = view
        urwid.set_encoding('utf8')
        self.__super.__init__(None, encoding='utf-8')  # 创建一个终端
        self.main_loop = Loop  # 这一步让终端流畅运行

    def keypress(self, size, key):

        if key in ('ctrl q',):  # 判断是否为ctrl q 按钮

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

    """A dialog that appears with nothing but a close button """
    #signals = ['closed']
    #term=urwid.Terminal(None,encoding='utf-8')

    def __init__(self,filename):
        urwid.set_encoding('utf8')
        with open('dir.yaml', 'r') as f:
            datas = yaml.safe_load(f)

        self.__super.__init__((ed,f'{datas["Dir"]+filename}'), encoding='utf-8') #创建一个终端
        self.main_loop=Loop   #这一步让终端流畅运行
    def keypress(self, size, key):
        #self.kp(size,key)
        if key in ('ctrl q',):      #判断是否为ctrl q 按钮
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

        self.term.scroll_buffer(reset=True)
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
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())     #模拟一旦某个按钮对象收到click信号则触发弹窗
        #FileButton(self.open_pop_up)

    def create_pop_up(self):
        pop_up = PopUpDialog(self.button.get_label().strip().split(" ")[0])  #发送文件名到弹窗终端里
        urwid.connect_signal(pop_up, 'closed',
                             lambda button: self.close_pop_up())              #假如收到弹窗关闭信号就关闭弹窗
        return pop_up



    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':300, 'overlay_height':100}  #定位弹窗大小

#删除文件或者目录
class Delfile(urwid.WidgetWrap):
    def  delete_file_or_dir(self,widget):

            file_list = ' '.join(delete_list)
                # os.system(f"echo '{dir_path}' > 1234 ")
            command_stat = os.system(f"rm -rf  '{file_list}' 2> /dev/null ")
            if command_stat != 0:
                self.pile._get_widget_list().append(urwid.Text(' Failed! Please check permissions '))
            else:
                font_buttons = create_button_list(*file_dir())
                #exterfonts = self.fonts
                exterfonts._set_widget_list(font_buttons)
                self.loop_widget.widget = self.view
    def delpop(self,widget):
        urwid.Overlay( self.view,self.exit, 'center', 30000, 'middle', 30000)  # 这里300和300不设置会报错 center 为宽度 middle为高度
        self.loop_widget.widget = self.view
    def __init__(self, view,loop_widget):
        self.view = view
        self.loop_widget=loop_widget
        filename_txt = urwid.Text("Delete Confirm：\n")
        self.filename = urwid.Text("")
        # for i in delete_list:
        #     counts=delete_list.count(i)
        #     if counts >= 2:
        #         for ii in range(counts):
        #             delete_list.remove(i)
        file_list='\n'.join(delete_list)
        self.filename.set_text(file_list)
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
            font_buttons = create_button_list(*file_dir())
            exterfonts._set_widget_list(font_buttons)
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








class BigTextDisplay:
    palette = [

        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'brown',   'bold'),
        ('button normal','light gray', 'dark gray', 'standout'),
        ('file button select','white',      'dark blue'),
        ('dir button select', 'white', 'dark green'),
        ('button disabled','dark gray','dark blue'),
        ('edit',         'light gray', 'black'),
        ('bigtext',      'black',      'dark magenta'),
        ('chars',        'light gray', 'black'),
        ('chars_bg', 'light gray', 'dark magenta'),
        ('exit',         'white',      'dark cyan'),
        ('delete', 'black', 'dark red'),
        ('select', 'black', 'yellow'),
        ]




    def create_disabled_radio_button(self, name):
        w = urwid.Text("    " + name + " (UTF-8 mode required)")
        w = urwid.AttrWrap(w, 'button disabled')
        return w

    def create_edit(self, label, text, fn):
        w = urwid.Edit(label, text)
        urwid.connect_signal(w, 'change', fn)
        #fn(w)
        w = urwid.AttrWrap(w, 'edit')
        return w

    def set_font_event(self, w, state):
        if state:
            self.bigtext.set_font(w.font)
            self.chars_avail.set_text(w.font.characters())

    def edit_change_event(self, widget,label):
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
            if re.findall(f'(.*{label}.*)', button_label):  #匹配项目会出现在列表如匹配apache 列表为['apache']
                font_buttons.append(buttons)
        if font_buttons==[]:                  #没有匹配项时添加两个空白的按钮
            font_buttons=[urwid.Button(''),urwid.Button(' ')]
        self.fonts._set_widget_list(font_buttons)


        # urwid.AttrWrap.set_w

    def create_button(self):
        font_buttons = []
        global exterfonts
        font_buttons=create_button_list(*file_dir())
        chars = urwid.Divider()
        #os.system(f'echo {len(font_buttons)} > 123')
        self.fonts = urwid.Pile(font_buttons,
                            focus_item=1)
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
            u'Ctrl+r  Refresh',
            u'Ctrl+c  Copy files',
            u'Ctrl+v  Paste file',
            u'Ctrl+x  Unzip file',
            u'Ctrl+s  Compress a dir',
            u'Ctrl+t  Term',
            u'Ctrl+a  Copy file contents ',
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
        bt = urwid.Pile([bt, edit], focus_item=1)
        files = urwid.Text(f"   文件名称{count_str('文件名称')}权限大小{count_str('权限大小')}用户/组{count_str('用户/组')}文件大小{count_str('文件大小')}创建时间{count_str('创建时间')}")
        #pb = urwid.ProgressBar('Begin', 'END') #进度条
        last=urwid.Text(u' ')
        last=urwid.AttrMap(last,'edit')

        #fill = urwid.Padding(ThingWithAPopUp(), 'center',15)
        #fill=urwid.LineBox(fill)

        l = [bt,files,self.col,last]
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
            self.In.set_text(f'【{datas["Dir"]}】：Location')
            dateTime_p = datetime.datetime.now()
            str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
            self.dates.set_text(str_p)
            self.cpu.set_text(str(psutil.cpu_percent(None))+'% :Cpu')
            self.mem.set_text(str(psutil.virtual_memory().percent) + '% :Mem')
            self.loop.draw_screen()


    def main(self):
        self.view, self.exit_view = self.setup_view()
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_input,pop_ups=True,handle_mouse=mouse)  #handle_mouse 开启鼠标点选模式，默认为真不能使用复制粘贴功能
        global Loop
        Loop=self.loop
        threading.Thread(target=self.change_data, args=()).start()
        self.loop.run()



    def unhandled_input(self, key):
        if key == 'ctrl d':
            Delfile(self.view,self.loop)
            return
        if key == 'ctrl n':
            TouchFile(self.view,self.loop)
            return
        if key == 'esc':  #回退目录重新读取按钮们
            with open('dir.yaml', 'r') as f:
                datas = yaml.safe_load(f)
            Dir=[ii for ii in datas['Dir'].split('/') if (len(str(ii)) != 0)]
            #os.system(f'echo "{Dir}" > 123')
            with open('dir.yaml', 'w') as f:
                if Dir!=[]: #如果Dir不是根号的话，就进行目录处理
                    datas['Dir'] = datas['Dir'].replace(Dir[-1]+'/','')
                yaml.dump(datas, f)
            font_buttons=create_button_list(*file_dir())
            self.fonts._set_widget_list(font_buttons)
            #筛选回退保证
            global original_buttons
            original_buttons = self.fonts._get_widget_list()
        if key == 'ctrl t':
            '''
            按键ctrl+t 召唤终端使用overload覆盖层的方式让终端浮于view层上
            '''
            urwid.set_encoding('utf8')
            term=Termpop(self.view)
            exit = urwid.LineBox(term)
            exit = urwid.Overlay(exit, self.view, 'center', 300, 'middle', 300)  #这里300和300不设置会报错
            self.loop.widget = exit
            return
        if key == 'ctrl r':  #刷新
            font_buttons=create_button_list(*file_dir())
            self.fonts._set_widget_list(font_buttons)
            return
        if key == '?':
            def fn(view,loop,new):  #这里的传参为顺序传参 传多个参数最后一个一直都是要操作的对象 这里是button
                loop.widget=view
            #help_info=urwid.Text('Command Help')  #需要制作退出按钮
            quit_button = urwid.Button('Quit')
            urwid.connect_signal(quit_button,'click',fn,weak_args=[self.view,self.loop]) #传参数给fn函数
            quit_button=urwid.Filler(quit_button,'top')
            help_info = urwid.Overlay(quit_button, self.view, 'center', 300, 'middle', 300)  # 这里300和300不设置会报错
            self.loop.widget = help_info
            return
        #if key == 'f8':
        if key == 'ctrl w':
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