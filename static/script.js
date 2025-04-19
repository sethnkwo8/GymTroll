var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;

    if (currentScrollPos === 0) {
        // Always show the navbar when at the top of the page
        document.getElementById("navbar").style.top = "0";
    } else if (prevScrollpos > currentScrollPos) {
        // Show the navbar when scrolling up
        document.getElementById("navbar").style.top = "0";
    } else {
        // Hide the navbar when scrolling down
        document.getElementById("navbar").style.top = "-100px"; // Adjust height if needed
    }

    prevScrollpos = currentScrollPos;
};