# import json

# path = "D:\\wsx\\pytools\\exml2ts\\config\\tmp.json"
# with open(path, "r", encoding="utf-8") as f:
#     jsons = json.load(f)
    
#     for key in jsons:
#         print(jsons["name"])

# jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
# text = json.loads(jsonData)
# print(text.function)

# import re
strr = '<e:Button id="testBtn" label="test" />'
seas = 'id="'
ends = '"'
index = strr.find(seas)
endIndex = strr.find(ends, index+4)

ids = strr[index+4: endIndex]
print(ids)

aa = ':'
bb = ' '
index = strr.find(aa)+1
endIndex = strr.find(bb, index)
className = strr[index:endIndex]
print(className)
