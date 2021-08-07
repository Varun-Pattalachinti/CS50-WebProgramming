document.addEventListener('DOMContentLoaded',()=>{
  if(!localStorage.getItem('username'))
  {
    ///need to add form for adding user
    const createForm = Handlebars.compile(document.querySelector('#createUserFormScript').innerHTML);
    document.querySelector('#addForm').innerHTML = createForm();
    ///console.log("I dont have username")
    ///get the first form element on the page
    const form = document.querySelector('form');
    // Stop the form from submitting when a button is pressed
    form.addEventListener('submit', function(e) {
      e.preventDefault();
    });

    const submitUsername = document.querySelector('#submitUsername')
    submitUsername.addEventListener('click', function() {
      // store the entered name in web storage
      username = document.querySelector('#username')
      ///console.log(username.value)
      localStorage.setItem('username', username.value);
      document.querySelector("#addForm").innerHTML = ""
    });

  }
  else {
    const welcomeUser = Handlebars.compile(document.querySelector('#welcomeUser').innerHTML)
    //console.log(localStorage.getItem('username'))
    username = localStorage.getItem('username')
    document.querySelector('#welcomeUserDiv').innerHTML = welcomeUser({'user': username})
  }
});
