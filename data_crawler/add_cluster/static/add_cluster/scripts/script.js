function addURLS() {
    debugger;
    var num = document.getElementsByName("noofurls")[0].value;
    var cont = document.getElementById("cont");
    cont.innerHTML = '';
    for(i = 0; i < num; i++) {
        cont.appendChild(document.createTextNode("url" + (i+1)));
        var input = document.createElement("input");
        input.type = "text";
        input.name = "name" + i;
        cont.appendChild(input);
        cont.appendChild(document.createElement("br"));
    }
}