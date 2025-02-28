// Инициализация слайдера независимо от наличия комментариев
document.addEventListener("DOMContentLoaded", function() {
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

        slider.appendChild(prevButton);
        slider.appendChild(nextButton);
    }
});

document.getElementById("edit-comment-btn").addEventListener("click", function() {
    document.querySelector('.comment-form-container').style.display = 'none';
    document.getElementById('edit-comment-form-container').style.display = 'block';
    document.getElementById("edit-comment-btn").style.display = 'none';
});

document.getElementById("cancel-edit-comment-btn").addEventListener("click", function() {
    document.querySelector('.comment-form-container').style.display = 'block';
    document.getElementById('edit-comment-form-container').style.display = 'none';
    document.getElementById("edit-comment-btn").style.display = 'inline-block';
});

document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const rateInput = document.querySelector("input[name='rate']");

    stars.forEach(star => {
        star.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            rateInput.value = value; // Устанавливаем значение в скрытое поле
            updateStars(value);
        });
    });

    function updateStars(value) {
        stars.forEach(star => {
            if (star.getAttribute("data-value") <= value) {
                star.classList.add("active");
            } else {
                star.classList.remove("active");
            }
        });
    }
});