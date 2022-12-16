import urwid

def main():
    urwid.set_encoding('utf8')

    term = urwid.Terminal(('sshpass','-p','Wlw123','ssh','wlw@127.0.0.1','-t','cd','/home',';','bash'), encoding='utf-8',env={'SHELL': '/bin/sh'},escape_sequence='"ctrl a"')
    # term = urwid.Terminal('None')



    # term = urwid.Terminal(None, encoding='utf-8')
    mainframe = urwid.LineBox(
        # urwid.Pile([
            term
            # ('fixed', 1, urwid.Filler(urwid.Edit('focus test edit: '))),
        # ]),
    )

    def set_title(widget, title):
        mainframe.set_title(title)

    def quit(*args, **kwargs):
        raise urwid.ExitMainLoop()

    def handle_key(key):
        if key in ('q', 'Q'):
            quit()

    urwid.connect_signal(term, 'title', set_title)
    urwid.connect_signal(term, 'closed', quit)

    loop = urwid.MainLoop(
        mainframe,
        handle_mouse=True,
        unhandled_input=handle_key)

    term.main_loop = loop
    # term.respond('o\n')
    # term.main_loop.stop()
    loop.run()

if __name__ == '__main__':
    main()
    # print()
