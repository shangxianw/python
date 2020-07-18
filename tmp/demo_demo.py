import math;
array = [1, 3, 5, 8, 9, 0, 2, 4, 6, 7];

class HeapSort(object):
	"""docstring for HeapSort"""
	def __init__(self):
		super(HeapSort, self).__init__()
		self.arr = [];

	def insert(self, num):
		arr = self.arr;
		i = len(arr) - 1;

		arr.insert(i, num);
		while math.floor(i/2) + 1 > 0 and arr[i] > arr[math.floor(i/2) + 1]:
			tmp = arr[i];
			arr[i] = arr[math.floor(i/2) + 1];
			arr[math.floor(i/2) + 1] = tmp;
			i = math.floor(i/2) + 1;

	def printfArr(self):
		for item in self.arr:
			print(item);

heap = HeapSort();

for item in array:
	heap.insert(item);

heap.printfArr();
