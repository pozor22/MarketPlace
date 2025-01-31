document.querySelectorAll('.product-slider').forEach(slider => {
  let currentIndex = 0;
  const items = slider.querySelectorAll('.slider-item');

  function showSlide(index) {
    items.forEach((item, i) => {
      item.style.display = i === index ? 'block' : 'none';
    });
  }

  showSlide(currentIndex);

  // Добавьте кнопки для управления (вперед/назад)
  const nextButton = document.createElement('button');
  nextButton.innerText = '→';
  nextButton.onclick = () => {
    currentIndex = (currentIndex + 1) % items.length;
    showSlide(currentIndex);
  };

  const prevButton = document.createElement('button');
  prevButton.innerText = '←';
  prevButton.onclick = () => {
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    showSlide(currentIndex);
  };

  slider.appendChild(prevButton);
  slider.appendChild(nextButton);
});