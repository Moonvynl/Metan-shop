const menuButton = document.getElementById("menuButton");
const sidebar = document.getElementById("sidebar");
const closeMenu = document.getElementById("closeMenu");
const overlay = document.getElementById("overlay");

function openMenu() {
    sidebar.classList.remove("-translate-x-full");
    overlay.classList.remove("hidden");
}

function closeMenuHandler() {
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
}

menuButton.addEventListener("click", openMenu);
closeMenu.addEventListener("click", closeMenuHandler);
overlay.addEventListener("click", closeMenuHandler);


function openCategoryMenu() {
    document.getElementById("categoryModal").classList.remove("hidden");
}

function closeCategoryMenu() {
    document.getElementById("categoryModal").classList.add("hidden");
}

document.addEventListener("click", function (event) {
    let modal = document.getElementById("categoryModal");
    if (event.target === modal) {
        closeCategoryMenu();
    }
});


document.addEventListener("DOMContentLoaded", function () {
document.querySelectorAll(".fa-angle-down").forEach(icon => {
icon.addEventListener("click", function (event) {
    event.preventDefault();
    let subcategories = this.closest("li").querySelector("ul");
    
    if (subcategories) {
        subcategories.classList.toggle("hidden");
    }
});
});
});
