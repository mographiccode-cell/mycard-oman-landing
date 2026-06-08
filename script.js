// ========== MyCard Oman - Premium Scripts V2 ==========
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initNavbar();
    initInviteCard3D();
    initFAQ();
    initMobileMenu();
    initSmoothScroll();
    initStatsCounter();
  });

  // ========== Scroll Reveal ==========
  function initScrollReveal() {
    var elements = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
      elements.forEach(function(el) { el.classList.add('visible'); });
      return;
    }
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    elements.forEach(function(el) { observer.observe(el); });
  }

  // ========== Navbar ==========
  function initNavbar() {
    var navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 50) navbar.classList.add('scrolled');
      else navbar.classList.remove('scrolled');
    }, { passive: true });
  }

  // ========== Invitation Card 3D Effect ==========
  function initInviteCard3D() {
    var card = document.querySelector('.card-invite');
    var wrapper = document.querySelector('.card-invite-wrapper');
    if (!card || !wrapper) return;

    wrapper.addEventListener('mousemove', function(e) {
      var rect = wrapper.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      var cx = rect.width / 2;
      var cy = rect.height / 2;
      var rx = (y - cy) / cy * -6;
      var ry = (x - cx) / cx * 10;
      card.style.transform = 'translateY(-4px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
    });

    wrapper.addEventListener('mouseleave', function() { card.style.transform = ''; });

    wrapper.addEventListener('touchmove', function(e) {
      e.preventDefault();
      var rect = wrapper.getBoundingClientRect();
      var t = e.touches[0];
      var rx = (t.clientY - rect.top - rect.height/2) / (rect.height/2) * -4;
      var ry = (t.clientX - rect.left - rect.width/2) / (rect.width/2) * 6;
      card.style.transform = 'translateY(-2px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
    }, { passive: false });

    wrapper.addEventListener('touchend', function() { card.style.transform = ''; });
  }

  // ========== FAQ ==========
  function initFAQ() {
    var items = document.querySelectorAll('.faq-item');
    items.forEach(function(item) {
      var q = item.querySelector('.faq-question');
      if (!q) return;
      q.addEventListener('click', function() {
        var isActive = item.classList.contains('active');
        items.forEach(function(i) { i.classList.remove('active'); });
        if (!isActive) item.classList.add('active');
      });
    });
  }

  // ========== Mobile Menu ==========
  function initMobileMenu() {
    var btn = document.querySelector('.mobile-menu-btn');
    var menu = document.querySelector('.mobile-menu');
    var body = document.body;
    if (!btn || !menu) return;

    var openIcon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
    var closeIcon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

    function close() {
      menu.classList.remove('active');
      body.style.overflow = '';
      btn.innerHTML = openIcon;
    }

    btn.addEventListener('click', function() {
      if (menu.classList.contains('active')) { close(); }
      else {
        menu.classList.add('active');
        body.style.overflow = 'hidden';
        btn.innerHTML = closeIcon;
      }
    });

    menu.querySelectorAll('a').forEach(function(link) { link.addEventListener('click', close); });
  }

  // ========== Smooth Scroll ==========
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(a) {
      a.addEventListener('click', function(e) {
        var id = this.getAttribute('href');
        if (id === '#') return;
        var target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - 70, behavior: 'smooth' });
      });
    });
  }

  // ========== Stats Counter ==========
  function initStatsCounter() {
    var nums = document.querySelectorAll('.stat-number[data-count]');
    if (!nums.length) return;
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var target = parseInt(el.getAttribute('data-count'), 10);
          var start = performance.now();
          var duration = 2000;
          function update(now) {
            var p = Math.min((now - start) / duration, 1);
            var val = Math.floor(target * (1 - Math.pow(1 - p, 3)));
            el.textContent = val.toLocaleString('en-US');
            if (p < 1) requestAnimationFrame(update);
            else el.textContent = target.toLocaleString('en-US');
          }
          requestAnimationFrame(update);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    nums.forEach(function(el) { observer.observe(el); });
  }
})();
