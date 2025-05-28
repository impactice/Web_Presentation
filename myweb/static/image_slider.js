document.addEventListener('DOMContentLoaded', function () {
    const sliderContainer = document.querySelector('.slider-image-slider-container');
    const slider = document.querySelector('.slider-image-slider');
    const prevButton = document.querySelector('.slider-prev-button');
    const nextButton = document.querySelector('.slider-next-button');
    const images = slider.querySelectorAll('img');
    const imageCount = images.length;
    let currentIndex = 0;
    let intervalId;
    const autoSlideInterval = 10000;

    // 이미지 슬라이더 너비 동적 조절
    slider.style.width = (imageCount * 100) + '%';
    images.forEach(img => {
        img.style.width = (100 / imageCount) + '%';
    });

    function updateSlider() {
        const translateX = -currentIndex * (100 / imageCount) + '%';
        slider.style.transform = 'translateX(' + translateX + ')';
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % imageCount;
        updateSlider();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + imageCount) % imageCount;
        updateSlider();
    }

    function startAutoSlide() {
        intervalId = setInterval(nextSlide, autoSlideInterval);
    }

    function stopAutoSlide() {
        clearInterval(intervalId);
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', () => {
            stopAutoSlide();
            prevSlide();
            startAutoSlide();
        });

        nextButton.addEventListener('click', () => {
            stopAutoSlide();
            nextSlide();
            startAutoSlide();
        });
    }

    if (sliderContainer) {
        sliderContainer.addEventListener('mouseenter', stopAutoSlide);
        sliderContainer.addEventListener('mouseleave', startAutoSlide);
    }

    startAutoSlide();
});