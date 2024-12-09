function animateCounters() {
    const counters = document.querySelectorAll(".counter");

    counters.forEach((counter, index) => {
        const target = parseInt(counter.getAttribute("data-target"));
        const duration = 100000; // Duration for the animation in milliseconds
        const step = Math.ceil(target / duration * 50); // Step increment per frame
        let current = 0;

        const updateCounter = () => {
            current += step;
            if (current <= target) {
                counter.innerText = current;
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };

        // Delay each counter by 3 seconds initially, then start the animation after 1 second
        setTimeout(() => {
            setTimeout(() => {
                updateCounter();
            }, index * 100); // Delay each counter by 1 second
        }, 1000); // Initial delay of 3 seconds before animation starts
    });
}

animateCounters();
