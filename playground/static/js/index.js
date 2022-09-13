// Navigation panel  
const navigator =document.getElementById('navigator');

// navigator.innerHTML += `
// <nav class="nav">
//             <div class="nav__toggle" id="nav-toggle">
//                 <i class="bx bx-menu"></i>
//             </div>

//             <div>
//                 <a href="{% url 'home' %}" class="nav__logo">Kelvin</a>
//             </div>

//             <div class="nav__menu" id="nav-menu">
//                 <div class="nav__close" id="nav-close">
//                     <i class="bx bx-x"></i>
//                 </div>

//                 <ul class="nav__list">
//                     <li class="nav__item"><a href="{% url 'home' %}" class="nav__link">
//                             <div>Homer</div>
//                         </a></li>
//                     <li class="nav__item"><a href="{% url 'about' %}" class="nav__link">
//                             <div>About</div>
//                         </a></li>
//                     <li class="nav__item"><a href="{% url 'contact' %}" class="nav__link">
//                             <div>Contactme</div>
//                         </a></li>


//                 </ul>
//             </div>
//         </nav>
// `
//navigation menu
const navMenu = document.getElementById('nav-menu'),
toggleMenu=document.getElementById('nav-toggle'),
closeMenu=document.getElementById('nav-close')

//show menu
toggleMenu.addEventListener('click', () => {
    navMenu.classList.toggle('show')
})

//Hide menu
closeMenu.addEventListener('click', () => {
    navMenu.classList.remove('show')
})

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
  alert("Thank you. I'll be getting back to you sooner.");
}