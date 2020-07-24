let elt;


const ajaxRequest = (body, url, callback) => {
  /** Ajax request */
  let request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
      let response = JSON.parse(this.responseText);
      callback(response);
    }
  }
  request.open("POST", url);
  request.setRequestHeader("Content-Type", "application/json");
  request.send(JSON.stringify(body));
};


/** check if the form contains text before sending */
const valider = (form) => {
  frm = document.forms[form];
  if(frm.elements['query'].value != "") {
    return true;
  }
  else {
    alert("Saisissez un produit");
    return false;
  }
}

const confirm = () => {
  frm = document.forms['passform'];
  if(frm.elements['newpassword'].value == frm.elements['confirmpassword'].value) {
    return true;
  }
  else {
    alert("Saisir un mot de passe identique");
    return false;
  }
}

/** function callback for ajaxRequest */
const success = (response) => {
  elt.innerHTML=response.message;
};

/** collect all button elements and add an event on each */
buttonList = document.getElementsByClassName('saveButtons')
for(i=0; i < buttonList.length; i++){
  buttonList[i].addEventListener('click', e => {
    elt = e.target;
    let body = {'id':e.target.id};
    ajaxRequest(body,e.target.dataset.url,success);
  });
}
