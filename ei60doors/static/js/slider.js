//Import swiper
import Swiper, {
    Navigation,
    Pagination,
    EffectFade,
    Autoplay,
    Thumbs,
    Parallax,
    Scrollbar,
} from 'swiper';

Swiper.use([
    Navigation,
    Pagination,
    EffectFade,
    Autoplay,
    Thumbs,
    Parallax,
    Scrollbar,
]);

//Import variable
import {
    breakpointXSMin
} from './match-media';

$(function () {

    //Init Intro Slider
    function swiperIntroInit() {
        const swiperIntroSliderBlock = document.querySelector('.intro--slider');
        if ($(swiperIntroSliderBlock).length > 0) {
            let swiperIntro = new Swiper('.intro--slider', {
                slidesPerView: 'auto',
                loop: true,
                parallax: true,
                speed: 1000,
                autoplay: {
                    delay: 2000,
                },
                pagination: {
                    el: swiperIntroSliderBlock.parentElement.querySelector('.intro__pagination'),
                    clickable: true,
                },
                navigation: {
                    nextEl: swiperIntroSliderBlock.querySelector('.intro__arrow-next'),
                    prevEl: swiperIntroSliderBlock.querySelector('.intro__arrow-prev')
                },
            });

            swiperIntro.on('slideChange', function () {
                $('.intro__slider-item').removeClass('intro__slider-item--first');
            });

            $(swiperIntroSliderBlock).mouseenter(function() {
                swiperIntro.autoplay.stop();
            });
            $(swiperIntroSliderBlock).mouseleave(function() {
                swiperIntro.autoplay.start();
            });
        }
    };
    swiperIntroInit();

    //Init Partners Slider
    function swiperPartnersInit() {
        const swiperPartnersBlock = document.querySelectorAll('.partners--slider');
        swiperPartnersBlock.forEach((el) => {
            let swiperPartners = new Swiper(el, {
                slidesPerView: 'auto',
                loop: false,
                speed: 800,
            });
        });
    };
    swiperPartnersInit();

    //Init Goods Slider
    function swiperGoodsInit() {
        const swiperGoodsBlock = document.querySelectorAll('.goods--slider');
        swiperGoodsBlock.forEach((el) => {
            let swiperGoods = new Swiper(el, {
                slidesPerView: 'auto',
                loop: true,
                speed: 800,
                autoplay: {
                    delay: 3000,
                    pauseOnMouseEnter: true,
                },
                pagination: {
                    el: '.slider__pagination',
                    type: 'bullets',
                    clickable: true,
                    dynamicBullets: true,
                },
            });
        });
    };
    swiperGoodsInit();

    //Init Product Gallery Slider
    function swiperProductGalleryInit() {
        const swiperProductGallery = document.querySelectorAll('.product__gallery');
        swiperProductGallery.forEach((el) => {
            let swiperProductGalleryThumbs = new Swiper(el.querySelector('.product--thumb'), {
                slidesPerView: 'auto',
                speed: 800,
            });
            let swiperProductGalleryParent = new Swiper(el.querySelector('.product--slider'), {
                slidesPerView: 'auto',
                speed: 800,
                thumbs: {
                    swiper: swiperProductGalleryThumbs,
                    autoScrollOffset: 4
                }
            });
        });
    };
    swiperProductGalleryInit();

    //Init Facing Slider
    function swiperFacingInit() {
        const swiperFacingBlock = document.querySelectorAll('.facing__slider');
        swiperFacingBlock.forEach((el) => {
            let swiperFacing = new Swiper(el.querySelector('.facing--slider'), {
                slidesPerView: 'auto',
                observer: true,
                observeParents: true,
                speed: 800,
                scrollbar: {
                    el: '.swiper-scrollbar',
                    draggable: true,
                },
            });
        });
    };
    swiperFacingInit();

    //Init Gallery Default Slider
    function swiperGalleryDefaultInit() {
        $(".gallery__default--slider").each(function (index, element) {
            let swiperGalleryDefault;
            let swiperGalleryDefaultSlider = $(element);
            const breakpointChecker = function() {
                if (breakpointXSMin.matches === true) {
                    if (swiperGalleryDefault !== undefined) swiperGalleryDefault.destroy(true, true);
                        return;
                    } else if (breakpointXSMin.matches === false) {
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
                breakpointXSMin.addListener(breakpointChecker);
                breakpointChecker();
            }
        });
    }
    swiperGalleryDefaultInit();

    //Init Tags Slider
    function swiperTagsSliderInit() {
        const swiperTagsSliderBlock = document.querySelector('.tags--slider');
        if ($(swiperTagsSliderBlock).length > 0) {
            let swiperTagsSlider = new Swiper(swiperTagsSliderBlock, {
                slidesPerView: 'auto',
                speed: 800,
                autoplay: {
                    delay: 2000,
                    stopOnLastSlide: true
                },
                freeMode: true,
            });

            $(swiperTagsSliderBlock).mouseenter(function() {
                swiperTagsSlider.autoplay.stop();
            });
            $(swiperTagsSliderBlock).mouseleave(function() {
                swiperTagsSlider.autoplay.start();
            });
        }
    };
    swiperTagsSliderInit();

});
