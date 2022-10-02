//Navigation select active link
let title =document.title;
activelink = document.querySelectorAll('.nav__link');

if (title.toLowerCase() == 'home'){
  activelink[0].classList.add('active')
}else if (title.toLowerCase() == 'about'){
  activelink[1].classList.add('active')
}else if (title.toLowerCase() == 'contact'){
  activelink[2].classList.add('active')
}

function send (){
  alert("Thank you. I'll be getting back to you soon.");
}