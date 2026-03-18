export class Hand {
    constructor(length, width, color) {
        this.length = length;
        this.width = width;
        this.color = color;
    }

    draw(ctx, angle) {
        ctx.save(); // Zapisanie stanu przed rotacją
        
        ctx.rotate(angle); 
        ctx.beginPath();
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.width;
        ctx.lineCap = "round"; 
        
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -this.length); 
        ctx.stroke();
        
        // Kółeczko dekoracyjne
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();

        ctx.restore();
    }
}