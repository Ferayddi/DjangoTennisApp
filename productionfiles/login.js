const appHeight = () => {
    $('.backgroundImage').css("height", window.innerHeight);
   }

window.addEventListener("resize", appHeight)
appHeight()