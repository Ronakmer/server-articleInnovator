const addBtn = document.getElementById('add-name-value-btn');
const wrapper = document.getElementById('name-value-wrapper');

function attachRemoveEvent(btn) {
    btn.addEventListener('click', function () {
        const group = this.closest('.name-value-group');
        if (document.querySelectorAll('.name-value-group').length > 1) {
            group.remove();
        }
    });
}

addBtn.addEventListener('click', () => {
    const group = wrapper.querySelector('.name-value-group');
    const newGroup = group.cloneNode(true);

    // Clear input/textarea values
    newGroup.querySelectorAll('input, textarea').forEach(field => field.value = '');

    // Show the remove button in the cloned group
    const removeBtn = newGroup.querySelector('.remove-name-value-btn');
    removeBtn.classList.remove('hidden');
    attachRemoveEvent(removeBtn);

    wrapper.appendChild(newGroup);
});

// Attach event to existing remove button (if visible)
document.querySelectorAll('.remove-name-value-btn').forEach(btn => {
    if (!btn.classList.contains('hidden')) attachRemoveEvent(btn);
});