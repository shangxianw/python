import win32api
import win32con

key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\*\shell");
newKey = win32api.RegCreateKey(key,"YNote")
sub_key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,r"SOFTWARE\Classes\*\shell\YNote")
newsubKey = win32api.RegCreateKey(sub_key,"command")
win32api.RegSetValue(newsubKey,"(Default)", win32con.REG_SZ,"\"D:\\软件\vsCode\\Microsoft VS Code\\Code.exe" "%1\"")