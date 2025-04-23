const toggleButtons = document.querySelectorAll('.order_num');

toggleButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const newBlock = button.nextElementSibling; // Получаем следующий блок после кнопки
        const currentMaxHeight = window.getComputedStyle(newBlock).maxHeight;
        
        if (currentMaxHeight === '0px') {
            newBlock.style.maxHeight = `${newBlock.scrollHeight}px`; // Устанавливаем max-height на текущее содержимое
            setTimeout(() => {
                newBlock.classList.add('visible'); // Добавляем класс visible после изменения max-height
            }, 0); // Используем 0 для немедленного добавления класса
        } else {
            newBlock.classList.remove('visible'); // Убираем класс visible перед изменением max-height
            newBlock.style.maxHeight = "0px"; 
        }
    });
});
