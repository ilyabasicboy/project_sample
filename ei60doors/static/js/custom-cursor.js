$(document).ready(function () {

    const cursor = document.querySelector('.cursor-custom');
    const cursorCircle = cursor.querySelector('.cursor-custom__circle');

    const mouse = {
        x: -100,
        y: -100
    };
    const pos = {
        x: 0,
        y: 0
    };
    const speed = 0.1;

    const updateCoordinates = e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    }

    window.addEventListener('mousemove', updateCoordinates);

    function getAngle(diffX, diffY) {
        return Math.atan2(diffY, diffX) * 180 / Math.PI;
    }

    function getSqueeze(diffX, diffY) {
        const distance = Math.sqrt(
            Math.pow(diffX, 2) + Math.pow(diffY, 2)
        );
        const maxSqueeze = 0.15;
        const accelerator = 1500;
        return Math.min(distance / accelerator, maxSqueeze);
    }

    const updateCursor = () => {
        const diffX = Math.round(mouse.x - pos.x);
        const diffY = Math.round(mouse.y - pos.y);

        pos.x += diffX * speed;
        pos.y += diffY * speed;

        const angle = getAngle(diffX, diffY);
        const squeeze = getSqueeze(diffX, diffY);

        const scale = 'scale(' + (1 + squeeze) + ', ' + (1 - squeeze) + ')';
        const rotate = 'rotate(' + angle + 'deg)';
        const translate = 'translate3d(' + pos.x + 'px ,' + pos.y + 'px, 0)';

        cursor.style.transform = translate;
        cursorCircle.style.transform = rotate + scale;
    };

    function loop() {
        updateCursor();
        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);

    function cursorChange() {
        const cursorModifiers = document.querySelectorAll('[cursor-class]');
        cursorModifiers.forEach(cursorModifiersItem => {
            cursorModifiersItem.addEventListener('mouseenter', function () {
                const className = this.getAttribute('cursor-class');
                cursor.classList.add(className);
            });

            cursorModifiersItem.addEventListener('mouseleave', function () {
                const className = this.getAttribute('cursor-class');
                cursor.classList.remove(className);
            });
        });
    }
    cursorChange();

    //Reinit Cursor Change With Load Card
    let target = document.querySelectorAll('.ajax-update');
    target.forEach(element => {
        if (element) {
            let observer = new MutationObserver(function(mutations) {
              mutations.forEach(function(mutation) {
                cursorChange();
              });
            });
            let config = { childList: true, characterData: true };
            observer.observe(element, config);
        }
    });

});