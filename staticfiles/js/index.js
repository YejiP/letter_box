window.onload = (event) => {
function searchFriend() {
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    dt = document.getElementsByClassName("scrollmenu");
    li = dt[0].getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
      friend = li[i].getElementsByTagName("button")[0];
      if (friend) {
        txtValue = friend.textContent;
        if (txtValue.toUpperCase().startsWith(filter)) {
          li[i].style.display = "inline-block";
        } else {
          li[i].style.display = "none";
        }
      }       
    }
  }

var search = document.getElementById('search')
if (search!=null){
    search.addEventListener('keyup',searchFriend)

}

function send(event){
  if (event.target.classList.contains('send_message')){
  var w =400;
  var h= 400;
  var left = (screen.width - w) / 2;
  var top = (screen.height - h) / 4;
  var myNewWindow =  window.open(event.target.getAttribute('data-next-url')+"?receiver="+event.target.getAttribute('data-myfriend'),'_blank',' width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
  }
 }
var fc = document.getElementById('friend_container')
if (fc!=null){
  fc.addEventListener('click',send)

  var logo = document.getElementsByClassName("sticky")[0]
  document.getElementById("login_name").style.fontSize="2em"

}


function friendNew() {
var w =400;
var h= 400;
var left = (screen.width - w) / 2;
var top = (screen.height - h) / 4;
var myNewWindow =  window.open(this.getAttribute('data-next-url'),'_blank',' width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
} 

var fn = document.getElementById('add_button')
if (fn!=null){
    fn.addEventListener('click', friendNew)}


function openNote() {
  // temporally removing red 'new' sign at index page.
    document.getElementById(this.getAttribute('data-noteid')).innerHTML=""
    var w =400;
    var h= 400;
    var left = (screen.width - w) / 2;
    var top = (screen.height - h) / 4;
    url = this.getAttribute('data-noteid')+ "?color="+this.getAttribute('data-color')+"&mailbox="+this.getAttribute('data-mailbox')
    var myNewWindow =  window.open(url,'_blank',' width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
    }     

var notes = document.getElementsByClassName('notes')
if(notes!=null){
    for (var i =0;i<notes.length;i++){
        notes[i].addEventListener('click',openNote)
    }
}
}

