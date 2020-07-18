class MathUtils:
	@staticmethod
	def Abs(n):
		return abs(n);

	def Round(n):
		return round(n);

	def Ceil(n):
		import math;
		return math.ceil(n);

	def Floor(n):
		import math;
		return math.floor(n);

	def Max(*n):
		return max(n);

	def Min(*n):
		return min(n);

	def Random():
		import random;
		return random.random();