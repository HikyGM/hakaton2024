
(function ($) {
	"use strict";
		gsap.registerPlugin(ScrollTrigger);


	// preloader
	$(window).on('load', function () {
		$('#loading').delay(10).fadeOut('slow');
		$('body').delay(10).css({ 'overflow': 'visible' });
	});

	// meanmenu
	$('#mobile-menu').meanmenu({
		meanMenuContainer: '.mobile-menu',
		meanScreenWidth: "992"
	});

	// MOBILE MENU CLICKABLE 
	$('.open-mobile-menu').on('click', function () {
		$('.mobile_info_open').addClass('show');
		$('.offcanvas-overlay').addClass('overlay-open');
	})

	$('.close_info,.offcanvas-overlay,.mobile_one_page li.menu-item a.nav-link').on('click', function () {
		$('.mobile_info_open').removeClass('show');
		$('.offcanvas-overlay').removeClass('overlay-open');
	});

	const tilt = $('.js-tilt').tilt();


	//   7. Header Sticky
	$(window).on('scroll', function () {
		var scroll = $(window).scrollTop();
		if (scroll < 245) {
			$(".mariox__header, .responsive_mobile_menu, .mariox__two-wrapper").removeClass("sticky");
		} else {
			$(".mariox__header, .responsive_mobile_menu, .mariox__two-wrapper").addClass("sticky");
		}
	});

	// wow js active 

	new WOW().init();

	/* 


	-----------------------------
	SLICK ACTIVATION BLOG HOMEPAGE ONE
	-----------------------------
	
	*/
	//testimonial single active

	$('.testimonail-active').slick({

		slidesToShow: 1,
  
		slidesToScroll: 1,
  
		arrows: false,
  
		fade: true,
  
		asNavFor: '.testimonial-img-active',
  
	 });
  
	 $('.testimonial-img-active').slick({
  
		slidesToShow: 3,
  
		slidesToScroll: 1,
  
		asNavFor: '.testimonail-active',
  
		dots: false,
  
		centerMode: true,
  
		focusOnSelect: true,
  
		centerPadding: '0px',
  
		arrows: false,
  
		responsive: [{
  
		  breakpoint: 1024,
  
		  settings: {
  
			 slidesToShow: 3,
  
			 slidesToScroll: 1,
  
			 infinite: true,
  
			 dots: false,
  
		  }
  
		},
  
		{
  
		  breakpoint: 992,
  
		  settings: {
  
			 slidesToShow: 3,
  
			 slidesToScroll: 2
  
		  }
  
		},
  
		{
  
		  breakpoint: 767,
  
		  settings: {
  
			 slidesToShow: 1,
  
			 slidesToScroll: 1
  
		  }
  
		},
  
		{
  
		  breakpoint: 480,
  
		  settings: {
  
			 slidesToShow: 1,
  
			 slidesToScroll: 1
  
		  }
  
		}
  
		]
  
	 });
  




	 var team = new Swiper(".mariox__team-activition", {
		navigation: {
		  nextEl: ".swiper-button-next",
		  prevEl: ".swiper-button-prev",
		},
		loop: true,
		speed: 1000,
		slidesPerView: 1,
	 });


	// brand active 
	var brand = new Swiper(".marioxx__brand-active", {
		navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
		},
		loop: true,
		speed: 1000,
		slidesPerView: 5,
		breakpoints: {
			// when window width is >= 320px
			320: {
			  slidesPerView: 2,
			  spaceBetween: 20
			},
			// when window width is >= 480px
			480: {
			  slidesPerView: 3,
			  spaceBetween: 30
			},
			// when window width is >= 640px
			640: {
			  slidesPerView: 4,
			  spaceBetween: 40
			}
		 }
	});

		var testimonial3 = new Swiper(".marioxxx__testimonial-active", {
			navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
			},
			loop: true,
			speed: 1000,
			slidesPerView: 1,
		});







		  var testimonial3 = new Swiper(".marioxxx__testimonial-active", {
			navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
			},
			loop: true,
			speed: 1000,
			slidesPerView: 1,
			
		});



		


	  

})(jQuery);