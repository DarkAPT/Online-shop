let stars = 
    document.getElementsByClassName("fa-star");
 
// Funtion to update rating
function gfg(n) {
        remove();
        for (let i = 0; i < n; i++) {
            if (n == 1) cls = "one";
            else if (n == 2) cls = "two";
            else if (n == 3) cls = "three";
            else if (n == 4) cls = "four";
            else if (n == 5) cls = "five";
            stars[i].className = "fa-star checked";
        }
}
 
// To remove the pre-applied styling
function remove() {
    let i = 0;
    while (i < 5) {
        stars[i].className = "fa-star";
        i++;
    }
}

let stars2 = document.querySelectorAll('.fa-star');

// Обработчик событий для наведения курсора
stars2.forEach((star, index) => {
    star.addEventListener('mouseover', () => {
        // Убираем активный класс у всех звезд
        stars2.forEach(s => s.classList.remove('active'));
        // Добавляем активный класс на текущую звезду и все предыдущие
        for (let i = 0; i <= index; i++) {
            stars2[i].classList.add('active');
        }
    });

    // Обработчик для сброса эффектов при уходе курсора
    star.addEventListener('mouseleave', () => {
        stars2.forEach(s => s.classList.remove('active'));
    });
});