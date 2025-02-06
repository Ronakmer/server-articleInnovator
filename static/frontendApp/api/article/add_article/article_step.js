
// // Ensure script runs only when elements exist
// const step1 = document.getElementById("step1");
// const step2 = document.getElementById("step2");
// const nextButton = document.getElementById("next_button_id");
// const backButton = document.querySelectorAll(".back_button_class"); // New Back Button
// const line1 = document.getElementById("line1");
// const step2Circle = document.getElementById("step2-circle");

// if (!step1 || !step2 || !nextButton || !backButton || !line1 || !step2Circle) {
//     console.error("Required elements are missing.");
// } else {
//     function showStep2() {
//         sessionStorage.setItem("current_step", "step2");

//         step1.classList.add("hidden");
//         step2.classList.remove("hidden");

//         line1.style.backgroundColor = "#4F46E5"; // Indigo-600
//         step2Circle.style.backgroundColor = "#4F46E5"; // Indigo-600
//     }

//     function showStep1() {
//         sessionStorage.setItem("current_step", "step1");

//         step2.classList.add("hidden");
//         step1.classList.remove("hidden");

//         line1.style.backgroundColor = "#D1D5DB"; // Gray-300
//         step2Circle.style.backgroundColor = "#E5E7EB"; // Gray-200
//     }

//     nextButton.addEventListener("click", showStep2);
//     backButton.addEventListener("click", showStep1);

//     // Restore correct step on page reload
//     if (sessionStorage.getItem("current_step") === "step2") {
//         showStep2();
//     } else {
//         showStep1();
//     }
// }








const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");

if (!step1 || !step2) {
    console.error("Required elements are missing.");
} else {




    function step_2(){


        // const nextButton = document.getElementById('next_button'); 

        const temp_article_type_title = sessionStorage.getItem("article_type_title");
        // if(temp_article_type_title == null) {
            
        //     // document.getElementById('next_button').disabled = true;
        //     // document.getElementById('next_button').style.backgroundColor = '#2563eb';
        //     nextButton.removeAttribute("disabled");
        //     nextButton.classList.replace("bg-indigo-400", "bg-indigo-600"); // Change color
        //     nextButton.classList.add("hover:bg-indigo-700"); // Add hover effect
        //     nextButton.style.cursor = "pointer";
                
        //     show_toast("error", `Please select an article type before proceeding`);

        //     // return;
        // } 

        document.getElementById('step1').style.display = "none";
        document.getElementById('step2').style.display = "block";
        document.getElementById('line1').style.backgroundColor = "#4F46E5"; // HEX for indigo-600
        document.getElementById('step2-circle').style.backgroundColor = "#4F46E5"; // HEX for indigo-600

        
        // store step in session
        sessionStorage.setItem("current_step", "step2");
        // sessionStorage.setItem("step_expiry", Date.now() + 1 * 60 * 1000); // Expire in 1 minute

        

    }


    function step_1(){

                
        document.getElementById('step2').style.display = "none";
        document.getElementById('step1').style.display = "block";
        document.getElementById('line1').style.backgroundColor = "#D1D5DB"; // HEX for indigo-600
        document.getElementById('step2-circle').style.backgroundColor = "#E5E7EB"; // HEX for indigo-600
        
        // store step in session
        sessionStorage.setItem("current_step", "step1");
        // sessionStorage.setItem("step_expiry", Date.now() + 1 * 60 * 1000); // Expire in 1 minute
        

    }

    if (sessionStorage.getItem("current_step") === "step2") {
        alert(sessionStorage.getItem("current_step"))
        step_2();
    } else {
        step_1();
    }

    
}

window.addEventListener('beforeunload', function() {
    // Optional: Clear the session step if you need to remove the step when leaving the page
    sessionStorage.removeItem("current_step");
});







