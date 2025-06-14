document.addEventListener("DOMContentLoaded", function () {
  const elements = document.querySelectorAll(".scroll-animate");

  function checkPosition() {
    const windowHeight = window.innerHeight;
    elements.forEach((el) => {
      const positionFromTop = el.getBoundingClientRect().top;
      if (positionFromTop - windowHeight <= -100) {
        el.classList.add("animate-fade");
      }
    });
  }

  window.addEventListener("scroll", checkPosition);
  window.addEventListener("resize", checkPosition);
  checkPosition();
});
