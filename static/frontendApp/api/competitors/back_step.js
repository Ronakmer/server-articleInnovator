async function back_step() {
    console.log(current_step, 'currentStep in back_step()');    

    if (current_step > 1) {
        if (current_step === 3) {
            current_step = 1;
        } else if (current_step === 4) {
            console.log('current_step == 4');
            current_step = 2;
        } else {
            current_step--;  // only decrease if not manually reset above
        }

        showStep(current_step);
    }
}

