import urwid as u


class MyListBox(u.ListBox):

    def keypress(self, size, key):
        if key in ('tab',):
            self.focus_position = (self.focus_position + 1) % len(self.body.contents)
            if self.focus_position == 0:
                return key
        else:
            return key

    def selectable(self):
        return len(self.body.contents) > 0


class App(object):

    def handle_key(self, key):
        if key in ('q',):
            raise u.ExitMainLoop()
        if key in ('tab',):
            next_focus = (self.columns.focus_position + 1) % len(self.columns.contents)
            self.columns.set_focus(next_focus)

    def __init__(self):

        s1 = "asd ad as d" * 10
        s2 = "a sd sdf sf" * 10
        s3 = "yxc d dsa a" * 10

        t1 = u.LineBox(u.AttrWrap(u.Text(s1), "normal", "selected"))
        t2 = u.LineBox(u.AttrWrap(u.Text(s2), "normal", "selected"))
        t3 = u.LineBox(u.AttrWrap(u.Text(s3), "normal", "selected"))

        lw1 = u.SimpleListWalker([t1])
        lw2 = u.SimpleListWalker([t2, t3])

        lb1 = MyListBox(lw1)
        lb2 = MyListBox(lw2)

        lb1 = u.LineBox(lb1)
        lb2 = u.LineBox(lb2)

        ba1 = u.BoxAdapter(lb1, height=20)
        ba2 = u.BoxAdapter(lb2, height=20)

        self.columns = u.Columns([ba1, ba2])

        filler = u.Filler(self.columns, 'top')

        PALETTE = [("normal", "black", "white"),
                   ("selected", "black", "light cyan")]

        loop = u.MainLoop(filler, PALETTE, unhandled_input=self.handle_key)

        loop.run()


if __name__ == '__main__':
    app = App()