//__________Загрузка оценки уже написанного отзыва
window.onload = function() {
    var markValue = document.querySelector('.hidden_span') ? document.querySelector('.hidden_span').getAttribute('value') : null;
    markValue = parseInt(markValue)
    if (markValue) {
        document.getElementById("star" + markValue).checked = true;
        var stars = document.querySelectorAll('.fa-star');
        
        stars.forEach(function(star, index) {
            if (index < markValue) {
                star.className = "fa-star checked";
            }
        });
    }
};



// Получаем все элементы с классом 'hidden' и атрибутом 'data-rating'
const ratingElements = document.querySelectorAll('.hidden[data-rating]');

ratingElements.forEach(ratingElement => {
    const rating = parseFloat(ratingElement.getAttribute('data-rating'));

    const starContainer = document.createElement('div');
    
    const totalStars = 5;
    
    for (let i = 1; i <= totalStars; i++) {
        if (i <= Math.floor(rating)) { 
            starContainer.appendChild(createStar(true, false, true)); // Полная звезда
        } else {
            starContainer.appendChild(createStar(true, true, false)); // Пустая звезда
        }
    }

    // Добавляем контейнер с звездами в текущий элемент
    ratingElement.appendChild(starContainer);
});

function createStar(isFilled,isEmpty, isFull) {
    const star = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    star.setAttribute("width", "16");
    star.setAttribute("height", "16");
    star.setAttribute("viewBox", "0 0 16 16");
    star.setAttribute("class", "star_rate")
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    if(isEmpty) {
        path.setAttribute("d", "M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z");
        path.setAttribute("fill", isFilled ? "#FFD700" : "#ccc"); // Золотой для заполненной звезды, серый для пустой
    }
    if(isFull){
        path.setAttribute("d", "M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z");
        path.setAttribute("fill", isFilled ? "#FFD700" : "#ccc"); // Золотой для заполненной звезды, серый для пустой
    }

    star.appendChild(path);
    return star;
}


