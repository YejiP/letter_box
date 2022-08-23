
var imported = document.createElement('script');
imported.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js";
document.head.appendChild(imported);


window.onload = (event) => {
    document.body.style.backgroundColor =
    document.getElementById("color").textContent;

    var e = document.getElementById("edit");
    if (e != null) {
        e.addEventListener("click", edit);
    }
    var r = document.getElementById("reply");
    if (r != null) {
        r.addEventListener("click", reply);
    }

    document.getElementById("delete").addEventListener("click", del);
    };

    function edit() {
    col = this.getAttribute("data-color");
    window.location.href =this.getAttribute("data-next-url") +"?color=" + col;
    }
    function del() {
    window.location.href = this.getAttribute("data-next-url")
    }

    function reply() {
    var w = 400;
    var h = 400;
    var left = (screen.width - w) / 4;
    var top = (screen.height - h) / 4;
    url = this.getAttribute("data-next-url")+"?receiver=" + this.getAttribute("data-sender");
    var mywindow = window.open(
        url,
        "_blank",
        " width=" + w + ", height=" + h + ", top=" + top + ", left=" + left
    );
    mywindow.addEventListener("load", set_receiver);
    function set_receiver() {
        mywindow.document.getElementById("receiver").value = receiver;
    }
}
