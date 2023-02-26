import { gsap, ScrollTrigger } from "gsap/all";

$(document).ready(function() {

    function scrollAnim() {
        //Init ScrollTrigger
        gsap.registerPlugin(ScrollTrigger);

        //Content Animation
        let contentAnim = document.querySelectorAll('.content-anim');
        contentAnim.forEach((text) => {
            ScrollTrigger.create({
                trigger: text,
                start: "top center+=40%",
                once: true,
                toggleClass: {targets: text, className: 'is-inview'},
            })
        });

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
                scale: 1.05,
                delay: -1.5,
                ease: 'Power2.out'
            });
        });
    };

    scrollAnim();

});