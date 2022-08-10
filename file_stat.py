import os, time, sys

# def file_dir():
#     #getFileInfo('/home/wlw/PycharmProjects/pythonProject')
#     output = os.popen('ls -lah ')
#     # print(output)
#     dir=[]
#     file=[]
#     for i in output:
#         if i.strip().split(' ')[0] == 'total':
#             continue
#         output_list=i.strip().split(' ')
#         output_list = [ii for ii in output_list if(len(str(ii))!=0)]
#         if output_list[0][0] == 'd':
#             dir.append(output_list)
#         else:
#             file.append(output_list)
#     return file,dir
import urwid
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


def unhandled_input( key):
    if key in ('Q', 'q'):
        raise urwid.ExitMainLoop()


# a=len('中文'.encode('utf-8'))






# print(tabulate([["Mark", 12, 95]],tablefmt="plain",))
a=urwid.Button('OK')

# print(a.get_label)
a=urwid.Filler(a,'top')

import time
time.sleep(2)

# a = urwid.AttrWrap(a, 'button normal', 'file button select')
# c=[]
# d=[]
# b=urwid.Button('not OK')
# #b=urwid.Filler(b,'top')
# b = urwid.AttrWrap(b, 'button normal', 'file button select')
# for i in range(5):
#     c.append(a)
# for i in range(5):
#     d.append(b)
#
#
# col = urwid.Columns(c, 0,
#             focus_column=1)
# print()
#
# col2 = urwid.Columns(d, 0,
#             focus_column=1)
#
# #col2.set_focus(3)
# #col2.set_focus_column(1)
# font2 = urwid.Pile([ urwid.Divider(),col,],focus_item=1)
#
#
# l = [font2]
# abc=urwid.SimpleListWalker(l)
# w = urwid.ListBox(abc)



#print(fonts.widget_list[0].widget_list[2].selectable())



# c=[]
# for i in   range(10):
#     c.append(a)

# fonts = urwid.Pile(c,
#             focus_item=1)
# col = urwid.Columns([chars, fonts], 0,
#             focus_column=1)
# l = [col]
# w = urwid.ListBox(urwid.SimpleListWalker(l))
#
#         # Frame
# w = urwid.AttrWrap(w, 'body')
# w = urwid.Frame( body=w)

loop = urwid.MainLoop(a, palette, unhandled_input=unhandled_input)
loop.run()