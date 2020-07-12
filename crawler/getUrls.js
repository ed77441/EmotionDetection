async function sleep(ms = 0) {
	return new Promise(r => setTimeout(r, ms));
}

async function extractUrlDownload() {
	var listofname = document.querySelector("input.gLFyf").value.split(" ");
	var fileName = listofname[0];
    var cur = null;
	var rm;
    var urls = "";
	var pre = 0;
	var counter = 0;
	for(var i = 1; i < listofname.length; ++i) {
		fileName += '+' + listofname[i];
	}

    do {
		window.scrollTo(0,document.body.scrollHeight);
		await sleep(1500);
        cur = document.querySelectorAll("div.rg_meta");  
		bt = document.getElementById("smb");
		if(pre == cur.length) {
			bt.click();
			counter++;
			if (counter > 5) {
				break;
			}
		}
		pre = cur.length;
    }while(cur.length < 500);

    for(var i = 0; i < cur.length ; ++i) {
        var targetObj = JSON.parse(cur[i].innerHTML);
        urls += targetObj.ou + '\r\n';        
    }
	
    var a = document.createElement("a");
    var file = new Blob([urls], {type: 'text/plain'});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();	
}


extractUrlDownload();