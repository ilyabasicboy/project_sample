//Import function
import ajaxReset from './feedback';

//Import variable
import {
    getScrollbarWidth
} from './scrollbar-width';

$(function () {

    //Form Modal
    function initDefaultModal() {
        $('.modal-open').each(function() {
            $(this).magnificPopup({
                type: "inline",
                removalDelay: 500,
                mainClass: 'mfp-move mfp-mobile',
                callbacks: {
                    open: function () {
                        $("body").addClass("noscroll");
                        $('.header__burger').addClass('active-modal');
                        $('.header').css('padding-right', getScrollbarWidth() + 'px');
                    },
                    close: function () {
                        if (!$('.header__list').hasClass('open')) {
                            $("body").removeClass("noscroll");
                            $('.header').css('padding-right', '0px');
                        }
                        $('.header__burger').removeClass('active-modal');
                        //Reload Form
                        ajaxReset(this.content.find('[data-reset]'));
                    },
                },
            });
        });
    };
    initDefaultModal();

    //Close modal
	$(document).on('click', '.header__burger', function(event) {
		event.preventDefault();
		if ($('.header__burger').hasClass('active-modal')) {
            $.magnificPopup.close();
		}
	});

    //Init Modal With Load Card
    let target = document.querySelectorAll('.ajax-update');
    target.forEach(element => {
        if (element) {
            let observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    initDefaultModal();
                });
            });
            let config = { childList: true, characterData: true };
            observer.observe(element, config);
        }
    });

    //Gallery Modal
    $('.mfp-gallery').each(function() {
        $(this).magnificPopup({
            type: 'image',
            removalDelay: 500,
            mainClass: 'mfp-fade',
            image: {
                cursor: null,
                tClose: 'Закрыть',
                titleSrc: function(item) {
                    return item.img.attr('alt');
                }
            },
            gallery: {
                enabled: true,
                preload: [0, 2],
                navigateByImgClick: true,
                tPrev: 'Предыдущее фото',
                tNext: 'Следующее фото'
            },
            delegate: 'a[href$=".png"][target!="_blank"], \
                           a[href$=".PNG"][target!="_blank"], \
                           a[href$=".jpeg"][target!="_blank"], \
                           a[href$=".JPEG"][target!="_blank"], \
                           a[href$=".jpg"][target!="_blank"], \
                           a[href$=".JPG"][target!="_blank"]',
            callbacks: {
                buildControls: function() {
                    if (this.items.length > 1) {
                        this.contentContainer.append(this.arrowLeft.add(this.arrowRight));
                    }
                },
                open: function() {
                    $("body").addClass("noscroll");
                    $('.header').css('padding-right', getScrollbarWidth() + 'px');
                },
                close: function() {
                    if (!$('.header__list').hasClass('open')) {
                        $("body").removeClass("noscroll");
                        $('.header').css('padding-right', '0px');
                    }
                }
            },
            closeMarkup: '<button title="Закрыть" type="button" class="mfp-close"></button>',
        });
    });

});