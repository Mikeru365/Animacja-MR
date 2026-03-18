import { Clock } from './Clock.js';

const clock = new Clock('clockCanvas');

function animate() {
    clock.update();
    requestAnimationFrame(animate); // Wywołanie kolejnej klatki
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        clock.togglePause();
    }});

animate();
