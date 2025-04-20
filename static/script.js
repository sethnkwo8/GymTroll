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

document.querySelectorAll('.custom-card-plan').forEach(card => {
    card.addEventListener('click', () => {
        // Remove 'selected' class from all cards
        document.querySelectorAll('.custom-card-plan').forEach(c => c.classList.remove('selected'));

        // Add 'selected' class to the clicked card
        card.classList.add('selected');

        // Perform an action (e.g., navigate to a new page)
        const cardId = card.getAttribute('data-id');
        console.log(`Selected card: ${cardId}`);
        // Example: Redirect to a specific page
        // window.location.href = `/${cardId}`;
    });
});