import urwid as u


# class MyListBox(u.ListBox):
#
#     def keypress(self, size, key):
#         if key in ('tab',):
#             self.focus_position = (self.focus_position + 1) % len(self.body.contents)
#             if self.focus_position == 0:
#                 return key
#         else:
#             return key
#
#     def selectable(self):
#         return len(self.body.contents) > 0
import os
class change(u.Pile):
    def __init__(self,widge,w):
        self.__super.__init__([widge,u.Divider(),w,])
    def keypress(self, size, key):
        if not self.contents:
            return key
        if key in ('tab',):
            next_focus = (self.focus_position + 1) % len(self.contents)
            self.set_focus(next_focus)

class App(object):

    def handle_key(self, key):
        if key in ('q',):
            raise u.ExitMainLoop()


    def __init__(self):

        s1 = "asd ad as d" * 10
        s2 = "a sd sdf sf" * 10
        s3 = "yxc d dsa a" * 10

        t1 = u.LineBox(u.AttrWrap(u.Text(s1), "normal", "selected"))
        t2 = u.AttrWrap(u.Edit(s2), "normal", "selected")
        t3 = u.Edit(s3)



        lb1 = change(t3,t2)
        # lb1=u.Pile([t3,t2,u.Divider()])


        lb1 = u.LineBox(lb1)







        filler = u.Filler(lb1, 'top')

        PALETTE = [("normal", "black", "white"),
                   ("selected", "black", "light cyan")]

        loop = u.MainLoop(filler, PALETTE, unhandled_input=self.handle_key)

        loop.run()


if __name__ == '__main__':
    app = App()