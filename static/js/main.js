function encodeImage(element, target) {
    let file = element.files[0];
    let reader = new FileReader();
    reader.onloadend = function() {
        document.getElementById(target).value = reader.result;
    }
    reader.readAsDataURL(file);
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
  function openNav() {
    document.getElementById("mySidenav").style.display = "block";
    document.getElementById("mySidenav").style.width = "100%";
  }