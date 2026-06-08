// ========== MyCard Oman - Premium Scripts ==========
(function() {
  'use strict';

  // ========== DOM Ready ==========
  document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initNavbar();
    initCard3D();
    initParallax();
    initFAQ();
    initMobileMenu();
    initThemeToggle();
    initSmoothScroll();
    initStatsCounter();
    initTestimonialCarousel();
  });

  // ========== Scroll Reveal Animation ==========
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');
    
    if (!('IntersectionObserver' in window)) {
      revealElements.forEach(el => el.classList.add('visible'));
      return;
    }

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(function(el) {
      observer.observe(el);
    });
  }

  // ========== Navbar Scroll Effect ==========
  function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', function() {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      lastScroll = currentScroll;
    }, { passive: true });
  }

  // ========== 3D Card Mouse Follow ==========
  function initCard3D() {
    const card = document.querySelector('.card-3d');
    const wrapper = document.querySelector('.card-3d-wrapper');
    if (!card || !wrapper) return;

    // Card Flip on Click
    card.addEventListener('click', function() {
      card.classList.toggle('flipped');
    });

    // Mouse Position Tracking for 3D tilt
    wrapper.addEventListener('mousemove', function(e) {
      const rect = wrapper.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = (y - centerY) / centerY * -8;
      const rotateY = (x - centerX) / centerX * 12;
      
      card.style.transform = 'translateY(-8px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
    });

    wrapper.addEventListener('mouseleave', function() {
      card.style.transform = '';
    });

    // Touch support for mobile
    wrapper.addEventListener('touchmove', function(e) {
      e.preventDefault();
      const rect = wrapper.getBoundingClientRect();
      const touch = e.touches[0];
      const x = touch.clientX - rect.left;
      const y = touch.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = (y - centerY) / centerY * -6;
      const rotateY = (x - centerX) / centerX * 8;
      
      card.style.transform = 'translateY(-4px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
    }, { passive: false });

    wrapper.addEventListener('touchend', function() {
      card.style.transform = '';
    });
  }

  // ========== Parallax Effect ==========
  function initParallax() {
    const parallaxLayers = document.querySelectorAll('.parallax-layer');
    if (!parallaxLayers.length) return;

    window.addEventListener('scroll', function() {
      const scrolled = window.pageYOffset;
      
      parallaxLayers.forEach(function(layer) {
        const speed = layer.getAttribute('data-parallax-speed') || 0.5;
        const yPos = scrolled * speed * 0.3;
        layer.style.transform = 'translateY(' + yPos + 'px)';
      });
    }, { passive: true });
  }

  // ========== FAQ Accordion ==========
  function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(function(item) {
      const question = item.querySelector('.faq-question');
      if (!question) return;

      question.addEventListener('click', function() {
        const isActive = item.classList.contains('active');
        
        // Close all
        faqItems.forEach(function(fi) {
          fi.classList.remove('active');
        });

        // Open clicked
        if (!isActive) {
          item.classList.add('active');
        }
      });
    });
  }

  // ========== Mobile Menu ==========
  function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    const body = document.body;

    if (!menuBtn || !mobileMenu) return;

    menuBtn.addEventListener('click', function() {
      const isOpen = mobileMenu.classList.contains('active');
      
      if (isOpen) {
        mobileMenu.classList.remove('active');
        body.style.overflow = '';
        menuBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
      } else {
        mobileMenu.classList.add('active');
        body.style.overflow = 'hidden';
        menuBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
      }
    });

    // Close menu when clicking a link
    const menuLinks = mobileMenu.querySelectorAll('a');
    menuLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        mobileMenu.classList.remove('active');
        body.style.overflow = '';
        menuBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
      });
    });
  }

  // ========== Theme Toggle (Light/Dark) ==========
  function initThemeToggle() {
    const toggle = document.querySelector('.theme-toggle');
    if (!toggle) return;

    // Check saved preference
    const savedTheme = localStorage.getItem('mycard-theme');
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    }

    toggle.addEventListener('click', function() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('mycard-theme', isDark ? 'dark' : 'light');
    });
  }

  // ========== Smooth Scroll for Anchor Links ==========
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
      anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        if (!target) return;

        e.preventDefault();
        const offset = 80; // Navbar height offset
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      });
    });
  }

  // ========== Stats Counter Animation ==========
  function initStatsCounter() {
    const statNumbers = document.querySelectorAll('.stat-number[data-count]');
    if (!statNumbers.length) return;

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-count'), 10);
          const duration = 2000;
          const start = performance.now();
          const startVal = 0;

          function update(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(startVal + (target - startVal) * easeOut);
            
            el.textContent = current.toLocaleString('en-US');
            
            if (progress < 1) {
              requestAnimationFrame(update);
            } else {
              el.textContent = target.toLocaleString('en-US');
            }
          }

          requestAnimationFrame(update);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(function(el) {
      observer.observe(el);
    });
  }

  // ========== Testimonial Auto-Carousel ==========
  function initTestimonialCarousel() {
    const carousel = document.querySelector('.testimonial-carousel');
    if (!carousel) return;

    const track = carousel.querySelector('.testimonial-track');
    const cards = carousel.querySelectorAll('.testimonial-card');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    
    if (!track || !cards.length) return;

    let currentIndex = 0;
    let autoPlayInterval;
    let isPaused = false;

    function goToSlide(index) {
      if (index < 0) index = cards.length - 1;
      if (index >= cards.length) index = 0;
      currentIndex = index;
      
      const offset = -currentIndex * 100;
      track.style.transform = 'translateX(' + offset + '%)';
    }

    function nextSlide() {
      goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      goToSlide(currentIndex - 1);
    }

    function startAutoPlay() {
      stopAutoPlay();
      autoPlayInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoPlay() {
      if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
      }
    }

    if (prevBtn) prevBtn.addEventListener('click', function() { prevSlide(); startAutoPlay(); });
    if (nextBtn) nextBtn.addEventListener('click', function() { nextSlide(); startAutoPlay(); });

    carousel.addEventListener('mouseenter', function() { stopAutoPlay(); });
    carousel.addEventListener('mouseleave', function() { startAutoPlay(); });

    // Touch support
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoPlay();
    }, { passive: true });

    track.addEventListener('touchend', function(e) {
      touchEndX = e.changedTouches[0].screenX;
      const diff = touchStartX - touchEndX;
      
      if (Math.abs(diff) > 50) {
        if (diff > 0) {
          nextSlide();
        } else {
          prevSlide();
        }
      }
      startAutoPlay();
    });

    startAutoPlay();
  }

  // ========== Material Selector Tabs ==========
  const materialTabs = document.querySelectorAll('.material-tab');
  const materialContents = document.querySelectorAll('.material-content');
  
  if (materialTabs.length && materialContents.length) {
    materialTabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        const target = this.getAttribute('data-material');
        
        materialTabs.forEach(function(t) { t.classList.remove('active'); });
        materialContents.forEach(function(c) { c.classList.remove('active'); });
        
        this.classList.add('active');
        const targetEl = document.querySelector('.material-content[data-material="' + target + '"]');
        if (targetEl) targetEl.classList.add('active');
      });
    });
  }

})();
