





// Onboarding flow structure
const onboardingFlow = {
    workspace_on_board_page: {
        ai_configuration_on_board_page: {
            team_on_board_page: {
                domain_on_board_page: {}
            }
        }
    }
};

// Get the current step from the URL or set default
const urlParams = new URLSearchParams(window.location.search);
let currentStep = urlParams.get("step") || "workspace_on_board_page";
let previousSteps = []; // Stack to keep track of previous steps

// Function to update the URL
const updateURL = (step) => {
    const newUrl = `${window.location.pathname}?step=${step}`;
    history.pushState(null, "", newUrl);
};

// Function to show the current step
const showStep = (step) => {
    // Hide all steps
    document.querySelectorAll(".onboard-step").forEach((el) => el.classList.add("hidden"));

    // Show the current step
    const stepElement = document.getElementById(step);
    if (stepElement) {
        stepElement.classList.remove("hidden");
    }
};

// Function to move to the next step
const nextStep = () => {
    // Traverse the onboardingFlow to find the next step
    const nextLocation = currentStep.split("/").reduce((acc, current) => acc[current] || {}, onboardingFlow);
    const nextSteps = Object.keys(nextLocation);
    const next = nextSteps.length ? nextSteps[0] : null;

    if (!next) {
        console.error(`No next step found for: ${currentStep}`);
        return;
    }

    let current_page = currentStep.split("/").pop();

    // Hide current step
    document.getElementById(current_page).classList.add("hidden");

    // Push the current step onto the previousSteps stack
    previousSteps.push(current_page);

    // Update currentStep
    currentStep += "/" + next;

    // Update URL
    updateURL(next);

    // Show the new step
    showStep(next);
};

// Function to move to the previous step
const previousStep = () => {
    if (previousSteps.length === 0) {
        return;
    }

    let current_page = currentStep.split("/").pop();

    // Hide current step
    document.getElementById(current_page).classList.add("hidden");

    // Pop the last step from the previousSteps stack
    currentStep = previousSteps.pop();

    // Update URL
    updateURL(currentStep);

    // Show the previous step
    showStep(currentStep);
};

// Show the correct step when the page loads
window.addEventListener("DOMContentLoaded", () => {
    showStep(currentStep);
});













