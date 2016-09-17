function submitUpvote(button_id){
  console.log(button_id);
  $.ajax({
      url: '/like',
      type: 'POST',
      ContentType: 'application/json',
      data:  button_id
  });
}

function upvoteButtons(){
  buttons = document.getElementsByClassName("likebutton");
  for(i = 0; i < buttons.length; i++){
    document.getElementById(entry_name).addEventListener("click", function(){submitUpvote(this.id)});
  }
}

window.onload = function(){
  upvoteButtons();
}
