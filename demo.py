import urwid
import threading
import  time
import os,sys
import datetime
import psutil
import yaml
Loop=None
exterfonts=None
ed='vi'
mouse=True
original_buttons=None
# a=urwid.Text(u'hello word',align='center')
# a.rows((11,))#定义了文本，还可以定义文本的悬浮
# b=urwid.Filler(a,'middle')    #定义了文本模块的位置
# loop=urwid.MainLoop(b)   #主循环
# loop.run()    #运行
# p=[('text','black','light gray'),  #名字 ，字体颜色， 背景色
#    ('bg','black','dark red'),
#    ('text_bg','black', 'light red'),]
# def exit(key):
#     if key == 'q':
#         raise  urwid.ExitMainLoop
#     # else:
#     #     a.set_text('请按下q退出界面 ')
# class Q(urwid.Filler):
#
#     def keypress(self, size, key):
#         if key != 'enter':
#             return super(Q,self).keypress(size,key)
#         self.original_widget=urwid.Text(f'Nice to meet {txt.edit_text}')
#         a=urwid.AttrMap(())
#
# txt= urwid.Edit(('text','FUCK ALL PEOPLE'),align='center')
# test=Q(txt)
#
#
# #bg=urwid.AttrMap(fi,'bg')
#
# loop = urwid.MainLoop(test, p, unhandled_input=exit)
# loop.run()


    # else:
    #     a.set_text('请按下q退出界面 ')

#
lb = urwid.SimpleListWalker([])
p=[('text','black','light gray'),  #名字 ，字体颜色， 背景色
   ('bg','black','dark red'),
   ('text_bg','black', 'light red'),]

# lb.extend([
# urwid.Columns([
#     urwid.Pile([,urwid.Divider()]),
# urwid.Pile([urwid.AttrMap(abc,'bg'),urwid.Divider()]),
#
# ])
# ])
# a=urwid.Text(u'Welcome to Lin',align='left').sizing()
# ac=urwid.Filler(a,'top')
#
#
# loop = urwid.MainLoop(ac, p, unhandled_input=exit)
# loop.run()
# import urwid
#
# def main():
#     urwid.set_encoding('utf8')
#     term = urwid.Terminal(('vi','GA.py'), encoding='utf-8')
#
#     mainframe = urwid.LineBox(
#         urwid.Pile([
#             ,
#             ('weight', 10, term),
#
#         ]),
#     )
#
#     def set_title(widget, title):
#         mainframe.set_title(title)
#
#     def quit(*args, **kwargs):
#         raise urwid.ExitMainLoop()
#
#     def handle_key(key):
#         if key in ('q', 'Q'):
#             quit()
#
#     urwid.connect_signal(term, 'title', set_title)
#     urwid.connect_signal(term, 'closed', quit)
#
#     loop = urwid.MainLoop(
#         mainframe,
#         handle_mouse=False,
#         unhandled_input=handle_key)
#
#     term.main_loop = loop
#     loop.run()
#
# if __name__ == '__main__':
#     main()

import urwid
import urwid.raw_display


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
    如果file和dir都为空则正常
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
        rb = create_dir_button(i)
        font_buttons.append(rb)
    for i in file:

        rb = create_file_button(i)
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

    else:
        w = urwid.Button(' ')
    w = urwid.AttrWrap(w, 'button normal', 'dir button select')
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

        w = ThingWithAPopUp(FileButton(
            f' {file[:30]}{count_str(file[:30])}{user_group}{count_str(user_group)}{chmod}{count_str(chmod)}{file_size}{count_str(file_size)}{dates}')
        )

    else:
        w = urwid.Button(' ')
    w = urwid.AttrWrap(w, 'button normal', 'file button select')
    return w


 #同种button可以做到不一样的效果

class DirButton(urwid.Button):
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
        else:
            return key

class FileButton(urwid.Button):
    # def __init__(self, abc):
    #     self.abc = abc
    def keypress(self, size, key):
        if key in ('ctrl p',) :
            os.system(f'echo {self.label.strip().split(" ")[-1]} > wulinwei1.py')
        elif  key in ('ctrl d',):
            os.system('rm -rf wulinwei.py')
        elif key in ('enter',):   #点击文件按钮发送click信号给按钮本身 模拟点击操作
            self._emit('click')
        else:
            return key


class Termpop(urwid.Terminal):

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



        oper=(
            u'Ctrl+r 刷新页面',
            u'Ctrl+c 复制文件',
            u'Ctrl+v 粘贴文件',
            u'Ctrl+x 解压文件',
            u'Ctrl+s 一键压缩文件夹',
            u'Ctrl+t 召唤终端',
            u'Alt+c 复制文件内容',
            u'shift+? 查看帮助'
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
            self.In.set_text(f'【{datas["Dir"]}】 当前位置')
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
        if key == 'esc':  #刷新
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
        if key == 'f8':
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