

function goto(){
    window.location.href = "/register";
}

// script.js
// script.js
document.getElementById('menuButton').addEventListener('click', function() {
    var menu = document.getElementById('menu');
    if (menu.style.left === '0px') {
        menu.style.left = '-200px'; // Hide the menu
    } else {
        menu.style.left = '0px'; // Show the menu
    }
});