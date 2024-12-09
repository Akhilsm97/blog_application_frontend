document.addEventListener("scroll", function () {
    const navbar = document.getElementById("navbar");
    
    if (window.scrollY > 50) { // Adjust scroll threshold as needed
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });
  