import wui

win = wui.Panel()
win.setSize(400, 300)

# group = wui.Group(win, bg="yellow")
# group.place(x=0, y=0, width=200, height=200)
# group.x = 10
# group.y = 10
# group.width = 200
# group.height = 200


com = wui.AskBtnLabelCom(win)
com.x = 10
com.y = 10
com.setType(1)
com.path


win.mainloop()