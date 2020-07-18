#! /usr/bin/env python
#coding=utf-8
 
import sys,os  ##参数处理for windows，和操作系统交互
import re  ##正则表达式处理工具
import struct  ##二进制数据操作
 
def extract_swf(filename, buf, offset):
    try:
        length = struct.unpack_from('<L', buf, offset+4)[0]
        swfname = filename + '_offset_0x%x.swf=' % offset
        open(swfname,'wb').write(buf[offset:offset + length])
        # print('[+] Find embeded swf file at offset 0x%x ' % offset)
        print('[+] Save embeded swf file to ' + swfname)
    except:
        pass
        
 
def usage():
    print('Usage: extract_swf.py  [file]')
 
 
if __name__ == '__main__':
    print('\nextract_swf.py 1.0\n')
    
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
 
    if (not os.path.exists(sys.argv[1])):
        print('[-] Invalid file path: %s!' % sys.argv[1])
        sys.exit(0)
 
  
    filename = sys.argv[1]
    
    print('[+] Searching embeded swf file in ' + sys.argv[1])
 
    
    buf = open(filename, 'rb').read()
    pattern = re.compile('FWS|CWS')
    match_obj = pattern.search(buf, 0)
 
    while match_obj != None:   ##循环提取（若文件中包含多个SWF文件）
        try:
            extract_swf(filename, buf, match_obj.start())
        except:
            pass
 
        match_obj = pattern.search(buf, match_obj.end())  ##下一个匹配