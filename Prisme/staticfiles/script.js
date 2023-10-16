function toggleMenu(){
    const menuMobile = document.getElementById("menu-mobile")

    if(menuMobile.className == "menu-mobile-active"){
        menuMobile.className = "menu-mobile"
    }
    else{
        menuMobile.className = "menu-mobile-active"
    }
}