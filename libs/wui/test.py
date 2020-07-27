import wui

win = wui.Panel()
win.setSize(400, 300)

# group = wui.Group(win, bg="yellow")
# group.place(x=0, y=0, width=200, height=200)
# group.x = 10
# group.y = 10
# group.width = 200
# group.height = 200


com = wui.IOCom(win)
com.x = 0
com.y = 0


win.mainloop()