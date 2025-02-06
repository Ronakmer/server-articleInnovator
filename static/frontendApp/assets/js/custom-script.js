// view more tag script
var toggle_button = document.getElementById("toggle-button");
if(toggle_button){
  toggle_button.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default link behavior

    var moreTags = document.getElementById("more-tags");
    var plusIcon = document.getElementById("plus-icon");
    var minusIcon = document.getElementById("minus-icon");

    if (moreTags.classList.contains("hidden")) {
      moreTags.classList.remove("hidden");
      plusIcon.classList.add("hidden");
      minusIcon.classList.remove("hidden");
    } else {
      moreTags.classList.add("hidden");
      plusIcon.classList.remove("hidden");
      minusIcon.classList.add("hidden");
    }
  });


}
//filter button script
document.addEventListener("DOMContentLoaded", function () {
  const filterButton = document.getElementById("filterButton");
  const filterSection = document.getElementById("filterSection");

  // Toggle the visibility of the filter section on button click
  if(filterButton){
    filterButton.addEventListener("click", function () {
      filterSection.classList.toggle("hidden");
    });  
  }
});


// Select all expand buttons
const expandButtons = document.querySelectorAll('.expandButton');

expandButtons.forEach((button) => {
  // Find the parent container for this button
  const container = button.closest('.rounded-xl');
  
  // Find related elements within this container
  const buttonText = button.querySelector('.buttonText');
  const expandIcon = button.querySelector('.expandIcon');
  const articleInfo = container.querySelector('#articleInfo');

  button.addEventListener('click', function() {
    // Toggle the text between Expand and Collapse
    const isCollapsed = buttonText.textContent.trim() === 'Collapse';
    buttonText.textContent = isCollapsed ? 'Expand' : 'Collapse';

    // Toggle the rotation of the icon
    expandIcon.classList.toggle('rotate-180');

    // Toggle the visibility of the articleInfo div
    articleInfo.classList.toggle('hidden');
  });
});

// Handle the "more tags" functionality
const toggleButton = document.getElementById('toggle-button');
const moreTags = document.getElementById('more-tags');
const plusIcon = document.getElementById('plus-icon');
const minusIcon = document.getElementById('minus-icon');

if (toggleButton && moreTags && plusIcon && minusIcon) {
  toggleButton.addEventListener('click', function(e) {
    e.preventDefault();
    moreTags.classList.toggle('hidden');
    plusIcon.classList.toggle('hidden');
    minusIcon.classList.toggle('hidden');
  });
}