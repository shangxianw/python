var Fs:IFile = require('fs');
var Path:IPath = require('path');
var Xlsx:IXlsx = require('xlsx');
let wordArray = ["", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];

class DaoCfg
{
    public oriDir:string;
    public tarClientDir:string;
    public tarServerDir:string;
    public supportFileType:string[];
    public tarFileType:string;

    public keyCountXY:string;
    public outputCol:number;
    public typeCol:number;
    public keyCol:number;
    public descCol:number;
    public contentCol:number;
    
    public typeInt:string;
    public typeString:string;
    public typeArray:string;
    public typeA:string;
    
    public clientTag:string;
    public serverTag:string;

    public rowRange:number[];
    public colRange:number[];
    public keyCount:number;

    public clientJson:any;
    public serverJson:any;
    public tarObjClient:any;
    public tarObjServer:any;
    public constructor()
    {
        this.init();
    }

    public init()
    {
        this.oriDir             /** excel表的地址文件夹      */    = "D:/wsx/war/config/xls/";
        this.tarClientDir       /** 输出客户端地址           */    = "D:/wsx/war/config/config/client/";
        this.tarServerDir       /** 输出服务端地址           */    = "D:/wsx/war/config/config/server/";
        this.supportFileType    /** 接受的excel表格式        */    = [".xls"];
        this.tarFileType        /** 输出格式                 */   = ".json";

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
    }

    public destroy()
    {

    }

    public start()
    {
        let fileArray:string[] = Fs.readdirSync(this.oriDir);
        for(let fileName of fileArray)
        {
            let path = this.oriDir + fileName;
            let fileType = Path.extname(path);
            if(this.supportFileType.indexOf(fileType) < 0) // 不符合文件格式
                continue;
            let workbook = Xlsx.readFile(path);
            this.doExcel(workbook);
        }
    }

    private doExcel(workbook:IWorkbook)
    {
        let sheetNameArray = workbook.SheetNames;
        for(let sheetName of sheetNameArray)
        {
            let sheet:ISheet = workbook.Sheets[sheetName];
            let range = sheet["!ref"].split(":"); // [A1, B2]
            
            // 初始化列的范围
            let startRow = wordArray.indexOf(range[0].slice(0, 1));
            let endRow = wordArray.indexOf(range[1].slice(0, 1));
            this.rowRange = [startRow, endRow];
            // 初始化行的范围
            let startCol = Number(range[0].slice(1));
            let endCol = Number(range[1].slice(1));
            this.colRange = [startCol, endCol];
            // 初始化key数量
            let node:INode = sheet[this.keyCountXY];
            if(node != null)
                this.keyCount = node.v;
            this.clientJson = {};
            this.serverJson = {};
            
            // 组装数据
            this.packJson(sheet);
            
            // 输出文件
            let clientPath = this.tarClientDir + sheetName + ".json";
            let clientJsonString = JSON.stringify(this.clientJson, null, 4);
            Fs.writeFileSync(clientPath, clientJsonString);
            
            let serverPath = this.tarServerDir + sheetName + ".json";
            let serverJsonString = JSON.stringify(this.serverJson, null, 4);
            Fs.writeFileSync(serverPath, serverJsonString);
            
        }
    }

    private packJson(sheet:ISheet)
    {
        for(let col = this.contentCol, colLen = this.colRange[1]; col<=colLen; col++)
        {
            let flag = this.packStruct(sheet, col);
            if(flag == false)
                continue;
            for(let row = this.rowRange[0], rowLen = this.rowRange[1]; row<=rowLen; row++)
            {
                this.packValue(sheet, col, row);
            }
        }

        // console.log(this.clientJson);
        // console.log(this.serverJson);
        // console.log("==================");
    }

    // 生成键结构
    private packStruct(sheet:ISheet, col:number):boolean
    {
        if(this.keyCount == 1)
        {
            let vNode1:INode = this.getNode(sheet, col, 1);
            if(vNode1 == null)
                return false;
            if(this.clientJson[vNode1.v] == null)
            {
                this.clientJson[vNode1.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v];
            }
            if(this.serverJson[vNode1.v] == null)
            {
                this.serverJson[vNode1.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v];
            }
            
        }
        else if(this.keyCount == 2)
        {
            let vNode1:INode = this.getNode(sheet, col, 1);
            let vNode2:INode = this.getNode(sheet, col, 2);
            if(vNode1 == null || vNode2 == null)
                return false;
            if(this.clientJson[vNode1.v] == null)
                this.clientJson[vNode1.v] = {};
            if(this.serverJson[vNode1.v] == null)
                this.serverJson[vNode1.v] = {};
            
            if(this.clientJson[vNode1.v][vNode2.v] == null)
            {
                this.clientJson[vNode1.v][vNode2.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v][vNode2.v];
            }
            if(this.serverJson[vNode1.v][vNode2.v] == null)
            {
                this.serverJson[vNode1.v][vNode2.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v][vNode2.v];
            }
        }
        else if(this.keyCount == 3)
        {
            let vNode1:INode = this.getNode(sheet, col, 1);
            let vNode2:INode = this.getNode(sheet, col, 2);
            let vNode3:INode = this.getNode(sheet, col, 3);
            if(vNode1 == null || vNode2 == null || vNode3 == null)
                return false;
            if(this.clientJson[vNode1.v] == null)
                this.clientJson[vNode1.v] = {};
            if(this.serverJson[vNode1.v] == null)
                this.serverJson[vNode1.v] = {};
            
            if(this.clientJson[vNode1.v][vNode2.v] == null)
                this.clientJson[vNode1.v][vNode2.v] = {};
            if(this.serverJson[vNode1.v][vNode2.v] == null)
                this.serverJson[vNode1.v][vNode2.v] = {};
            
            if(this.clientJson[vNode1.v][vNode2.v][vNode3.v] == null)
            {
                this.clientJson[vNode1.v][vNode2.v][vNode3.v] = {};
                this.tarObjClient = this.clientJson[vNode1.v][vNode2.v][vNode3.v];
            }
            if(this.serverJson[vNode1.v][vNode2.v][vNode3.v] == null)
            {
                this.serverJson[vNode1.v][vNode2.v][vNode3.v] = {};
                this.tarObjServer = this.serverJson[vNode1.v][vNode2.v][vNode3.v];
            }
        }
        return true;
    }

    private packValue(sheet:ISheet, col:number, row:number)
    {
        let keyNode:INode = this.getNode(sheet, this.keyCol, row);
        let valueNode:INode = this.getNode(sheet, col, row);
        let typeNode:INode = this.getNode(sheet, this.typeCol, row);
        if(keyNode == null || valueNode == null || typeNode == null)
            return;
        
        if(typeNode.v == this.typeInt)
        {
            if(this.isOutputClient(sheet, row) == true)
                this.tarObjClient[keyNode.v] = Number(valueNode.v);
            if(this.isOutputServer(sheet, row) == true)
                this.tarObjServer[keyNode.v] = Number(valueNode.v);
        }
        else if(typeNode.v == this.typeString)
        {
            if(this.isOutputClient(sheet, row) == true)
                this.tarObjClient[keyNode.v] = String(valueNode.v);
            if(this.isOutputServer(sheet, row) == true)
                this.tarObjServer[keyNode.v] = String(valueNode.v);
        }
        else if(typeNode.v == this.typeArray)
        {
            if(this.isOutputClient(sheet, row) == true)
            {
                if(this.tarObjClient[keyNode.v] == null)
                    this.tarObjClient[keyNode.v] = [];
                this.tarObjClient[keyNode.v].push(valueNode.v)
            }
            if(this.isOutputServer(sheet, row) == true)
            {
                if(this.tarObjClient[keyNode.v] == null)
                    this.tarObjClient[keyNode.v] = [];
                this.tarObjClient[keyNode.v].push(valueNode.v)
            }
        }
        else if(typeNode.v == this.typeA)
        {
            let keyArray:string[] = (keyNode.v as string).split("_");
            if(keyArray==null || keyArray[0] == null || keyArray[1] == null)
                return;
            let key = keyArray[0];
            let subKey = keyArray[1];
            if(this.isOutputClient(sheet, row) == true)   
            {
                if(this.tarObjClient[key] == null)
                    this.tarObjClient[key] = [];
                
                let aoArray:any[] = this.tarObjClient[key];
                let flag:boolean = false;
                for(let item of aoArray)
                {
                    if(item[subKey] != null) // 说明这个对象已经给这个key赋过值，需要找没有赋过值的，那个才是目标对象
                        continue;
                    item[subKey] = valueNode.v;
                    flag = true;
                    break;
                }
                if(flag == false) // 说明里面还没有这个对象
                {
                    let newObj = {};
                    newObj[subKey] = valueNode.v;
                    aoArray.push(newObj);
                }
            }

            if(this.isOutputServer(sheet, row) == true)
            {
               if(this.tarObjServer[key] == null)
                    this.tarObjServer[key] = [];
                
                let aoArray:any[] = this.tarObjServer[key];
                let flag:boolean = false;
                for(let item of aoArray)
                {
                    if(item[subKey] != null) // 说明这个对象已经给这个key赋过值，需要找没有赋过值的，那个才是目标对象
                        continue;
                    item[subKey] = valueNode.v;
                    flag = true;
                    break;
                }
                if(flag == false) // 说明里面还没有这个对象
                {
                    let newObj = {};
                    newObj[subKey] = valueNode.v;
                    aoArray.push(newObj);
                } 
            }
        }
    }

    private getRealXY(col:number, row:number):string
    {
        let a = wordArray[row];
        if(a != null)
        {
            return a + col;
        }
        return "A1";
    }

    private getNode(sheet:ISheet, col:number, row:number):INode
    {
        let nodeKey = this.getRealXY(col, row);
        return sheet[nodeKey];
    }

    private isOutputClient(sheet:ISheet, row:number):boolean
    {
        let outputNode = this.getNode(sheet, this.outputCol, row);
        if(outputNode == null)
            return false;
        return outputNode.v.indexOf(this.clientTag) >= 0
    }

    private isOutputServer(sheet:ISheet, row:number):boolean
    {
        let outputNode = this.getNode(sheet, this.outputCol, row);
        if(outputNode == null)
            return false;
        return outputNode.v.indexOf(this.serverTag) >= 0
    }
}
let daoCfg = new DaoCfg();
daoCfg.start();

// ---------------------------------------------------------------------- interface
interface IPath
{
    extname(path:string):string;
}

interface IXlsx
{
    readFile(path:string):IWorkbook;
    utils:{
        sheet_to_json(sheet:ISheet):any[]
    }
}

interface IWorkbook
{
    SheetNames:string[];
    Sheets:any;
}

interface ISheet
{
    "!ref":string;
}

interface INode
{
    v:any;
    t:any;
    w:any;
}

interface IFile
{
    readdirSync(path:string):string[];
    writeFileSync(path:string, content:any);
}