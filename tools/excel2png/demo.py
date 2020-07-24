from win32com.client import Dispatch, DispatchEx
import pythoncom
from PIL import ImageGrab
import uuid
 
 
# screen_area——类似格式"A1:J10"
def excel_catch_screen(filename, sheetname, screen_area, img_name=False):
    """ 对excel的表格区域进行截图——用例：excel_catch_screen(ur"./ss.xlsx", "争霸赛", "A1:J10")"""
    # pythoncom.CoInitialize()  # excel多线程相关
 
    excel = DispatchEx("Excel.Application")  # 启动excel
    excel.Visible = True  # 可视化
    excel.DisplayAlerts = False  # 是否显示警告

    wb = excel.Workbooks.Open(filename)  # 打开excel
    
    ws = wb.Sheets(sheetname)  # 选择sheet
    ws.Range(screen_area).CopyPicture()  # 复制图片区域
    ws.Paste()
    excel.Selection.ShapeRange.Name = sheetname#new_shape_name  # 将刚刚选择的Shape重命名，避免与已有图片混淆
    ws.Shapes(sheetname).Copy()  # 选择图片

    img = ImageGrab.grabclipboard()  # 获取剪贴板的图片数据
    saveName = "D:\\wsx\\python\\tools\\excel2png\\" + sheetname + ".PNG"
    img.save(saveName)  # 保存图片
    wb.Close(SaveChanges=0)  # 关闭工作薄，不保存
    excel.Quit()  # 退出excel
    # pythoncom.CoUninitialize()
 
 
if __name__ == '__main__':
    excel_catch_screen("D:\\wsx\\python\\tools\\excel2png\\赛事.xlsx", "争霸赛", "A1:J10")
    # excel_catch_screen("D:\\wsx\\python\\tools\\excel2png\\ss.xlsx", "排位赛", "A1:J10")