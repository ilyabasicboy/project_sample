import { gsap, ScrollTrigger } from "gsap/all";

$(document).ready(function() {

    //Hidden Preloader
    let tl = new gsap.timeline();
    tl.to('.preloader__logo', {
        duration: 1,
        opacity: 0,
        scale: 0.8,
        ease: 'power4.inOut'
    });
    tl.to('.preloader', {
        duration: 1,
        yPercent: -100,
        ease: 'power4.inOut'
    });
    //Header Animation
    gsap.to('.header__logo', {
        duration: 2,
        opacity: 1,
        delay: 1,
        ease: 'power4.inOut'
    });
    gsap.to('.header__list', {
        duration: 2.2,
        opacity: 1,
        delay: 1,
        ease: 'power4.inOut'
    });
    gsap.to('.header__right', {
        duration: 2.3,
        opacity: 1,
        delay: 1,
        ease: 'power4.inOut'
    });

    //Visible Preloader
    gsap.to('.preloader__logo', {
        duration: 1.2,
        opacity: 1,
        scale: 1,
        ease: 'power4.inOut'
    });
    gsap.to('.preloader__info', {
        duration: 1.3,
        opacity: 1,
        ease: 'power4.inOut'
    });

    function scrollAnim() {
        //Init ScrollTrigger
        gsap.registerPlugin(ScrollTrigger);

        //Img Animation
        let revealContainers = document.querySelectorAll('.img-anim');
        revealContainers.forEach((container) => {
            let image = container.querySelector('img');
            let tl = gsap.timeline({
                scrollTrigger: {
                    trigger: container,
                }
            });
            tl.set(container, {
                autoAlpha: 1
            });
            tl.from(container, 1.5, {
                xPercent: -100,
                ease: 'Power2.out'
            });
            tl.from(image, 1.5, {
                xPercent: 100,
                scale: 1.3,
                delay: -1.5,
                ease: 'Power2.out'
            });
        });

        //BackgroundColor Animation
        let scrollBgElems = document.querySelectorAll('.bg-anim');
        scrollBgElems.forEach((bgSection) => {
            let tl = gsap.timeline({
                scrollTrigger: {
                    trigger: bgSection,
                    start: "top center+=10%",
                }
            });
            tl.to(bgSection, 1.5, {
                backgroundColor: bgSection.dataset.bgcolor,
                ease: 'Power2.out'
            });
        });

        //Text Animation
        let contentAnim = document.querySelectorAll('.content-anim');
        contentAnim.forEach((text) => {
            ScrollTrigger.create({
                trigger: text,
                start: "top center+=40%",
                once: true,
                toggleClass: {targets: text, className: 'is-inview'},
            })
        });
    }

    //Init Content Anim
    setTimeout(() => {
        scrollAnim();
    }, 1850);

    //Init Content Anim With Load Card
    let target = document.querySelector('.product_list_ajax');
    if (target) {
        let observer = new MutationObserver(function(mutations) {
          mutations.forEach(function(mutation) {
            scrollAnim();
          });
        });
        let config = { childList: true, characterData: true };
        observer.observe(target, config);
    }

});