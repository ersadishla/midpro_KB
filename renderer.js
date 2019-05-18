// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

const {PythonShell} = require('python-shell')

var running = false;
var size = 0;
var counter = 1;
var asd;
var obj_ref = {};
var data = new Array();

function exploreChild(obj){
    console.log(obj);
    let dd = document.getElementById(obj.id);

    for(let i in obj.children){
        obj_ref[obj.children[i].id] = obj.children[i];
        if(obj.children[i].expand == 0){
            let aa = addElement(obj.children[i]);
            dd.appendChild(aa);
            obj.children[i].expand = 1;
        }
    }
}

function drawBoard(element, bitmask) {
    var num = bitmask;
    var newBoard = element;
    for(let i=0; i<size; i++) {
        var row = newBoard.insertRow(i); /* Drawing the Rows */
        for(let j=0; j<size; j++) {
            var cell = row.insertCell(j); /* Drawing the Column */
            if ((num&3) == 0) cell.innerHTML = '-';
            else if ((num&3) == 2) cell.innerHTML = 'X';
            else if((num&3) == 3) cell.innerHTML = 'O';
            num = num >> 2;
        }
    }
    return newBoard;
}

function exploreObjChild(id){
    console.log(id, asd);
    exploreChild(obj_ref[id]);
}

function addElement(obj){
    var id = obj.id;
    var newRealDiv = document.createElement("div");
    var newButton = document.createElement("button"); 
    var newContent = document.createElement("table");

    newRealDiv.setAttribute("id", id);
    newButton.setAttribute("onclick", "exploreObjChild("+id+")");
    newContent.setAttribute("id","new-table");

    if (obj.status == "prunned") {
        newButton.setAttribute("class","prunned");
        newContent.setAttribute("class","table bg-danger text-white table-prunned");
    } else {
        newButton.setAttribute("class","not-prunned");
        newContent.setAttribute("class","table table-not-prunned");
    }

    newContent = drawBoard(newContent, Number(id));
    
    newButton.appendChild(newContent); 
    newRealDiv.appendChild(newButton);

    return newRealDiv;
}

function generate() {
    var zz = document.getElementById("size");
    var yy = document.getElementById("generate-button");
    zz.parentNode.removeChild(zz);
    yy.parentNode.removeChild(yy);
    if (size > 2) running = true; /* ADDITION */
    data = JSON.stringify(data);
    let next_turn = 0; /*ADDITION */
    if (counter == 0) next_turn = -1; /*ADDITION */
    else next_turn = 1; /*ADDITION */

    let options = {
        pythonPath: 'C:/Program Files/Python37/python.exe',
        scriptPath: 'D:/TerCapai/SMT4/KB/MidPro/UI - Copy/Alphabet/back_end',
        args : [data, size, next_turn]
    };
    PythonShell.run('Main.py',  options, function  (err, results)  {
        if  (err)  throw err;
        let out = document.getElementById("root");
        let obj = JSON.parse(results);
        asd = obj;
        out.setAttribute("id", obj.id);
        exploreChild(obj);
        console.log("Time Execution : "+obj.time+" second");
    });
}

function fill(id){
    if (!running) {
        if(counter == 0){
            document.getElementById(id).innerHTML = 'O';
            data[id[0]][id[1]] = 'O';
        }else {
            document.getElementById(id).innerHTML = 'X';
            data[id[0]][id[1]] = 'X';
        }
        counter = (counter + 1) % 2;
    }
}

function buildTable(){
    counter = 1;
    let n = document.getElementById("size").selectedIndex + 2;
    if (n < 3) return; /* ADDITION */
    size = n; /* ADDITION */
    createArray(n);
    // console.log(data);
    let tk = document.getElementById("tabel");
    while(tk.hasChildNodes()) {
        tk.removeChild(tk.firstChild);
    }
    for (let i=0; i<n; i++){
        let tr = document.createElement("tr");
        tr.setAttribute("id", ""+i+"");
        let tt = document.getElementById("tabel");  
        tt.appendChild(tr);
        for (let j=0; j<n; j++){
            let td = document.createElement("td");
            td.setAttribute("id", ""+i+""+j+"")
            td.setAttribute("onmousedown","fill('"+i+""+j+"')")
            td.innerHTML = "-";
            tr.appendChild(td);
        }
    }
}


function createArray(n){
    data = [];
    for(let i=0; i<n; i++){
        let tmp = new Array();
        for(let j=0; j<n; j++){
            tmp.push('-');
        }
        data.push(tmp);
    }
}