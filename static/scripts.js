function showTabContent(tabID) {
  hideAllTabContent()
  document.getElementById(tabID).style.display = "block";
}

function hideAllTabContent() {
  var i, tabcontent;
  tabcontent = document.getElementsByClassName("tabcontent")
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
}

document.addEventListener('DOMContentLoaded', init, false);

function init() {
  document.getElementById("button1").addEventListener("click", function(){showTabContent("mpc")}, false);
  document.getElementById("button2").addEventListener("click", function(){showTabContent("css")}, false);  
}
