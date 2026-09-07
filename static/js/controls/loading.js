export function createMapLoadingIndicator() {
    const container = document.getElementById("map-loading");
    const image = document.getElementById("map-loading-image");

    let currentProgress = 0;
    let animationFrame = null;

    function applyProgress(value) {
        const fadeWidth = 12;
        const fadeStart = Math.max(value - fadeWidth, 0);

        if (value <= 0) {
            image.style.maskImage =
                "linear-gradient(to right, transparent, transparent)";
            image.style.webkitMaskImage =
                "linear-gradient(to right, transparent, transparent)";
        } else if (value >= 100) {
            image.style.maskImage =
                "linear-gradient(to right, black, black)";
            image.style.webkitMaskImage =
                "linear-gradient(to right, black, black)";
        } else {
            const mask = `
                linear-gradient(
                    to right,
                    black 0%,
                    black ${fadeStart}%,
                    transparent ${value}%,
                    transparent 100%
                )
            `;

            image.style.maskImage = mask;
            image.style.webkitMaskImage = mask;
        }

        const backgroundOpacity =
            0.98 - (value / 100) * 0.68;

        container.style.backgroundColor =
            `rgba(245, 248, 246, ${backgroundOpacity})`;
    }

    function animateProgress(targetProgress) {
        const startProgress = currentProgress;
        const difference = targetProgress - startProgress;

        const duration = 700;
        const startTime = performance.now();

        if (animationFrame !== null) {
            cancelAnimationFrame(animationFrame);
        }

        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const easedProgress =
                progress < 0.5
                    ? 4 * progress ** 3
                    : 1 - Math.pow(-2 * progress + 2, 3) / 2;

            currentProgress =
                startProgress + difference * easedProgress;

            applyProgress(currentProgress);

            if (progress < 1) {
                animationFrame = requestAnimationFrame(animate);
            } else {
                animationFrame = null;
            }
        }

        animationFrame = requestAnimationFrame(animate);
    }

    applyProgress(0);

    return {
        setProgress(value) {
            const targetProgress = Math.min(
                Math.max(value, 0),
                100,
            );

            animateProgress(targetProgress);
        },

        hide() {
            window.setTimeout(() => {
                container.classList.add("hidden");
            }, 500);
        },
    };
}