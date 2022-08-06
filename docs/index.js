
function onSuccess(json) {
    var spaces = document.getElementById("spaces");
    var value = spaces.value;
    spaces.innerHTML = "";
    // from https://attacomsian.com/blog/javascript-iterate-objects
    for (const space in json) {
        if (json.hasOwnProperty(space)) {
            addSpace(space, json[space]);
        }
    }
    spaces.value = value;
    showImage();
}

var xmlhttp = new XMLHttpRequest();

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
        if (this.status == 200) {
            try {
                var myArr = JSON.parse(this.responseText);
                onSuccess(myArr);
                console.log("loaded!");
            } catch(err) {
                console.log("Error:", err.message);
            }
        } else {
            console.log("could not load space data.");
            document.getElementById("loading").innerText = "Error Loading!";
        }
    }
};
xmlhttp.open("GET", "https://directory.spaceapi.io/", true);
xmlhttp.send();

console.log("loading...");

function addSpace(space, url) {
    var select = document.getElementById("spaces");
    var option = document.createElement("option");
    option.value = url
    option.innerText = space;
    select.appendChild(option);
}

function getUrl(status) {
    // get params
    var server = document.getElementById("server").value;
    var params = new URLSearchParams();
    params.set("url", document.getElementById("spaceurl").value);
    var open = document.getElementById("open").value;
    if (open) {
        params.set("open", open);
    }
    var closed = document.getElementById("open").value;
    if (closed) {
        params.set("closed", closed);
    }
    if (status) {
        params.set("status", status);
    }
    // construct url
    return server + "/status?" + params.toString();
}

function spaceChanged() {
    document.getElementById("spaceurl").value = document.getElementById("spaces").value;
    showImage();
}

function showImage() {
    // fill UI
    // preview link
    document.getElementById("imagelink").href = getUrl();
    document.getElementById("imagelink").innerText = getUrl();

    // current image
    document.getElementById("imageNowLink").href = getUrl();
    document.getElementById("imageNow").src = getUrl();

    // open image
    document.getElementById("imageOpenLink").href = getUrl("open");
    document.getElementById("imageOpen").src = getUrl("open");

    // closed image
    document.getElementById("imageClosedLink").href = getUrl("closed");
    document.getElementById("imageClosed").src = getUrl("closed");

    // error
    document.getElementById("error").src = getUrl();
}

function escapeHTML(str){
    // from https://stackoverflow.com/a/22706073
    return new Option(str).innerHTML;
}

window.addEventListener("load", function() {
    spaceChanged();
});

