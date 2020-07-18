import json;

class JsonUtils:
	@staticmethod
	def Stringify(jsonStr):
		return json.loads(jsonStr);

	def Parse(s):
		return json.dumps(s);