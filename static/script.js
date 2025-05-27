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

// Loading Screen
document.addEventListener("DOMContentLoaded", () => {
    // Add event listener to the submit button
    const submitButton = document.getElementById("submit-button");
    const loadingScreen = document.getElementById("loading-screen");
    const continueButton = document.getElementById("continue-button");
    const contentContainer = document.getElementById("content-container");

    console.log("JavaScript loaded");
    console.log("Submit button:", submitButton);
    console.log("Loading screen:", loadingScreen);

    if (submitButton) {
        submitButton.addEventListener("click", function (event) {

            if (loadingScreen) {
                loadingScreen.style.display = "flex"; // Show the loading screen
            }

            // Delay for the loading screen
            setTimeout(() => {
                if (loadingScreen) {
                    loadingScreen.style.display = "none"; // Hide the loading screen
                }
                if (contentContainer) {
                    contentContainer.style.display = "none"; // Hide the content container
                }
                if (continueButton) {
                    continueButton.style.display = "block"; // Show the continue button
                }
            }, 3000); // Adjust the delay time (3000 ms = 3 seconds)
        });
    }

    // Automatically submit the form when a card is selected
    document.querySelectorAll('input[name="card-input"]').forEach(input => {
        input.addEventListener('change', () => {
            input.closest('form').submit();
        });
    });
});



