// Get the modal
var modal = document.getElementById("review_form");

// Get the button that opens the modal
var btn = document.getElementById("open_review_button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

const radioButtons = document.querySelectorAll('input[name="mark"]');
const submitBtn = document.getElementById('submit_review');

// Функция для проверки выбранной радиокнопки
radioButtons.forEach(radio => {
  radio.addEventListener('change', function() {
    // Проверка, есть ли выбранный рейтинг
    const isSelected = Array.from(radioButtons).some(r => r.checked);
    submitBtn.disabled = !isSelected; // Разблокировать кнопку, если выбран хотя бы один рейтинг
  });
});