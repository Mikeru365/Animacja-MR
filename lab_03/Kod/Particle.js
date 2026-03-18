class Particle {
   constructor(x,y,hue) {
    this.x = x;
    this.y = y;
    
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 6 + 1;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed;

    this.alpha = 1;
    this.hue = hue;
    this.decay = Math.random() * 0.015 + 0.005;
    this.active = true;
   }

   update(gravity, canvasHeight) {
    this.vx *= 0.98; 
    this.vy *= 0.98;
    this.vy += gravity; 

    this.x += this.vx;
    this.y += this.vy;
    this.alpha -= this.decay; 

    if (this.y >= canvasHeight) {
        const overflow = this.y - canvasHeight;
        this.y = canvasHeight - overflow;
        this.vy *= -0.6; 
    }
 
    if (this.alpha <= 0) this.active = false;
   }

   draw(ctx) {
    ctx.fillStyle = `hsla(${this.hue}, 100%, 50%, ${this.alpha})`;
    ctx.beginPath();
    ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
    ctx.fill();
   }
}