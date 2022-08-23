window.onload = (event) => {
var imported = document.createElement('script');
imported.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js";
document.head.appendChild(imported);
var imported2 = document.createElement('script');
imported2.src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js";
document.head.appendChild(imported2);

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
        parent_doc=window.opener.document
        window.location.href= this.getAttribute('data-next-url')+"?with="+this.getAttribute('data-with')
        //    add new friend to the parent view
        var li = document.createElement('li')
        var but = document.createElement('button')
        li.appendChild(but)
        but.setAttribute('data-myfriend' , this.getAttribute('data-with'))
        but.setAttribute('data-next-url',this.getAttribute('data-send-note'))
        but.textContent=this.getAttribute('data-with')
        but.className="send_message friend_item"
        parent_doc.getElementById("friend_container").appendChild(li)

        //    add new friend to the parent view
        parent_doc.getElementById("new_notification").innerHTML = parseInt(parent_doc.getElementById("new_notification").innerHTML) -1
        
        
        })
    }
}
}