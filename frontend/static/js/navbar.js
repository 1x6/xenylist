var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-50px";
  }
  prevScrollpos = currentScrollPos;

  if (window.pageYOffset == 0) {
    document.getElementById("navbar").style.backgroundColor = "#0b1622";
  } else {
    document.getElementById("navbar").style.backgroundColor = "#09121b";
  }
} 