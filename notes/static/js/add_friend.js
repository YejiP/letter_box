window.onload = (event) => {

var imported = document.createElement('script');
imported.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js";
document.head.appendChild(imported);


var fr = document.getElementById('send_friend_request')
if (fr !=null){
    fr.addEventListener('click', function(){
        window.location.href = this.getAttribute('data-next-url')+"?friend_username="+this.getAttribute("data-to-whom");
    })

}

var af = document.getElementsByClassName('accept_friend')
if (af!=null){
    for(var i =0;i<af.length;i++){
        af[i].addEventListener('click',function(){
            window.location.href= this.getAttribute('data-next-url')+"?with="+this.getAttribute('data-with')
        })
    }
}
}