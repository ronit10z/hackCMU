function submitUpvote(button_id){
  console.log(button_id);
  $.post( "like", { card: button_id } );
}

function upvoteButtons(){
  buttons = document.getElementsByClassName("likebutton");
  for(i = 0; i < buttons.length; i++){
    var entry_name = buttons[i].id;
    document.getElementById(entry_name).addEventListener("click", function(){submitUpvote(this.id)});
  }
}

window.onload = function(){
  upvoteButtons();
}