// Header section

const langBtn = document.querySelector('header .container button.primary')
const langMenu = document.querySelector("header .container .lang-menu")

langBtn.addEventListener("click", () => {
    if (langMenu.style.display === "block") {
        langMenu.style.display = "none"
    } else {
        langMenu.style.display = "block"
    }
})

// FAQ section

const questions = document.querySelectorAll('.question')

questions.forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;
        answer.classList.toggle('show');
    });
});

// End FAQ section



// Slider responsive

// Previous Debates Section
const swipers = document.querySelectorAll("swiper-container")

if (parseInt(window.innerWidth) < 576) {
  swipers.forEach(swiper => {
    swiper.setAttribute("slides-per-view", "1")
  })
}

if (parseInt(window.innerWidth) >= 576) {
  swipers.forEach(swiper => {
    swiper.setAttribute("slides-per-view", "2")
  })
}

if (parseInt(window.innerWidth) >= 992) {
  swipers.forEach(swiper => {
    swiper.setAttribute("slides-per-view", "3")
  })
}

window.addEventListener("resize", () => {
  if (parseInt(window.innerWidth) < 576) {
    swipers.forEach(swiper => {
      swiper.setAttribute("slides-per-view", "1")
    })
  }

  if (parseInt(window.innerWidth) >= 576) {
    swipers.forEach(swiper => {
      swiper.setAttribute("slides-per-view", "2")
    })
  }
  
  if (parseInt(window.innerWidth) >= 992) {
    swipers.forEach(swiper => {
      swiper.setAttribute("slides-per-view", "3")
    })
  }
})


// Map section
