// Функция для расчета итоговой цены
function calculateTotalPrice() {
    const priceInput = document.querySelector('#id_price');  // ID поля "Цена"
    const discountInput = document.querySelector('#id_discount');  // ID поля "Скидка"
    const totalPriceInput = document.querySelector('#id_total_price');  // ID поля "Итоговая цена"

    // Получаем значения цены и скидки
    const price = parseFloat(priceInput.value) || 0;
    const discount = parseFloat(discountInput.value) || 0;

    // Рассчитываем итоговую цену
    let totalPrice = price;
    if (discount > 0) {
        totalPrice = price - (price * discount / 100);
    }

    // Округляем до целого числа
    totalPriceInput.value = Math.round(totalPrice);
}

// Добавляем обработчики событий для полей "Цена" и "Скидка"
document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.querySelector('#id_price');
    const discountInput = document.querySelector('#id_discount');

    if (priceInput && discountInput) {
        priceInput.addEventListener('input', calculateTotalPrice);
        discountInput.addEventListener('input', calculateTotalPrice);
    }

    // Инициализируем расчет итоговой цены при загрузке страницы
    calculateTotalPrice();
});


// Инициализация слайдера
function initSlider() {
    const slider = document.querySelector('.product-slider');
    if (slider) {
        let currentIndex = 0;
        const items = slider.querySelectorAll('.slider-item');

        function showSlide(index) {
            items.forEach((item, i) => {
                item.style.display = i === index ? 'block' : 'none';
            });
        }

        showSlide(currentIndex);

        const nextButton = document.createElement('button');
        nextButton.innerText = 'Вперед';
        nextButton.onclick = () => {
            currentIndex = (currentIndex + 1) % items.length;
            showSlide(currentIndex);
        };

        const prevButton = document.createElement('button');
        prevButton.innerText = 'Назад';
        prevButton.onclick = () => {
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            showSlide(currentIndex);
        };

        // Удаляем старые кнопки, если они есть
        const oldButtons = slider.querySelectorAll('button');
        oldButtons.forEach(button => button.remove());

        // Добавляем новые кнопки
        slider.appendChild(prevButton);
        slider.appendChild(nextButton);
    }
}

// Функция для переключения видимости блоков
function toggleEditForm() {
    const productDetailContainer = document.getElementById('product-detail-container');
    const createContainer = document.getElementById('create-container');

    if (productDetailContainer.style.display === 'none') {
        // Если форма редактирования видна, скрываем её и показываем информацию о товаре
        productDetailContainer.style.display = 'block';
        createContainer.style.display = 'none';
    } else {
        // Если информация о товаре видна, скрываем её и показываем форму редактирования
        productDetailContainer.style.display = 'none';
        createContainer.style.display = 'block';
    }

    // Инициализируем слайдер при каждом отображении блока с информацией о товаре
    if (productDetailContainer.style.display === 'block') {
        initSlider();
    }
}

// Инициализация слайдера при загрузке страницы
document.addEventListener("DOMContentLoaded", function() {
    initSlider();
});