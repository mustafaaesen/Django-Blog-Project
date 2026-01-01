/**
* Template Name: Story
* Template URL: https://bootstrapmade.com/story-bootstrap-blog-template/
* Updated: Aug 11 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  // --- Sayfa yüklendiğinde çalışacak genel başlangıç kodu ---
  document.addEventListener('DOMContentLoaded', () => {
    console.log("main.js aktif!");

    // ✅ Preloader güvenli kapatma
    const preloader = document.querySelector('#preloader');
    if (preloader) {
      setTimeout(() => {
        preloader.style.opacity = '0';
        setTimeout(() => {
          preloader.style.display = 'none';
        }, 500);
      }, 500); // preloader 1.5 saniye ekranda kalır
    }


    // ✅ AOS güvenli init
    try {
      if (typeof AOS !== 'undefined') {
        AOS.init({
          duration: 600,
          easing: 'ease-in-out',
          once: true,
          mirror: false
        });
      }
    } catch (err) {
      console.warn("AOS init hatası:", err);
    }

    // ✅ Swiper güvenli init
    try {
      if (typeof Swiper !== 'undefined') {
        document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
          let config = JSON.parse(
            swiperElement.querySelector(".swiper-config").innerHTML.trim()
          );
          new Swiper(swiperElement, config);
        });
      }
    } catch (err) {
      console.warn("Swiper init hatası:", err);
    }

    // ✅ PureCounter init
    try {
      new PureCounter();
    } catch (err) {
      console.warn("PureCounter hatası:", err);
    }
  });

  /**
   * Scroll durumuna göre body class ekleme
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader) return;
    if (!selectHeader.classList.contains('scroll-up-sticky') && 
        !selectHeader.classList.contains('sticky-top') && 
        !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobil menü aç/kapat
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');
  function mobileNavToogle() {
    document.body.classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');
  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

})();
