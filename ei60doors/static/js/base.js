import {
    getScrollbarWidth
} from './scrollbar-width';

$(function () {

    //Fix Transition CSS
    $('body').removeClass('fix-anim');

    //Init Phone Mask
    $(document).on('focus', 'input[name*="phone"]', function() {
        $(this).mask('+7 (999) 999-99-99');
    });

    //Wrap for Table
    $(".placeholder table").wrap('<div class="table-wrap"></div>');

    //Wrap for Iframe
    let placeholderVideo = $('.placeholder iframe');
    placeholderVideo.each(function (index, item) {
        let videoMaxWidth = $(item).attr('width');
        $(item).wrap('<div class="iframe-wrap" style="max-width: ' + videoMaxWidth + 'px;"></div>');
    });

    //Visible search
    $('.search-input').removeClass('search-input--hidden');

    //Check Anchor Margin
    let headeFixedHeight = 0;
    headeFixedHeight = $('.header').height();

    //Header Shadow
    $(window).scroll(function(){
        $('.header--dark').toggleClass('active', $(this).scrollTop() > 0);
    });
    if ($(window).scrollTop() > 0) {
        $('.header--dark').addClass('active');
    }

    //Open/Close Header Menu function
    function openHeaderMenu() {
        setTimeout( function(){$('.header__list-header').addClass('open');}, 900);
        setTimeout( function(){$('.header__list-body').addClass('open');}, 950);
        $('.header__overlay').addClass('active');
        $('.header__burger').addClass('active');
        $('.header__list').addClass('anim--active');
        $('.header__list').addClass('open');
        $('body').addClass("noscroll");

        $('body').css('margin-right', getScrollbarWidth() + 'px');
        $('.header').css('padding-right', getScrollbarWidth() + 'px');
    }
    function closeHeaderMenu() {
        setTimeout( function(){$('.header__list-header').removeClass('open');}, 250);
        setTimeout( function(){$('.header__list-body').removeClass('open');}, 100);
        setTimeout( function() {
            $('.header__overlay').removeClass('active');
            $('.header__burger').removeClass('active');
            $('.header__list').removeClass('open');
            $('body').removeClass("noscroll");

            $('body').css('margin-right', '0px');
            $('.header').css('padding-right', '0px');
        }, 500);
    };

    //Header menu toggle
	$('.header__burger').on('click', function(event) {
		event.preventDefault();

        if (!$('.header__burger').hasClass('active-modal')) {
            if ($('.header__list').hasClass('open')) {
                closeHeaderMenu();
            } else {
                openHeaderMenu();
            }
        }
	});

	//Close menu on overlay
	$('.header__overlay').on('click', function() {
        closeHeaderMenu();
	});

    //Header menu children
    $('.header__menu-icon').on('click', function() {
        $(this).toggleClass('active');
        $(this).parent().next().slideToggle();
    });
    $('.header__submenu-title').on('click', function() {
        $(this).toggleClass('active');
        $(this).next().slideToggle();
    });

    //Toggle Text
    $.fn.extend({
        toggleText: function (a, b) {
            if (this.text() == a) {
                this.text(b);
            }
            else {
                this.text(a)
            }
        }
    });

    //Division Load Items
    let galleryGridHeight = $('.gallery__grid-overflow').outerHeight(true);
    if (galleryGridHeight > 1300) {
        $('.gallery__grid-overflow').addClass('gallery__grid-load');
        $('.gallery__grid-more').addClass('active');
    }
    $('.gallery__grid-more').on('click', function() {
        $('.gallery__grid-overflow').toggleClass('gallery__grid-load');
        $(this).toggleText('Скрыть', 'Смотреть ещё');

        if ($('.gallery__grid-overflow').hasClass('gallery__grid-load')) {
            $('html, body').animate( { scrollTop: $('.gallery__grid-overflow').offset().top - headeFixedHeight - 20 }, 0);
        }
    });

    //Add to title gallery img link
    $('.gallery__grid-btn').click(function() {
        let imgLink = $(location).attr('protocol') + '//' + $(location).attr('host') + $(this).prev().attr('href');
        let link = $("<a />", {
            href: imgLink,
            text: imgLink,
            target: '_blank'
        });
        $('#wantsimilar-modal .modal__subtitle').html(link);
        $('#wantsimilar-modal #id_want_similar-image_url').val(imgLink);
    });

    //Init Slidable Tabs
    function slidableTabsInit() {
        $('.slidable-tabs').slidable({
            minimal: 220,
        });
    }
    slidableTabsInit();

    //Tabs
    const tabsDefault = $('.tabs');
    tabsDefault.each(function(index, item) {
        $(item).find('.tabs__link:first-child').addClass('active');
        $(item).find('.tabs__link').on('click', function(event) {
            event.preventDefault();
            if(!$(this).hasClass('active')) {
                $(item).find('.tabs__link').removeClass('active');
                $(this).toggleClass('active');
                $(item).find('.tabs__item').hide();
                let dataTabs = $(this).attr('data-tabs-link');
                $(item).find('.tabs__item[data-tabs-item="'+ dataTabs +'"]').fadeIn();
                slidableTabsInit();
            }
        });
    });

    //Toggle sitemap
    $('.sitemap__item-icon').on('click', function(e) {
        $(this).parent().toggleClass('active');
        $(this).parent().next().slideToggle();
    });

    //Open/Close Filter Price
    $(".filter-open").on("click", function() {
        $('.filter__option').addClass('open');
    });
    $(".filter-close").on("click", function() {
        $('.filter__option').removeClass('open');
    });
    $(document).click(function(e) {
        let div = $(".filter__option");
        let div2 = $(".filter-open");
        if (!div.is(e.target) && div.has(e.target).length === 0 && !div2.is(e.target) && div2.has(e.target).length === 0) {
            $('.filter__option').removeClass('open');
        }
    });

});
