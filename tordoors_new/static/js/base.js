$(function () {

    //Fix Transition CSS
    $('body').removeClass('fix-anim');

    //Init Phone Mask
    $(document).on('focus', 'input[name*="phone"]', function() {
        $(this).mask('+7(999)999-99-99');
    });

    //Wrap for Table
    $(".placeholder table").wrap('<div class="table-wrap scroll-custom-x"></div>');

    //Wrap for Iframe
    let placeholderVideo = $('.placeholder iframe');
    placeholderVideo.each(function (index, item) {
        let videoMaxWidth = $(item).attr('width');
        $(item).wrap('<div class="iframe-wrap" style="max-width: ' + videoMaxWidth + 'px;"></div>');
    });

    //Add preview for Video
    $(".video-custom").each(function() {
        let vimeoId = $(this).data("bg-video");
        $.getJSON('https://vimeo.com/api/oembed.json?url=https%3A//vimeo.com/' + vimeoId, {
            format: "json",
            width: "640"
        },
        function(data) {
            $(".video-custom[data-bg-video=" + vimeoId + "]").css('background-image', 'url(' + data.thumbnail_url + ')');
        });
    });

	//Mobile Menu
	$(".header__burger").on("click", function(event) {
		event.preventDefault();
		$(this).toggleClass("active");
		$('.header__list').toggleClass('active');
		$('.header__list').addClass('anim--active');
		$("body").toggleClass("noscroll");
	});

	//Mobile Big Menu Toggle
	$('.header__menu-mobleicon').on('click', function() {
	    $(this).toggleClass('active');
        $(this).parent().find('.header__submenu-bg').slideToggle(550);
	});

    //Big Menu Hover
    const menuItem = $('.menu-level-2');
    menuItem.on('click', function() {
        if (!$(this).hasClass('active')) {
            $(menuItem).removeClass('active');
            $(this).addClass('active');
            let menuTarget = $(this).data('menu');
            $("[data-target]").removeClass('open');
            $("[data-target='" + menuTarget + "']").addClass('open');
        }
    });

    //Mobile Open/Close Filter Price
    $(".filter__open").on("click", function() {
        $('.filter__left').addClass('open');
    });
    $(".filter__close").on("click", function() {
        $('.filter__left').removeClass('open');
    });

    //Go Top
    $(window).scroll(function () {
        let scrollTop = $(this).scrollTop();
        let documentHeight = $(document).outerHeight();
        if (scrollTop < documentHeight / 1.5) {
            $(".btn__up").fadeOut(300);
        } else {
            $(".btn__up").fadeIn(300);
        }
    });
    $(".btn__up").click(function () {
        $("html, body").animate({ scrollTop: 0 }, 1000);
    });

    //Slide Toggle
    let headerHeight = $('.header').height();
    $(document).on('click', '._slide', function(e){
        e.preventDefault();
        if ($(this).hasClass('_slide-parent')) {
            $(this).parent().next('._slide-target').slideToggle(550);
            $(this).parent().toggleClass('active');
        } else {
            $(this).next('._slide-target').slideToggle(550, function(){
                if ($(this).prev().attr("href")) {
                    let elementClick = $(this).prev().attr("href");
                    let destination = $(elementClick).offset().top - headerHeight;
                    $('html, body').animate( { scrollTop: destination }, 1000);
                }
            });
            $(this).toggleClass('active');
        }
    });

    //Anchor Link
    $('.anchor-link').click(function (e) {
        e.preventDefault();
        let anchorMargin = 0;
        if ($(this).hasClass('anchor-link-m20')) {
            anchorMargin = 20;
        }
        let elementClick = $(this).attr("href");
        let destination = $(elementClick).offset().top - headerHeight - anchorMargin;
        $('html, body').animate( { scrollTop: destination }, 1500, 'swing');
    });
    $(".anchor-link-next").on('click', function() {
        let parent = $(this).parent().outerHeight();
        $("body,html").animate({ scrollTop: parent }, 1500, 'swing');
    });

    //Check focus Search
    $(document).on('focus', '.search-form input', function () {
        $('.search-form').addClass('active');
    });
    $(document).on('blur', '.search-form input', function () {
        if( !$(this).val() ) {
            $('.search-form').removeClass('active');
        }
    });

    //Check focus Search Result
    $(document).on('focus', '.search-result input', function () {
        $('.search-result').addClass('active');
    });
    $(document).on('blur', '.search-result input', function () {
        if( !$(this).val() ) {
            $('.search-result').removeClass('active');
        }
    });

    //Init Slidable
    function slidableReviewInit() {
        if ($(window).width() < 768) {
            $(".review__item-wrapper").slidable({
                minimal: 105,
                controls: ['<span>Читать далее</span>', '<span>Скрыть</span>'],
            });
        } else {
            $(".review__item-wrapper .tall").each(function() {
                var height = $(this).data("height");
                if (height) {
                    $(this).css({"height": ""});
                    $(this).removeData("height")
                }
            });
            $(".review__item-wrapper .controller").remove();
        }
    }
    $(window).resize(slidableReviewInit);
    slidableReviewInit();

    //Fixed Button Faq
    if ($('.faq__sticky').length > 0) {
        $(window).scroll(function () {
            let position = $('.faq__theme').offset().top + $('.faq__theme').height();
            let scroll = $(document).scrollTop();
            if (scroll > position && $(window).width() < 768) {
                $('.faq__sticky').addClass('fixed');
            } else {
                $('.faq__sticky').removeClass('fixed');
            }
        });
    }

    //Fixed Panel Filter
    if ($('.filter__panel-sticky').length > 0) {
        $(window).scroll(function () {
            let position = $('.filter__panel').offset().top + $('.filter__panel').height();
            let scroll = $(document).scrollTop();
            if (scroll > position && $(window).width() < 768) {
                $('.filter__panel-sticky').addClass('fixed');
            } else {
                $('.filter__panel-sticky').removeClass('fixed');
            }
        });
    }

    //Fixed Panel Product
    if ($('.product__sidebar-footer--sticky').length > 0) {
        $(window).scroll(function () {
            let position = $('.product__sidebar-bottom').offset().top + $('.product__sidebar-bottom').height();
            let scroll = $(document).scrollTop();
            if (scroll > position && $(window).width() < 768) {
                $('.product__sidebar-footer--sticky').addClass('fixed');
            } else {
                $('.product__sidebar-footer--sticky').removeClass('fixed');
            }
        });
    }

    //Product View Change with Color
    let colorTarget;
    $(document).on('click', '.product-change-color', function() {
        colorTarget = $(this).data('product-color');
        let colorTargetTitle = $(this).data('product-color-title');
        if (!$(this).hasClass('active')) {
            $('.product-change-color').removeClass('active');
            $(this).addClass('active');

            //Change Img Preview
            $(".product__view-img").find('.product-change-img').fadeOut(600);
            let imgPreviewTarget = $(".product__view-img").find('.product-change-img[data-product-color="'+ colorTarget +'"]');
            imgPreviewTarget.fadeIn(600);

            //Change Img Interior
            $(".product__interior-preview").find('.product__interior-preview__img').fadeOut(600);
            $(".product__interior-preview").find('.product__interior-preview__img[data-product-color="'+ colorTarget +'"]').fadeIn(600);
            $('.view-color__title span').text(colorTargetTitle);

            //Change Drawing Title
            imgPreviewTarget.each(function(index, item) {
                let drawingTargetTitle = $(item).data('product-drawing-title');
                if($(item).parent().parent().hasClass('view-dimensions')) {
                    $(item).parent().parent().parent().find('.product__view-drawing span').text(drawingTargetTitle);
                } else {
                    $(item).parent().parent().find('.product__view-drawing span').text(drawingTargetTitle);
                }
            });
        }
    });
    $('.product-change-color-list').find('.product-change-color').each(function() {
        if ($(this).hasClass('active')) {
            colorTarget = $(this).data('product-color');
        }
    });

    //Change Product Img with Swipe
    function productCardChangeSwipe() {
        let swipeImg = $('.product-card__img-item');
        swipeImg.each(function (index, item) {
            $(item).swipe({
                left: function() {
                    if ($(item).next('.product-card__img-item').length > 0) {
                        let productTargetColor = $(item).next().data('card');

                        $(item).fadeOut(600).removeClass('active');
                        $(item).next().fadeIn(600).addClass('active');

                        $(item).parent().parent().find('.product-card__color-item').removeClass('active');
                        $(item).parent().parent().find('.product-card__color-item[data-target-card="'+ productTargetColor +'"]').addClass('active');
                    } else {
                        $(item).fadeOut(600).removeClass('active');
                        $(item).parent().find('.product-card__img-item').first().fadeIn(600).addClass('active');

                        $(item).parent().parent().find('.product-card__color-item').removeClass('active');
                        $(item).parent().parent().find('.product-card__color-item').first().addClass('active');
                    }
                },
                right: function() {
                    if ($(item).prev('.product-card__img-item').length > 0) {
                        let productTargetColor = $(item).prev().data('card');

                        $(item).fadeOut(600).removeClass('active');
                        $(item).prev().fadeIn(600).addClass('active');

                        $(item).parent().parent().find('.product-card__color-item').removeClass('active');
                        $(item).parent().parent().find('.product-card__color-item[data-target-card="'+ productTargetColor +'"]').addClass('active');
                    } else {
                        $(item).fadeOut(600).removeClass('active');
                        $(item).parent().find('.product-card__img-item').last().fadeIn(600).addClass('active');

                        $(item).parent().parent().find('.product-card__color-item').removeClass('active');
                        $(item).parent().parent().find('.product-card__color-item').last().addClass('active');
                    }
                },
                threshold: {
                    x: 30,
                    y: 2000
                }
            });
        });
    }
    productCardChangeSwipe();

    //Change Product Img with Color
    function productCardChangeClick() {
        let productCard = $('.product-card');
        productCard.each(function (index, item) {
            $(item).find('.product-card__color-item').on('click mouseover', function() {
                if (!$(this).hasClass('active')) {
                    let productTargetImg = $(this).data('target-card');

                    $(this).parent().find('.product-card__color-item').removeClass('active');
                    $(this).addClass('active');

                    $(this).parent().parent().find(".product-card__img-item").fadeOut(600).removeClass('active');
                    $(this).parent().parent().find('.product-card__img-item[data-card="'+ productTargetImg +'"]').fadeIn(600).addClass('active');
                }
            });
        });
    }
    productCardChangeClick();

    //Init Change Product Img With Load Card
    let target = document.querySelector('.product_list_ajax');
    if (target) {
        let observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                productCardChangeClick();
                productCardChangeSwipe();
            });
        });
        let config = { childList: true, characterData: true };
        observer.observe(target, config);
    }

    //Change background Interior
    $('.product__interior-option__item').on('click', function(){
        let targetBg = $(this).data('target-bg');
        if (!$(this).hasClass('active')) {
            $('.product__interior-option__item').removeClass('active');
            $(this).addClass('active');
            $(".product__interior-item").removeClass('active');
            $('.product__interior-item[data-bg="'+ targetBg +'"]').addClass('active');
        }
    });

    //Tooltip Open/Close
    $('.tooltip__btn').on('click', function(){
        $(this).next().toggleClass('open');
    });
    $('.tooltip__close').on('click', function(){
        $(this).parent().removeClass('open');
    });

    //Add Base Equipment Title in List
    let baseEquipment = '';
    function baseEquipmentTitle() {
        $('.product__option-base-js').each(function() {
            if (baseEquipment == '') {
                baseEquipment = $(this).text().trim();
            }
            else {
                baseEquipment = baseEquipment + ', ' + $(this).text().trim();
            }
        });
    }
    baseEquipmentTitle();

    //Add Additional Title in List
    let additional = '';
    function additionalTitle() {
        additional = '';
        $('.price-change-js').each(function() {
            if ($(this).is(':checked')) {
                additional = additional + $(this).val().trim() + ', ';
            };
        });
    }
    additionalTitle();

    //Init Text Order Form
    function orderFormText() {
        let title = '';
        if ($('.product__sidebar-title').length) {
            title = $('.product__sidebar-title').text().trim() + ', ';
        };

        let size = '';
        if ($('.product__size').length) {
            size = 'Размер коробки: ' + $('.product__size').text().trim() + ', ';
        };

        let viewColor = '';
        if ($('.view-color__text').length) {
            viewColor = $('.view-color__text').text().trim() + ', ';
        };

        let baseEquipmentText = '';
        if (baseEquipment == '') {
            baseEquipmentText = ''
        } else {
            baseEquipmentText = 'Комплектация: ' + baseEquipment + ', ';
        }

        let additionalText = '';
        if (additional == '') {
            additionalText = ''
        } else {
            additionalText = 'Дополнительно: ' + additional;
        }

        let term = '';
        if ($('.product__term').length) {
            term = ' Срок изготовления: ' + $('.product__term').text().trim();
        };

        let price = '';
        if ($('.product__price').length) {
            price = ', Примерная стоимость: ' + $('.product__price-info').text().trim();
        };

        let form_text = title + size + viewColor + baseEquipmentText + additionalText + term + price;
        $('.order-text-js').html(form_text);
        $('#id_order-popup_text').val(form_text.replace(/\s{2,}/g, ' '));
    }
    $('.order-text-init-js').on('click', function() {
        orderFormText();
    });

    //Init Text Order Form
    function updatePriceProduct() {
        var price = $(('.product__price')).attr('data-original-price');
        $('.price-change-js').each(function() {
            if ($(this).is(':checked') && parseInt($(this).attr('data-price-change'))) {
                price = parseInt(price) + parseInt($(this).attr('data-price-change'));
            };
        });
        const productPrice = $('.product__price span');
        productPrice.html(parseInt(price));
        productPrice.text(productPrice.text().toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    }
    $(document).on('change', '.price-change-js', function() {
        updatePriceProduct();
        additionalTitle();
    });

});