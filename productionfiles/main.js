
$('.logoutButton').on("click", () => {
    window.location.href = "/logout";
});



const hideAllTabs = () => {
    $("#practiceTab").css("display", "none");
    $("#forumTab").css("display", "none");
    $("#profileTab").css("display", "none");
    $("#adminTab").css("display", "none");

}

$('.profileButton').on("click", () => {
    hideAllTabs();
    $("#profileTab").css("display", "block");
    location.href = "#profileTab";
});

$('.forumButton').on("click", () => {
    hideAllTabs();
    $("#forumTab").css("display", "block");
    location.href = "#forumTab";
});

$('.practiceButton').on("click", () => {
    hideAllTabs();
    $("#practiceTab").css("display", "block");
    location.href = "#practiceTab";
});

$('.adminButton').on("click", () => {
    hideAllTabs();
    $("#adminTab").css("display", "block");
    location.href = "#adminTab";
});



