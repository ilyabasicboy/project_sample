//Import Function
import ajaxReset from './feedback';

$(function () {

    //Form Modal
    function initDefaultModal() {
        $('.modal-open').each(function() {
            $(this).magnificPopup({
                type: "inline",
                removalDelay: 500,
                mainClass: 'mfp-move',
                callbacks: {
                    open: function () {
                        $("body").addClass("noscroll");
                    },
                    close: function () {
                        $("body").removeClass("noscroll");
                        //Reload Form
                        ajaxReset();
                    },
                },
            });
        });
    }
    initDefaultModal();

    //Close Modal With Scroll
    $(document).on('click', '.close-modal', function(){
        $.magnificPopup.close();
        $("html, body").animate({ scrollTop: 0 }, 1000);
    });

    //Close Modal
    $(document).on('click', '.close-modal-noscroll', function(){
        $.magnificPopup.close();
    });

    //Init Content Anim With Load Card
    let target = document.querySelector('.product_list_ajax');
    if (target) {
        let observer = new MutationObserver(function(mutations) {
          mutations.forEach(function(mutation) {
            initDefaultModal();
          });
        });
        let config = { childList: true, characterData: true };
        observer.observe(target, config);
    }

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
                },
                close: function() {
                    $("body").removeClass("noscroll");
                }
            },
            closeMarkup: '<button title="Закрыть" type="button" class="mfp-close"></button>',
        });
    });

    //Video Modal
    $('.modal-video').each(function() {
        $(this).magnificPopup({
            type: 'iframe',
            removalDelay: 500,
            mainClass: 'mfp-move',
            iframe: {
                markup: '<div class="mfp-iframe-scaler">'+
                        '<div class="mfp-close"></div>'+
                        '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>'+
                        '</div>',
                patterns: {
                        vimeo: {
                            index: 'vimeo.com/',
                            id: '/',
                            src: '//player.vimeo.com/video/%id%?autoplay=1'
                        },
                },
                srcAction: 'iframe_src',
            },
            callbacks: {
                beforeOpen: function() {
                    this.st.iframe.markup = this.st.iframe.markup.replace('mfp-iframe-scaler', 'mfp-iframe-scaler mfp-anim');
                },
                open: function() {
                    $("body").addClass("noscroll");
                },
                close: function() {
                    $("body").removeClass("noscroll");
                }
            },
        });
    });

});

