var Fs = require('fs');
var Path = require('path');
var Xlsx = require('xlsx');
var wordArray = ["", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
var DaoCfg = /** @class */ (function () {
    function DaoCfg() {
        this.init();
    }
    DaoCfg.prototype.init = function () {
        this.oriDir /** excel表的地址文件夹      */ = "D:/wsx/war/config/xls/";
        this.tarClientDir /** 输出客户端地址           */ = "D:/wsx/war/config/config/client/";
        this.tarServerDir /** 输出服务端地址           */ = "D:/wsx/war/config/config/server/";
        this.supportFileType /** 接受的excel表格式        */ = [".xls"];
        this.tarFileType /** 输出格式                 */ = ".json";
        this.keyCountXY = "A2";
        this.outputCol = 3;
        this.typeCol = 4;
        this.keyCol = 5;
        this.descCol = 6;
        this.contentCol = 7;
        this.clientTag = "c";
        this.serverTag = "s";
        this.typeInt = "int";
        this.typeString = "string";
        this.typeArray = "array";
        this.typeA = "ao";
        this.keyCount = 0;
        this.rowRange = [1, 1];
        this.colRange = [1, 1];
    };
    DaoCfg.prototype.destroy = function () {
    };
    DaoCfg.prototype.start = function () {
        var fileArray = Fs.readdirSync(this.oriDir);
        for (var _i = 0, fileArray_1 = fileArray; _i < fileArray_1.length; _i++) {
            var fileName = fileArray_1[_i];
            var path = this.oriDir + fileName;
            var fileType = Path.extname(path);
            if (this.supportFileType.indexOf(fileType) < 0) // 不符合文件格式
                continue;
            var workbook = Xlsx.readFile(path);
            this.doExcel(workbook);
        }
    };
    DaoCfg.prototype.doExcel = function (workbook) {
        var sheetNameArray = workbook.SheetNames;
        for (var _i = 0, sheetNameArray_1 = sheetNameArray; _i < sheetNameArray_1.length; _i++) {
            var sheetName = sheetNameArray_1[_i];
            var sheet = workbook.Sheets[sheetName];
            var range = sheet["!ref"].split(":"); // [A1, B2]
            // 初始化列的范围
            var startRow = wordArray.indexOf(range[0].slice(0, 1));
            var endRow = wordArray.indexOf(range[1].slice(0, 1));
            this.rowRange = [startRow, endRow];
            // 初始化行的范围
            var startCol = Number(range[0].slice(1));
            var endCol = Number(range[1].slice(1));
            this.colRange = [startCol, endCol];
            // 初始化key数量
            var node = sheet[this.keyCountXY];
            if (node != null)
                this.keyCount = node.v;
            this.clientJson = {};
            this.serverJson = {};
            // 组装数据
            this.packJson(sheet);
            // 输出文件
            var clientPath = this.tarClientDir + sheetName + ".json";
            var clientJsonString = JSON.stringify(this.clientJson, null, 4);
            Fs.writeFileSync(clientPath, clientJsonString);
            var serverPath = this.tarServerDir + sheetName + ".json";
            var serverJsonString = JSON.stringify(this.serverJson, null, 4);
            Fs.writeFileSync(serverPath, serverJsonString);
        }
    };
    DaoCfg.prototype.packJson = function (sheet) {
        for (var col = this.contentCol, colLen = this.colRange[1]; col <= colLen; col++) {
            var flag = this.packStruct(sheet, col);
            if (flag == false)
                continue;
            for (var row = this.rowRange[0], rowLen = this.rowRange[1]; row <= rowLen; row++) {
                this.packValue(sheet, col, row);
            }
        }
        // console.log(this.clientJson);
        // console.log(this.serverJson);
        // console.log("==================");
    };
    // 生成键结构
    DaoCfg.prototype.packStruct = function (sheet, col) {
        if (this.keyCount == 1) {
            var vNode1 = this.getNode(sheet, col, 1);
            if (vNode1 == null)
                return false;
            if (this.clientJson[vNode1.v] == null) {
                this.clientJson[vNode1.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v];
            }
            if (this.serverJson[vNode1.v] == null) {
                this.serverJson[vNode1.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v];
            }
        }
        else if (this.keyCount == 2) {
            var vNode1 = this.getNode(sheet, col, 1);
            var vNode2 = this.getNode(sheet, col, 2);
            if (vNode1 == null || vNode2 == null)
                return false;
            if (this.clientJson[vNode1.v] == null)
                this.clientJson[vNode1.v] = {};
            if (this.serverJson[vNode1.v] == null)
                this.serverJson[vNode1.v] = {};
            if (this.clientJson[vNode1.v][vNode2.v] == null) {
                this.clientJson[vNode1.v][vNode2.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v][vNode2.v];
            }
            if (this.serverJson[vNode1.v][vNode2.v] == null) {
                this.serverJson[vNode1.v][vNode2.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v][vNode2.v];
            }
        }
        else if (this.keyCount == 3) {
            var vNode1 = this.getNode(sheet, col, 1);
            var vNode2 = this.getNode(sheet, col, 2);
            var vNode3 = this.getNode(sheet, col, 3);
            if (vNode1 == null || vNode2 == null || vNode3 == null)
                return false;
            if (this.clientJson[vNode1.v] == null)
                this.clientJson[vNode1.v] = {};
            if (this.serverJson[vNode1.v] == null)
                this.serverJson[vNode1.v] = {};
            if (this.clientJson[vNode1.v][vNode2.v] == null)
                this.clientJson[vNode1.v][vNode2.v] = {};
            if (this.serverJson[vNode1.v][vNode2.v] == null)
                this.serverJson[vNode1.v][vNode2.v] = {};
            if (this.clientJson[vNode1.v][vNode2.v][vNode3.v] == null) {
                this.clientJson[vNode1.v][vNode2.v][vNode3.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v][vNode2.v][vNode3.v];
            }
            if (this.serverJson[vNode1.v][vNode2.v][vNode3.v] == null) {
                this.serverJson[vNode1.v][vNode2.v][vNode3.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v][vNode2.v][vNode3.v];
            }
        }
        return true;
    };
    DaoCfg.prototype.packValue = function (sheet, col, row) {
        var keyNode = this.getNode(sheet, this.keyCol, row);
        var valueNode = this.getNode(sheet, col, row);
        var typeNode = this.getNode(sheet, this.typeCol, row);
        if (keyNode == null || valueNode == null || typeNode == null)
            return;
        if (typeNode.v == this.typeInt) {
            if (this.isOutputClient(sheet, row) == true)
                this.tarObjClient[keyNode.v] = Number(valueNode.v);
            if (this.isOutputServer(sheet, row) == true)
                this.tarObjServer[keyNode.v] = Number(valueNode.v);
        }
        else if (typeNode.v == this.typeString) {
            if (this.isOutputClient(sheet, row) == true)
                this.tarObjClient[keyNode.v] = String(valueNode.v);
            if (this.isOutputServer(sheet, row) == true)
                this.tarObjServer[keyNode.v] = String(valueNode.v);
        }
        else if (typeNode.v == this.typeArray) {
            if (this.isOutputClient(sheet, row) == true) {
                if (this.tarObjClient[keyNode.v] == null)
                    this.tarObjClient[keyNode.v] = [];
                this.tarObjClient[keyNode.v].push(valueNode.v);
            }
            if (this.isOutputServer(sheet, row) == true) {
                if (this.tarObjClient[keyNode.v] == null)
                    this.tarObjClient[keyNode.v] = [];
                this.tarObjClient[keyNode.v].push(valueNode.v);
            }
        }
        else if (typeNode.v == this.typeA) {
            var keyArray = keyNode.v.split("_");
            if (keyArray == null || keyArray[0] == null || keyArray[1] == null)
                return;
            var key = keyArray[0];
            var subKey = keyArray[1];
            if (this.isOutputClient(sheet, row) == true) {
                if (this.tarObjClient[key] == null)
                    this.tarObjClient[key] = [];
                var aoArray = this.tarObjClient[key];
                var flag = false;
                for (var _i = 0, aoArray_1 = aoArray; _i < aoArray_1.length; _i++) {
                    var item = aoArray_1[_i];
                    if (item[subKey] != null) // 说明这个对象已经给这个key赋过值，需要找没有赋过值的，那个才是目标对象
                        continue;
                    item[subKey] = valueNode.v;
                    flag = true;
                    break;
                }
                if (flag == false) // 说明里面还没有这个对象
                 {
                    var newObj = {};
                    newObj[subKey] = valueNode.v;
                    aoArray.push(newObj);
                }
            }
            if (this.isOutputServer(sheet, row) == true) {
                if (this.tarObjServer[key] == null)
                    this.tarObjServer[key] = [];
                var aoArray = this.tarObjServer[key];
                var flag = false;
                for (var _a = 0, aoArray_2 = aoArray; _a < aoArray_2.length; _a++) {
                    var item = aoArray_2[_a];
                    if (item[subKey] != null) // 说明这个对象已经给这个key赋过值，需要找没有赋过值的，那个才是目标对象
                        continue;
                    item[subKey] = valueNode.v;
                    flag = true;
                    break;
                }
                if (flag == false) // 说明里面还没有这个对象
                 {
                    var newObj = {};
                    newObj[subKey] = valueNode.v;
                    aoArray.push(newObj);
                }
            }
        }
    };
    DaoCfg.prototype.getRealXY = function (col, row) {
        var a = wordArray[row];
        if (a != null) {
            return a + col;
        }
        return "A1";
    };
    DaoCfg.prototype.getNode = function (sheet, col, row) {
        var nodeKey = this.getRealXY(col, row);
        return sheet[nodeKey];
    };
    DaoCfg.prototype.isOutputClient = function (sheet, row) {
        var outputNode = this.getNode(sheet, this.outputCol, row);
        if (outputNode == null)
            return false;
        return outputNode.v.indexOf(this.clientTag) >= 0;
    };
    DaoCfg.prototype.isOutputServer = function (sheet, row) {
        var outputNode = this.getNode(sheet, this.outputCol, row);
        if (outputNode == null)
            return false;
        return outputNode.v.indexOf(this.serverTag) >= 0;
    };
    return DaoCfg;
}());
var daoCfg = new DaoCfg();
daoCfg.start();
//# sourceMappingURL=main.js.map