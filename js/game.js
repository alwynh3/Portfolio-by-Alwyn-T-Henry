const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('scoreValue');
const startScreen = document.getElementById('startScreen');
const gameOverScreen = document.getElementById('gameOverScreen');
const finalScoreElement = document.getElementById('finalScore');

// Game State
let gameRunning = false;
let score = 0;
let frames = 0;
let gameSpeed = 3;

// Resize canvas
function resizeCanvas() {
    const container = document.querySelector('.game-container');
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Player (Dot)
const player = {
    x: 50,
    y: 150,
    radius: 8,
    velocity: 0,
    gravity: 0.25,
    jumpStrength: -5.5,
    color: '#00f0ff',

    draw: function () {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.closePath();
        ctx.shadowBlur = 0;
    },

    update: function () {
        this.velocity += this.gravity;
        this.y += this.velocity;

        // Floor collision
        if (this.y + this.radius > canvas.height) {
            this.y = canvas.height - this.radius;
            gameOver();
        }

        // Ceiling collision
        if (this.y - this.radius < 0) {
            this.y = this.radius;
            this.velocity = 0;
        }
    },

    jump: function () {
        this.velocity = this.jumpStrength;
    },

    reset: function () {
        this.y = canvas.height / 2;
        this.velocity = 0;
    }
};

// Obstacles (Buildings)
const obstacles = [];
const obstacleWidth = 50;
const obstacleGap = 150;
const obstacleFrequency = 120; // Frames between obstacles

class Obstacle {
    constructor() {
        this.x = canvas.width;
        this.width = obstacleWidth;
        this.topHeight = Math.random() * (canvas.height - obstacleGap - 100) + 50;
        this.bottomY = this.topHeight + obstacleGap;
        this.bottomHeight = canvas.height - this.bottomY;
        this.passed = false;
    }

    draw() {
        ctx.fillStyle = '#222';
        ctx.strokeStyle = '#00f0ff';
        ctx.lineWidth = 1;

        // Top Building
        ctx.fillRect(this.x, 0, this.width, this.topHeight);
        ctx.strokeRect(this.x, 0, this.width, this.topHeight);

        // Bottom Building
        ctx.fillRect(this.x, this.bottomY, this.width, this.bottomHeight);
        ctx.strokeRect(this.x, this.bottomY, this.width, this.bottomHeight);

        // Windows (Visual flair)
        ctx.fillStyle = '#333';
        for (let i = 10; i < this.topHeight - 10; i += 20) {
            if (Math.random() > 0.5) ctx.fillRect(this.x + 10, i, 10, 10);
            if (Math.random() > 0.5) ctx.fillRect(this.x + 30, i, 10, 10);
        }
        for (let i = this.bottomY + 10; i < canvas.height - 10; i += 20) {
            if (Math.random() > 0.5) ctx.fillRect(this.x + 10, i, 10, 10);
            if (Math.random() > 0.5) ctx.fillRect(this.x + 30, i, 10, 10);
        }
    }

    update() {
        this.x -= gameSpeed;

        // Collision Detection
        // Top pipe
        if (player.x + player.radius > this.x &&
            player.x - player.radius < this.x + this.width &&
            player.y - player.radius < this.topHeight) {
            gameOver();
        }

        // Bottom pipe
        if (player.x + player.radius > this.x &&
            player.x - player.radius < this.x + this.width &&
            player.y + player.radius > this.bottomY) {
            gameOver();
        }

        // Score update
        if (this.x + this.width < player.x && !this.passed) {
            score++;
            scoreElement.innerText = score;
            this.passed = true;

            // Speed up
            gameSpeed += 0.5;
        }
    }
}

function gameOver() {
    gameRunning = false;
    finalScoreElement.innerText = score;
    gameOverScreen.style.display = 'flex';
}

function resetGame() {
    player.reset();
    obstacles.length = 0;
    score = 0;
    frames = 0;
    gameSpeed = 3;
    scoreElement.innerText = score;
    gameRunning = true;
    startScreen.style.display = 'none';
    gameOverScreen.style.display = 'none';
    animate();
}

function animate() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 50) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 50) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }

    player.update();
    player.draw();

    if (frames % obstacleFrequency === 0) {
        obstacles.push(new Obstacle());
    }

    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].update();
        obstacles[i].draw();

        if (obstacles[i].x + obstacles[i].width < 0) {
            obstacles.shift();
            i--;
        }
    }

    frames++;
    requestAnimationFrame(animate);
}

// Input handling
window.addEventListener('keydown', function (e) {
    if (e.code === 'Space') {
        e.preventDefault(); // Prevent scrolling
        if (gameRunning) {
            player.jump();
        } else if (startScreen.style.display !== 'none' || gameOverScreen.style.display !== 'none') {
            resetGame();
        }
    }
});

canvas.addEventListener('mousedown', function (e) {
    if (gameRunning) {
        player.jump();
    } else {
        resetGame();
    }
});

// Initial Draw
resizeCanvas();
ctx.fillStyle = '#00f0ff';
ctx.font = '20px monospace';
ctx.fillText('Press Space to Start', canvas.width / 2 - 100, canvas.height / 2);
