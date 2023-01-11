const navbar = document.getElementById("navbar");
let prevScrollpos = window.pageYOffset;

window.onscroll = function () {
  const currentScrollPos = window.pageYOffset;

  navbar.style.top = prevScrollpos > currentScrollPos ? "0" : "-50px";
  prevScrollpos = currentScrollPos;
  navbar.style.backgroundColor = currentScrollPos === 0 ? "#0b1622" : "#09121b";
};
