import { Hand } from './Hand.js'; 

export class Clock {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.isPaused = false;

        this.hourHand = new Hand(100, 8, '#2c3e50');
        this.minuteHand = new Hand(150, 5, '#34495e');
        this.secondHand = new Hand(180, 2, '#e74c3c');
    }

    drawFace() {
        const ctx = this.ctx;
        ctx.save(); // Zapisujemy stan przed rysowaniem tarczy
        ctx.strokeStyle = '#2c3e50';
        
        for (let i = 0; i < 60; i++) {
            const isHour = i % 5 === 0;
            ctx.lineWidth = isHour ? 4 : 1;
            
            ctx.beginPath();
            ctx.moveTo(0, -210);
            ctx.lineTo(0, isHour ? -230 : -220);
            ctx.stroke();
            
            ctx.rotate(Math.PI / 30); // Obrót o 6 stopni (360/60)
        }
        ctx.restore(); // Przywracamy stan po narysowaniu tarczy
    }

    update() {
        if (this.isPaused) return;

        const now = new Date();
        const ms = now.getMilliseconds();
        const sec = now.getSeconds() + ms / 1000;
        const min = now.getMinutes() + sec / 60;
        const hr = (now.getHours() % 12) + min / 60;

        // Czyszczenie tła
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save();
        this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);

        this.drawFace();

        // Rysowanie wskazówek
        this.hourHand.draw(this.ctx, (hr / 12) * 2 * Math.PI);
        this.minuteHand.draw(this.ctx, (min / 60) * 2 * Math.PI);
        this.secondHand.draw(this.ctx, (sec / 60) * 2 * Math.PI);

        this.ctx.restore();
    }

    togglePause() {
        this.isPaused = !this.isPaused;
    }
}