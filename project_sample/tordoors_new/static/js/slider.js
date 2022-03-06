import Swiper, { Navigation, Pagination, Thumbs, EffectFade } from 'swiper';
Swiper.use([Navigation, Pagination, Thumbs, EffectFade]);

$(function () {

    //Media Breakpoint PC
    const breakpointPc = window.matchMedia('(min-width: 1280px)');

    //Media Breakpoint MD
    const breakpointMD = window.matchMedia('(min-width: 1025px)');

    //Media Breakpoint XS
    const breakpointXs = window.matchMedia('(min-width: 768px)');

    //Init Produce Slider
    function slickProduceInit() {
        let slickProduce = $('.produce--slider');
        slickProduce.on('init', function(event, slick) {
            $(this).parent().parent().find('.slider__count .slider__count-total').text(slick.slideCount);
        })
        .slick({
            infinite: true,
            slidesToShow: 2,
            slidesToScroll: 1,
            touchThreshold: 100,
            arrows: true,
            prevArrow: slickProduce.parent().parent().find('.slider__nav .slider__nav-prev'),
            nextArrow: slickProduce.parent().parent().find('.slider__nav .slider__nav-next'),
            useTransform: true,
            speed: 1000,
            asNavFor: '.produce-menu--slider',
            responsive: [
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 1,
                  }
                },
              ]
        })
        .on('afterChange', function(event, slick, currentSlide, nextSlide){
            $(this).parent().parent().find('.slider__count .slider__count-current').html(currentSlide+1);
        });

        let slickProduceMenu = $('.produce-menu--slider');
        $(slickProduceMenu).slick({
            infinite: true,
            variableWidth: true,
            touchThreshold: 100,
            slidesToShow: 3,
            slidesToScroll: 1,
            centerMode: true,
            arrows: false,
            useTransform: true,
            focusOnSelect: true,
            speed: 1000,
            asNavFor: '.produce--slider',
        });
    };
    slickProduceInit();

    //Init Technologies Slider
    function slickTechnologiesInit() {
        let slickTechnologies = $('.technologies--slider');
        slickTechnologies.on('init', function(event, slick) {
            $(this).parent().parent().find('.slider__count .slider__count-total').text(slick.slideCount);
        })
        .slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            touchThreshold: 100,
            variableWidth: false,
            arrows: true,
            prevArrow: slickTechnologies.parent().parent().find('.slider__nav .slider__nav-prev'),
            nextArrow: slickTechnologies.parent().parent().find('.slider__nav .slider__nav-next'),
            useTransform: true,
            speed: 1000,
            asNavFor: '.technologies-menu--slider',
            responsive: [
                {
                  breakpoint: 768,
                  settings: {
                    variableWidth: true,
                  }
                },
              ]
        })
        .on('afterChange', function(event, slick, currentSlide, nextSlide){
            $(this).parent().parent().find('.slider__count .slider__count-current').html(currentSlide+1);
        });

        let slickTechnologiesMenu = $('.technologies-menu--slider');
        $(slickTechnologiesMenu).slick({
            infinite: true,
            variableWidth: true,
            touchThreshold: 100,
            slidesToShow: 3,
            slidesToScroll: 1,
            centerMode: true,
            arrows: false,
            useTransform: true,
            focusOnSelect: true,
            speed: 1000,
            asNavFor: '.technologies--slider',
        });
    };
    slickTechnologiesInit();

    //Init Goods Slider
    function slickGoodsInit() {
        let slickGoods = $('.goods--slider');
        slickGoods.slick({
            infinite: true,
            slidesToShow: 4,
            slidesToScroll: 1,
            touchThreshold: 100,
            arrows: true,
            prevArrow: slickGoods.parent().parent().find('.slider__nav .slider__nav-prev'),
            nextArrow: slickGoods.parent().parent().find('.slider__nav .slider__nav-next'),
            useTransform: true,
            speed: 1000,
            responsive: [
                {
                  breakpoint: 1025,
                  settings: {
                    slidesToShow: 3,
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 1,
                    variableWidth: true,
                  }
                },
              ]
        });
    };
    slickGoodsInit();

    //Init Gallery Slider
    function slickGalleryInit() {
        let slickGallery = $('.gallery--slider');
        slickGallery.slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            touchThreshold: 100,
            arrows: true,
            prevArrow: slickGallery.parent().find('.slider__fullnav-prev'),
            nextArrow: slickGallery.parent().find('.slider__fullnav-next'),
            useTransform: true,
            speed: 1000,
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        variableWidth: true,
                    }
                },
            ]
        });
    };
    slickGalleryInit();

    //Init Gallery Default Slider
    function swiperGalleryDefaultInit() {
        $(".gallery--default-slider").each(function (index, element) {
            let swiperGalleryDefault;
            let swiperGalleryDefaultSlider = $(element);
            const breakpointChecker = function() {
                if (breakpointXs.matches === true) {
                    if (swiperGalleryDefault !== undefined) swiperGalleryDefault.destroy(true, true);
                        return;
                    } else if (breakpointXs.matches === false) {
                        return swiperGalleryDefaultSettings();
                    }
            };
            const swiperGalleryDefaultSettings = function() {
                swiperGalleryDefault = new Swiper (element, {
                    slidesPerView: 'auto',
                    speed: 800,
                });
            };
            if (swiperGalleryDefaultSlider.length > 0) {
                breakpointXs.addListener(breakpointChecker);
                breakpointChecker();
            }
        });
    }
    swiperGalleryDefaultInit();

    //Advantages Slider
    function slickAdvantagesInit() {
        let advantagesSlider;
        let slickAdvantagesSliders = $('.advantages--slider');
        const breakpointChecker = function() {
            if (breakpointXs.matches === true) {
                if (advantagesSlider !== undefined)
                    advantagesSlider.slick('unslick');
                    return;
                } else if (breakpointXs.matches === false) {
                    return advantagesSliderSettings();
                }
        };
        const advantagesSliderSettings = function() {
            advantagesSlider = slickAdvantagesSliders.slick({
                infinite: true,
                slidesToShow: 1,
                slidesToScroll: 1,
                touchThreshold: 20,
                arrows: false,
                useTransform: true,
                speed: 800,
                variableWidth: true,
            });
        };
        breakpointXs.addListener(breakpointChecker);
        breakpointChecker();
    }
    slickAdvantagesInit();

    //Dignity Slider
    function slickDignityInit() {
        let dignitySlider;
        let slickDignitySliders = $('.dignity--slider');
        const breakpointChecker = function() {
            if (breakpointXs.matches === true) {
                if (dignitySlider !== undefined)
                    dignitySlider.slick('unslick');
                    return;
                } else if (breakpointXs.matches === false) {
                    return dignitySliderSettings();
                }
        };
        const dignitySliderSettings = function() {
            dignitySlider = slickDignitySliders.slick({
                infinite: true,
                slidesToShow: 1,
                slidesToScroll: 1,
                touchThreshold: 20,
                arrows: false,
                useTransform: true,
                speed: 800,
                variableWidth: true,
                centerMode: true,
            });
        };
        breakpointXs.addListener(breakpointChecker);
        breakpointChecker();
    }
    slickDignityInit();

    //Init Partners Slider
    function slickPartnersInit() {
        let slickPartners = $('.partners-review--slider');
        slickPartners.slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            touchThreshold: 100,
            fade: true,
            arrows: true,
            prevArrow: slickPartners.parent().find('.slider__fullnav-prev'),
            nextArrow: slickPartners.parent().find('.slider__fullnav-next'),
            useTransform: true,
            speed: 700,
        });
    };
    slickPartnersInit();

    //Init Partners Slider
    function slickPartnersLogoInit() {
        let slickPartnersLogo = $('.partners-logo--slider');
        slickPartnersLogo.slick({
            infinite: true,
            slidesToShow: 3,
            touchThreshold: 1000,
            arrows: false,
            useTransform: true,
            speed: 600,
            variableWidth: true,
            autoplay: true,
            autoplaySpeed: 2000,
            pauseOnHover: true
        });
    };
    slickPartnersLogoInit();

    //Init Product Option Slider
    function slickOptionInit() {
        $(".product__option").each(function (index, element) {
            const $optionSlider = $(element).find(".product__option--slider");

            //Margin Slides
            const spaceBetween = 32;

            //Slides
            const $slides = $(element).find(".product__option-item");
            let slidesCount = $slides.length;
            let showSlides = 0;

            //Nav
            const $nav = $(element).find(".slider__nav--visibility");
            const $prevNavBtn = $($nav).find(".slider__nav-prev");
            const $nextNavBtn = $($nav).find(".slider__nav-next");

            //Update Slider
            function setArrowsVisibilty() {
                //Container Width
                const sectionWidth = Math.round($(element).width());

                //Slides Width
                const slidesSumWidth =
                    Array.from($slides).reduce(function (sum, slide) {
                        return Math.round($(slide).width() + spaceBetween + sum);
                    }, 0) - spaceBetween;

                //SlidesToShow option
                showSlides = (sectionWidth / slidesSumWidth) * slidesCount;

                if (sectionWidth - slidesSumWidth > -2) {
                    $nav.attr("data-hide", true);
                    $optionSlider.removeClass('slider__shadow--active');
                    $(element).find(".product__option--slider.slick-initialized").slick('slickSetOption', 'slidesToShow', showSlides, true);
                } else {
                    $nav.attr("data-hide", false);
                    $optionSlider.addClass('slider__shadow--active');
                    $(element).find(".product__option--slider.slick-initialized").slick('slickSetOption', 'slidesToShow', showSlides, true);
                }
            }

            setArrowsVisibilty();
            $(window).resize(function () {
                setArrowsVisibilty();
            });

            //Init Slider
            $optionSlider.not('.slick-initialized').slick({
                infinite: false,
                touchThreshold: 13,
                arrows: true,
                prevArrow: $prevNavBtn,
                nextArrow: $nextNavBtn,
                slidesToShow: showSlides,
                useTransform: true,
                speed: 1000,
                variableWidth: true,
            });
        });
    };
    slickOptionInit();

    //Init Documents Slider
    function slickDocumentsInit() {
        let slickDocuments = $('.documents--slider');
        slickDocuments.slick({
            infinite: true,
            touchThreshold: 20,
            arrows: true,
            prevArrow: slickDocuments.parent().find('.slider__nav .slider__nav-prev'),
            nextArrow: slickDocuments.parent().find('.slider__nav .slider__nav-next'),
            useTransform: true,
            speed: 1000,
            variableWidth: true,
        });
    };
    slickDocumentsInit();

    //Init Articles Slider
    function swiperArticlesInit() {
        $(".articles--slider").each(function (index, element) {
            let swiperArticles;
            let swiperArticlesSlider = $(element);
            const breakpointChecker = function() {
                if (breakpointMD.matches === true) {
                    if (swiperArticles !== undefined) swiperArticles.destroy(true, true);
                        return;
                    } else if (breakpointMD.matches === false) {
                        return swiperArticlesSettings();
                    }
            };
            const swiperArticlesSettings = function() {
                swiperArticles = new Swiper (element, {
                    slidesPerView: 'auto',
                    speed: 800,
                });
            };
            if (swiperArticlesSlider.length > 0) {
                breakpointMD.addListener(breakpointChecker);
                breakpointChecker();
            }
        });
    }
    swiperArticlesInit();

    //Init News Slider
    function swiperNewsInit() {
        $(".news--slider").each(function (index, element) {
            let swiperNews;
            let swiperNewsSlider = $(element);
            const breakpointChecker = function() {
                if (breakpointPc.matches === true) {
                    if (swiperNews !== undefined) swiperNews.destroy(true, true);
                        return;
                    } else if (breakpointPc.matches === false) {
                        return swiperNewsSettings();
                    }
            };
            const swiperNewsSettings = function() {
                swiperNews = new Swiper (element, {
                    slidesPerView: 'auto',
                    speed: 800,
                });
            };
            if (swiperNewsSlider.length > 0) {
                breakpointPc.addListener(breakpointChecker);
                breakpointChecker();
            }
        });
    }
    swiperNewsInit();

    //Init Furniture Slider
    function swiperFurnitureInit() {
        let swiperFurnitureThumbs = new Swiper('.furniture--thumb', {
            slidesPerView: 'auto',
            freeMode: true,
            watchSlidesVisibility: true,
            watchSlidesProgress: true,
        });

        let swiperFurnitureParent = new Swiper('.furniture--slider', {
            slidesPerView: 'auto',
            thumbs: {
                swiper: swiperFurnitureThumbs
            },
            speed: 1000,
        });
    };
    swiperFurnitureInit();

});
