// Function to resize a widget with blur on the animating widget
function resizeWidget(widget) {
    const currentSize = widget.classList.contains('small') ? 'small'
                        : widget.classList.contains('medium') ? 'medium'
                        : 'large';

    const nextSize = currentSize === 'small' ? 'medium'
                    : currentSize === 'medium' ? 'large'
                    : 'small';

    const originalRect = widget.getBoundingClientRect();

    // Calculate target size without blurring other widgets
    widget.classList.add(nextSize);
    const targetRect = widget.getBoundingClientRect();
    widget.classList.remove(nextSize);

    const scaleX = targetRect.width / originalRect.width;
    const scaleY = targetRect.height / originalRect.height;
    const deltaX = targetRect.left - originalRect.left;
    const deltaY = targetRect.top - originalRect.top;

    // Create clone and blur it
    const clone = widget.cloneNode(true);
    clone.classList.add('widget-transitioning', 'blurred'); // Add blurred class to clone
    clone.style.position = 'absolute';
    clone.style.top = `${originalRect.top}px`;
    clone.style.left = `${originalRect.left}px`;
    clone.style.width = `${originalRect.width}px`;
    clone.style.height = `${originalRect.height}px`;
    clone.style.zIndex = 1000;
    clone.style.pointerEvents = 'none';
    clone.style.transition = 'all 0.3s ease-in-out';
    clone.style.transform = 'translate(0px, 0px) scale(1, 1)';
    clone.style.transformOrigin = 'top left';

    widget.style.visibility = 'hidden';
    document.body.appendChild(clone);

    requestAnimationFrame(() => {
        clone.classList.add('active');
        clone.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(${scaleX}, ${scaleY})`;
    });

    setTimeout(() => {
        clone.classList.remove('active');
        clone.remove();
        widget.classList.remove(currentSize);
        widget.classList.add(nextSize);
        widget.style.visibility = 'visible';
    }, 300);
}

// Event listener for adding a new widget with blur on the animating widget
const addButton = document.querySelector('.add-widget-btn');
const grid = document.getElementById('home-grid');

if (addButton && grid) {
    addButton.addEventListener('click', () => {
        const newWidget = document.createElement('div');
        newWidget.classList.add('widget', 'medium');

        grid.appendChild(newWidget);
        newWidget.style.visibility = 'hidden';

        // Create clone and blur it
        const clone = newWidget.cloneNode(true);
        clone.classList.add('widget-transitioning', 'blurred'); // Add blurred class to clone
        clone.style.position = 'absolute';
        const originalRect = newWidget.getBoundingClientRect();
        clone.style.top = `${originalRect.top}px`;
        clone.style.left = `${originalRect.left}px`;
        clone.style.width = `${originalRect.width}px`;
        clone.style.height = `${originalRect.height}px`;
        clone.style.zIndex = 1000;
        clone.style.pointerEvents = 'none';
        clone.style.transition = 'all 0.3s ease-in-out';
        clone.style.transform = 'translate(0px, 0px) scale(1, 1)';
        clone.style.transformOrigin = 'top left';
        document.body.appendChild(clone);

        requestAnimationFrame(() => {
            clone.classList.add('active    active');
            clone.style.transform = 'scale(1, 1)'; // Placeholder animation
        });

        setTimeout(() => {
            clone.classList.remove('active');
            clone.remove();
            newWidget.style.visibility = 'visible';
        }, 300);

        newWidget.addEventListener('click', () => {
            resizeWidget(newWidget);
        });
    });
}