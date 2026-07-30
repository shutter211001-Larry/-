document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const counter = document.getElementById('slide-counter');
    const progressBar = document.getElementById('progress-bar-fill');
    
    let currentSlide = 0;
    const totalSlides = slides.length;

    // 更新 UI 狀態
    function updateUI() {
        slides.forEach((slide, index) => {
            if (index === currentSlide) {
                slide.classList.add('active');
                // 每次進入新頁面，重置捲軸位置到最上方
                const contentArea = slide.querySelector('.content-area');
                if (contentArea) contentArea.scrollTop = 0;
            } else {
                slide.classList.remove('active');
                // 隱藏非當前頁面的 fragment
                const fragments = slide.querySelectorAll('.fragment');
                fragments.forEach(f => f.classList.remove('visible'));
            }
        });

        counter.textContent = `${currentSlide + 1} / ${totalSlides}`;
        prevBtn.disabled = currentSlide === 0;
        nextBtn.disabled = currentSlide === totalSlides - 1;

        const progressPercentage = (currentSlide / (totalSlides - 1)) * 100;
        progressBar.style.width = `${progressPercentage}%`;
    }

    // 導航邏輯 (結合 Fragment)
    function goNext() {
        // 先尋找當前頁面是否有尚未顯示的 fragment
        const currentSlideEl = slides[currentSlide];
        const hiddenFragments = currentSlideEl.querySelectorAll('.fragment:not(.visible)');
        
        if (hiddenFragments.length > 0) {
            // 亮出下一個 fragment
            const nextFrag = hiddenFragments[0];
            nextFrag.classList.add('visible');
            
            // 對話演示：只捲動到剛好能看見新氣泡的位置，避免滑過頭
            setTimeout(() => {
                nextFrag.scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest'
                });
            }, 100);
        } else if (currentSlide < totalSlides - 1) {
            // 切換到下一頁
            currentSlide++;
            updateUI();
        }
    }

    function goPrev() {
        const currentSlideEl = slides[currentSlide];
        const visibleFragments = currentSlideEl.querySelectorAll('.fragment.visible');
        
        if (visibleFragments.length > 0) {
            // 隱藏上一個 fragment
            visibleFragments[visibleFragments.length - 1].classList.remove('visible');
            
            // 往上一步時，稍微往上捲動
            const contentArea = currentSlideEl.querySelector('.content-area');
            if (contentArea && visibleFragments.length > 1) {
                setTimeout(() => {
                    visibleFragments[visibleFragments.length - 2].scrollIntoView({
                        behavior: 'smooth',
                        block: 'nearest'
                    });
                }, 100);
            }
        } else if (currentSlide > 0) {
            // 切換到上一頁
            currentSlide--;
            updateUI();
            
            // 返回上一頁時，讓該頁的 fragment 全部顯示
            setTimeout(() => {
                const prevSlideEl = slides[currentSlide];
                const fragments = prevSlideEl.querySelectorAll('.fragment');
                fragments.forEach(f => f.classList.add('visible'));
            }, 50); // 給一點延遲避免閃爍
        }
    }

    nextBtn.addEventListener('click', goNext);
    prevBtn.addEventListener('click', goPrev);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') {
            goNext();
            if(e.key === ' ') e.preventDefault();
        } else if (e.key === 'ArrowLeft') {
            goPrev();
        }
    });

    // 初始載入
    updateUI();
});
