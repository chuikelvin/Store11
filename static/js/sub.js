const lessons = ['HTML5', 'css3', 'javascript', 'git', 'nodejs', 'react', 'python', 'django', 'flutter'];

const lessonTitles = [' introduction', ' variables', ' data types', ' functions', ' if else statements', ' loops (for and while)', ' object oriented programming', 'debugging and code structuring', ' best practices'];

const subjects = stringtoarray(sessionStorage.getItem('subjects'));
const subjectPercentages = stringtoarray(sessionStorage.getItem('progress'));
const container = document.querySelector('.container1')
const role = sessionStorage.getItem('role')

const nameTitle = document.querySelector('.lead')
let navlink = document.querySelectorAll(".nav-link")

let action;

function stringtoarray(str) {
    str = str.split(",");
    for (let i = 0; i < str.length; i++) {
        str[i] = parseInt(str[i])
    }
    return str;
}

nameTitle.insertAdjacentHTML('afterbegin', `
<h1>Welcome back to your ${sessionStorage.getItem('role')} dashboard ${sessionStorage.getItem('firstname')}</h1>
`);

function signout() {
    sessionStorage.clear();
    window.location.assign("index.php");
}

function showall() {
    action = "view lesson";

    navlink[1].classList.remove("chaguo");
    navlink[0].classList.add("chaguo");

    container.innerHTML = ""
    lessons.forEach((item, index) => {
        container.insertAdjacentHTML('beforeend', `<div class="col-sm">
  
  <!-- course -->
  <div class="gradient" onclick="location.href='#';" style="cursor:pointer;">
  <div class="row" style="flex:2;">
    <h3>${item}</h3>
    <!--<span class="progress-number">${subjectPercentages[index]}%</span>-->
    <span class="progress-bar progress-background"><span class="progress-foreground" style ="width:100%"></span></span>
  </div>
    <div class="row">
      <div class="col"><a href="#" class="progress">see overview</a></div>
      <div class="col"><a href="#" class="progress">${action}</a></div>
    </div>
    <div class="row" style="flex:2;display:flex;flex-direction:row;">
      <span>
      <i class="bx bxl-${item} information-icon"></i>
      </span>
      <p>${item}</p>
    </div>
  </div>
  <!-- course -->
                
  </div>`);
    });
}

function loadcontent() {
    navlink = document.querySelectorAll(".nav-link")
    navlink[1].classList.add("chaguo");
    navlink[0].classList.remove("chaguo");
    container.innerHTML = ""
    if (role == 'student') {
        action = "resume lesson"

        subjects.forEach((value, index) => {
            course = value - 1;

            container.insertAdjacentHTML('beforeend', `<div class="col-sm">
  
  <!-- course -->
  <div class="gradient" style="cursor:pointer;">
  <div class="row" style="flex:2;">
    <h3>${lessons[course]}</h3>
    <span class="progress-number">${subjectPercentages[index]}%</span>
    <span class="progress-bar progress-background"><span class="progress-foreground" style ="width:${subjectPercentages[index]}%"></span></span>
  </div>
    <div class="row">
      <div class="col"><a href="#" class="progress">see overview</a></div>
      <div class="col"><a href="#" class="progress">${action}</a></div>
    </div>
    <div class="row" style="flex:2;display:flex;flex-direction:row;">
      <span>
      <i class="bx bxl-${lessons[course]} information-icon"></i>
      </span>
      <p>${lessons[course]}</p>
    </div>
  </div>
  <!-- course -->
                
  </div>`);
        })
    } else {
        action = "modify lesson"

        let course = subjects - 1;

        container.insertAdjacentHTML('beforeend', `<div class="floating-add">
  <a href="#">
    <i class="bx bx-plus floating-icon" title = "add new chapter" ></i>
  <!-- <h3>add</h3> -->
  </a>
</div>`);

        for (let i = 0; i < subjectPercentages[0]; i++) {
            container.insertAdjacentHTML('beforeend', `<div class="col-sm">
  
  <!-- course -->
  <div class="gradient" style="cursor:pointer;">
  <div class="row" style="flex:2;">
    <h3>${lessons[course] +"  " +lessonTitles[i]}</h3>
    <!--<span class="progress-number"></span> -->
    <span class="progress-bar progress-background"><span class="progress-foreground" style ="width:100%"></span></span>
  </div>
    <div class="row">
      <div class="col"><a href="#" class="progress">see overview</a></div>
      <div class="col"><a href="#" class="progress">${action}</a></div>
    </div>
    <div class="row" style="flex:2;display:flex;flex-direction:row;">
      <span>
      <i class="bx bxl-${lessons[course]} information-icon"></i>
      </span>
      <p>${lessons[course]}</p>
    </div>
  </div>
  <!-- course -->
                
  </div>`)
        }

    }
}