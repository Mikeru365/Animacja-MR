class FireworkShow {
   constructor() {
    this.canvas = document.getElementById('fireworkCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.resize();
    window.addEventListener('resize', () => this.resize());

    this.rockets = [];
    this.particles = [];
    this.gravity = 0.2;
    this.particleCount = 100;

    this.autoFireTimer = 0;
    this.fireInterval = 90;

    document.getElementById('gravityRange').addEventListener('input', (e) => {
        this.gravity = parseFloat(e.target.value);
    });
    document.getElementById('particleRange').addEventListener('input', (e) => {
        this.particleCount = parseInt(e.target.value);
    });

    this.canvas.addEventListener('click', (e) => {
        const startx= this.canvas.width / 2;
        const starty = this.canvas.height;
        const targetx = e.clientX;
        const targety = e.clientY;
        const rocket = new Firework(startx, starty, targetx, targety, this.particleCount);
        this.rockets.push(rocket);
    });
    
    this.update();
   }

   resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    update() {
        this.autoFireTimer++;
        if (this.autoFireTimer >= this.fireInterval) {
            const startX = Math.random() * this.canvas.width; 
            const targetX = Math.random() * this.canvas.width;
            const targetY = Math.random() * (this.canvas.height / 2); 
            
            const rocket = new Firework(startX, this.canvas.height, targetX, targetY, this.particleCount);
            this.rockets.push(rocket);
            
            this.autoFireTimer = 0; 
        }

        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.rockets.forEach(rocket => {
          rocket.update();
          rocket.draw(this.ctx);

          if (rocket.exploded) {
            for (let i = 0; i < rocket.particleCount; i++) {
              const particle = new Particle(rocket.x, rocket.y, rocket.hue);
              this.particles.push(particle);
            }
          rocket.exploded = false;
        }

        });

        this.particles.forEach(particle => {
            particle.update(this.gravity, this.canvas.height);
            particle.draw(this.ctx);
        });

        this.rockets = this.rockets.filter(r => r.active);
        this.particles = this.particles.filter(p => p.active);

        requestAnimationFrame(() => this.update());
    }
    
}

const show = new FireworkShow();