import threading
import time
import requests
import random
from urllib import request, error
from fake_useragent import UserAgent

file = open("aaa.txt", mode="w", encoding="utf-8");
oriFile = open("proxy.txt", mode="r");
allThread = [];
lock = threading.Lock();
def verifyProxyList():
	while True:
		lock.acquire();
		a = oriFile.readline().strip();
		lock.release();
		if len(a) == 0:
			break;
		b = a.split("|");
		ip = b[1];
		port = b[2];
		ipPath  = ip + ":" + port;
		time.sleep(random.randint(1,7))
		code = verifyProxy(ipPath);
		if code == 200:
			lock.acquire();
			file.write(ipPath + "\n");
			print("写入 "+ ipPath + " 成功");
			lock.release();
		else:
			print(ipPath + " 失败");

def verifyProxy(ip):
	ua = UserAgent();
	header = {"User-Agent": ua.random};
	testUrl = "https://blog.csdn.net";

	proxy = {"http": ip};
	# proxyHandler = request.ProxyHandler(proxy);
	# proxyOpen    = request.build_opener(proxyHandler);
	# request.install_opener(proxyOpen);

	try:
		req = request.Request(testUrl, headers=header);
		rsq = request.urlopen(req, timeout=5.0);
		code = rsq.getcode();
		return code;
	except BaseException as e:
		return e;

if __name__ == '__main__':
	
	for i in range(5):
		t = threading.Thread(target=verifyProxyList);
		allThread.append(t);
		t.setDaemon(True);
		t.start();

	for t in allThread:
		t.join();

	file.close();
	oriFile.close();










































# def run():
#     time.sleep(2)
#     print('当前线程的名字是： ', threading.current_thread().name)
#     time.sleep(2)

# if __name__ == '__main__':
#     start_time = time.time()
#     print('这是主线程：', threading.current_thread().name)
#     thread_list = []
#     for i in range(5):
#         t = threading.Thread(target=run)
#         thread_list.append(t)
#     for t in thread_list:
#         t.setDaemon(True)
#         t.start();
#         t.join()
#     # for t in thread_list:
# print('主线程结束了！' , threading.current_thread().name)
# print('一共用时：', time.time()-start_time)