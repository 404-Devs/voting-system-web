function encodeImage(element, target) {
    let file = element.files[0];
    let reader = new FileReader();
    reader.onloadend = function() {
        document.getElementById(target).value = reader.result;
    }
    reader.readAsDataURL(file);
}