// Plant Animations for PlantPal

document.addEventListener('DOMContentLoaded', function() {
    initPlantAnimations();
    initParticleEffects();
});

// Initialize plant animations based on state
function initPlantAnimations() {
    const plants = document.querySelectorAll('.plant-emoji');
    
    plants.forEach(plant => {
        const state = plant.getAttribute('data-state') || 'idle';
        applyPlantAnimation(plant, state);
    });
}

// Apply animation based on plant state
function applyPlantAnimation(element, state) {
    element.style.transition = 'all 0.5s ease';
    
    switch(state) {
        case 'growing':
            growingAnimation(element);
            break;
        case 'calming':
            calmingAnimation(element);
            break;
        case 'idle':
        default:
            idleAnimation(element);
            break;
    }
}

// Growing animation (positive mood)
function growingAnimation(element) {
    let scale = 1;
    let growing = true;
    
    setInterval(() => {
        if (growing) {
            scale += 0.01;
            if (scale >= 1.2) growing = false;
        } else {
            scale -= 0.01;
            if (scale <= 1) growing = true;
        }
        element.style.transform = `scale(${scale}) rotate(${(scale - 1) * 20}deg)`;
    }, 50);
    
    // Add sparkle effect
    createSparkles(element);
}

// Calming animation (negative mood)
function calmingAnimation(element) {
    let rotation = 0;
    
    setInterval(() => {
        rotation = Math.sin(Date.now() / 1000) * 5;
        element.style.transform = `rotate(${rotation}deg)`;
    }, 50);
    
    // Add gentle glow
    element.style.filter = 'drop-shadow(0 0 10px rgba(16, 185, 129, 0.3))';
}

// Idle animation (neutral mood)
function idleAnimation(element) {
    let offset = 0;
    
    setInterval(() => {
        offset = Math.sin(Date.now() / 1000) * 10;
        element.style.transform = `translateY(${offset}px)`;
    }, 50);
}

// Create sparkle particles for growing plants
function createSparkles(element) {
    setInterval(() => {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.cssText = `
            position: absolute;
            width: 5px;
            height: 5px;
            background: radial-gradient(circle, #ffd700, transparent);
            border-radius: 50%;
            pointer-events: none;
            animation: sparkleFloat 1s ease-out forwards;
        `;
        
        const rect = element.getBoundingClientRect();
        sparkle.style.left = `${rect.left + Math.random() * rect.width}px`;
        sparkle.style.top = `${rect.top + Math.random() * rect.height}px`;
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => sparkle.remove(), 1000);
    }, 500);
}

// Initialize particle effects
function initParticleEffects() {
    // Add sparkle animation CSS
    if (!document.querySelector('#sparkleAnimation')) {
        const style = document.createElement('style');
        style.id = 'sparkleAnimation';
        style.textContent = `
            @keyframes sparkleFloat {
                0% {
                    opacity: 1;
                    transform: translateY(0) scale(0);
                }
                50% {
                    opacity: 1;
                    transform: translateY(-30px) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-60px) scale(0);
                }
            }
            
            @keyframes leafFall {
                0% {
                    opacity: 1;
                    transform: translateY(0) rotate(0deg);
                }
                100% {
                    opacity: 0;
                    transform: translateY(100vh) rotate(360deg);
                }
            }
            
            @keyframes petalsFloat {
                0% {
                    opacity: 0;
                    transform: translateY(100vh) rotate(0deg);
                }
                50% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    transform: translateY(-100px) rotate(360deg);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Create floating leaves background effect
function createFloatingLeaves() {
    const leaves = ['🍃', '🌿', '🍀', '🌱'];
    
    setInterval(() => {
        const leaf = document.createElement('div');
        leaf.textContent = leaves[Math.floor(Math.random() * leaves.length)];
        leaf.style.cssText = `
            position: fixed;
            font-size: ${Math.random() * 20 + 20}px;
            left: ${Math.random() * 100}vw;
            top: -50px;
            pointer-events: none;
            z-index: -1;
            animation: leafFall ${Math.random() * 5 + 5}s linear forwards;
        `;
        
        document.body.appendChild(leaf);
        
        setTimeout(() => leaf.remove(), 10000);
    }, 3000);
}

// Create flower petals effect
function createPetalsEffect(element) {
    const petals = ['🌸', '🌺', '🌼', '🌻'];
    
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const petal = document.createElement('div');
            petal.textContent = petals[Math.floor(Math.random() * petals.length)];
            
            const rect = element.getBoundingClientRect();
            petal.style.cssText = `
                position: fixed;
                font-size: 24px;
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top + rect.height / 2}px;
                pointer-events: none;
                z-index: 9999;
                animation: petalsFloat 3s ease-out forwards;
            `;
            
            document.body.appendChild(petal);
            
            setTimeout(() => petal.remove(), 3000);
        }, i * 200);
    }
}

// Celebrate level up with confetti
function celebrateLevelUp() {
    const confettiCount = 50;
    const colors = ['#10b981', '#34d399', '#fbbf24', '#f59e0b', '#ef4444'];
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}vw;
                top: -20px;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                animation: confettiFall ${Math.random() * 2 + 2}s linear forwards;
            `;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 4000);
        }, i * 50);
    }
    
    // Add confetti animation
    if (!document.querySelector('#confettiAnimation')) {
        const style = document.createElement('style');
        style.id = 'confettiAnimation';
        style.textContent = `
            @keyframes confettiFall {
                0% {
                    opacity: 1;
                    transform: translateY(0) rotate(0deg);
                }
                100% {
                    opacity: 0;
                    transform: translateY(100vh) rotate(720deg);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Pulse effect for notifications
function pulseElement(element) {
    element.style.animation = 'pulse 0.5s ease 3';
    
    if (!document.querySelector('#pulseAnimation')) {
        const style = document.createElement('style');
        style.id = 'pulseAnimation';
        style.textContent = `
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Shake effect for errors
function shakeElement(element) {
    element.style.animation = 'shake 0.5s ease';
    
    if (!document.querySelector('#shakeAnimation')) {
        const style = document.createElement('style');
        style.id = 'shakeAnimation';
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
                20%, 40%, 60%, 80% { transform: translateX(10px); }
            }
        `;
        document.head.appendChild(style);
    }
    
    setTimeout(() => {
        element.style.animation = '';
    }, 500);
}

// Export functions for use in other files
window.PlantAnimations = {
    applyPlantAnimation,
    createPetalsEffect,
    celebrateLevelUp,
    pulseElement,
    shakeElement,
    createFloatingLeaves
};

// Start floating leaves on page load
createFloatingLeaves();