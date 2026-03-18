class Firework {
    constructor(startX, startY, targetX, targetY, particleCount) {
        this.x = startX;
        this.y = startY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.particleCount = particleCount;
        
        this.hue = Math.random() * 360;
        this.speed = 8;
        this.active = true;
        this.exploded = false;

        const angle = Math.atan2(targetY - startY, targetX - startX);
        this.vx = Math.cos(angle) * this.speed;
        this.vy = Math.sin(angle) * this.speed;
    }

    update() {        
            this.x += this.vx;
            this.y += this.vy;  
    
            const distanceToTarget = Math.hypot(this.targetX - this.x, this.targetY - this.y);
            if (distanceToTarget < this.speed) {
                this.exploded = true;
                this.active = false;
            }
        }   

    draw(ctx) {
        ctx.fillStyle = `hsl(${this.hue}, 100%, 60%)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fill();
    }

}