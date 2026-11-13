// Interactive SIH Presentation Deck Controller

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlide = 1;

  const progressBar = document.getElementById('progress-bar');
  const slideCounter = document.getElementById('slide-counter');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnTheme = document.getElementById('btn-theme');
  const btnFullscreen = document.getElementById('btn-fullscreen');
  const btnNotes = document.getElementById('btn-notes');
  const btnGrid = document.getElementById('btn-grid');
  const notesDrawer = document.getElementById('notes-drawer');
  const notesContent = document.getElementById('notes-content');
  const btnCloseNotes = document.getElementById('btn-close-notes');
  const gridModal = document.getElementById('grid-modal');
  const btnCloseGrid = document.getElementById('btn-close-grid');
  const gridThumbnails = document.getElementById('grid-thumbnails');

  // Populate Grid Thumbnails
  slides.forEach((slide, idx) => {
    const slideNum = idx + 1;
    const title = slide.querySelector('h2') ? slide.querySelector('h2').textContent : (slide.querySelector('.hero-title') ? slide.querySelector('.hero-title').textContent : `Slide ${slideNum}`);
    
    const card = document.createElement('div');
    card.className = `thumb-card ${slideNum === 1 ? 'active' : ''}`;
    card.dataset.slide = slideNum;
    card.innerHTML = `
      <div class="thumb-num">SLIDE ${slideNum}</div>
      <div class="thumb-title">${title.replace(/<[^>]*>?/gm, '').slice(0, 48)}...</div>
    `;
    card.addEventListener('click', () => {
      goToSlide(slideNum);
      closeGrid();
    });
    gridThumbnails.appendChild(card);
  });

  function updateSlide(newSlide) {
    if (newSlide < 1 || newSlide > totalSlides) return;
    currentSlide = newSlide;

    slides.forEach(s => s.classList.remove('active'));
    const activeSlideEl = document.querySelector(`.slide[data-slide="${currentSlide}"]`);
    if (activeSlideEl) activeSlideEl.classList.add('active');

    // Update Progress
    const pct = ((currentSlide) / totalSlides) * 100;
    progressBar.style.width = `${pct}%`;

    // Update Counter
    slideCounter.textContent = `${currentSlide} / ${totalSlides}`;

    // Update Buttons
    btnPrev.disabled = currentSlide === 1;
    btnNext.disabled = currentSlide === totalSlides;

    // Update Speaker Notes
    if (activeSlideEl && activeSlideEl.dataset.notes) {
      notesContent.textContent = activeSlideEl.dataset.notes;
    } else {
      notesContent.textContent = "No specific notes for this slide.";
    }

    // Update Active Thumbnail
    document.querySelectorAll('.thumb-card').forEach(tc => {
      tc.classList.toggle('active', parseInt(tc.dataset.slide) === currentSlide);
    });
  }

  function goToSlide(n) {
    updateSlide(n);
  }

  function nextSlide() {
    if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
  }

  function prevSlide() {
    if (currentSlide > 1) updateSlide(currentSlide - 1);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const target = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', target);
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  function toggleNotes() {
    notesDrawer.classList.toggle('open');
  }

  function openGrid() {
    gridModal.classList.add('open');
  }

  function closeGrid() {
    gridModal.classList.remove('open');
  }

  // Event Listeners
  btnNext.addEventListener('click', nextSlide);
  btnPrev.addEventListener('click', prevSlide);
  btnTheme.addEventListener('click', toggleTheme);
  btnFullscreen.addEventListener('click', toggleFullscreen);
  btnNotes.addEventListener('click', toggleNotes);
  if (btnCloseNotes) btnCloseNotes.addEventListener('click', () => notesDrawer.classList.remove('open'));
  btnGrid.addEventListener('click', openGrid);
  if (btnCloseGrid) btnCloseGrid.addEventListener('click', closeGrid);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      e.preventDefault();
      nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      prevSlide();
    } else if (e.key.toLowerCase() === 'f') {
      toggleFullscreen();
    } else if (e.key.toLowerCase() === 'n') {
      toggleNotes();
    } else if (e.key.toLowerCase() === 'g') {
      if (gridModal.classList.contains('open')) closeGrid(); else openGrid();
    } else if (e.key.toLowerCase() === 't') {
      toggleTheme();
    } else if (e.key === 'Escape') {
      closeGrid();
      notesDrawer.classList.remove('open');
    }
  });

  // Init
  updateSlide(1);
});

