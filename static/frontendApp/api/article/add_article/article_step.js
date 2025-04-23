





// url localStorage 



// const step1 = document.getElementById("step1");
// const step2 = document.getElementById("step2");

// if (!step1 || !step2) {
//     console.error("Required elements are missing.");
// } else {




//     function step_2(){


//         // const nextButton = document.getElementById('next_button'); 

//         const temp_article_type_title = localStorage.getItem("article_type_title");
            

//         document.getElementById('step1').style.display = "none";
//         document.getElementById('step2').style.display = "block";
//         document.getElementById('line1').style.backgroundColor = "#4F46E5"; // HEX for indigo-600
//         document.getElementById('step2-circle').style.backgroundColor = "#4F46E5"; // HEX for indigo-600

        
//         // store step in session
//         localStorage.setItem("current_step", "step2");
//         // localStorage.setItem("step_expiry", Date.now() + 1 * 60 * 1000); // Expire in 1 minute

        

//     }


//     function step_1(){

                
//         document.getElementById('step2').style.display = "none";
//         document.getElementById('step1').style.display = "block";
//         document.getElementById('line1').style.backgroundColor = "#D1D5DB"; // HEX for indigo-600
//         document.getElementById('step2-circle').style.backgroundColor = "#E5E7EB"; // HEX for indigo-600
        
//         // store step in session
//         localStorage.setItem("current_step", "step1");
//         // localStorage.setItem("step_expiry", Date.now() + 1 * 60 * 1000); // Expire in 1 minute
        

//     }

//     if (localStorage.getItem("current_step") === "step2") {
//         alert(localStorage.getItem("current_step"))
//         step_2();
//     } else {
//         step_1();
//     }

    
// }











// url base 

const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");

if (!step1 || !step2) {
    console.error("Required elements are missing.");
} else {
    function updateURL(step) {
        const url = new URL(window.location);
        url.searchParams.set("step", step);
        window.history.pushState({}, "", url);
    }

    function step_2() {
        document.getElementById('step1').style.display = "none";
        document.getElementById('step2').style.display = "block";
        document.getElementById('line1').style.backgroundColor = "#4F46E5"; // HEX for indigo-600
        document.getElementById('step2-circle').style.backgroundColor = "#4F46E5"; // HEX for indigo-600

        // Update URL
        updateURL("step2");
    }

    function step_1() {
        document.getElementById('step2').style.display = "none";
        document.getElementById('step1').style.display = "block";
        document.getElementById('line1').style.backgroundColor = "#D1D5DB"; // Gray color
        document.getElementById('step2-circle').style.backgroundColor = "#E5E7EB"; // Gray color

        // Update URL
        updateURL("step1");
    }

    // Get step from URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentStep = urlParams.get("step");

    if (currentStep === "step2") {
        step_2();
    } else {
        step_1();
    }
}
