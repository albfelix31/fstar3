function renderUserInfo() {
  var question = $("#question").val();
  var answer = $("#answer").val();
  var topicQ= $("#topicQ").val();


  // insert values in html
  $("#submission-placeholder").text(question);
  $("#answer-placeholder").text(answer);
  $("#topic-placeholder").text(topicQ);
}

function saveInfo(event){
  // stop normal function:submit forum info to app engine
  event.preventDefault();
  //grab user input values
  var question = $("#question").val();
  var answer = $("#answer").val();
  var topicQ= $("#topicQ").val();

  //send a request taht calls the post fiunction in one of our handlers
  var url = "/submit"; //cals the handler in manin.py
  var data ={
    'question':question,
    'answer':answer,
    'topicQ':topicQ,
  }
  var settings ={
    'method': 'POST',// call the post function in Main Handler
    'data': data,// send the user input to server
    'success': renderUserInfo

  };
  $.ajax(url, settings);

}

function setup() {
  $ ("#submit").click(saveInfo)
}

$(document).ready(setup)
