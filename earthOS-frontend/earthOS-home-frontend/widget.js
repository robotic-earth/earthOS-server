// widget.js — preserves original animation, saves only id/size/index

// Utility: generate unique ID
function generateID() {
    return 'widget-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
}

// Resize with clone + blur animation (matches original)
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

    // Create clone and blur it (same as your original)
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

        // Persist state after resize (saves id/size/index)
        saveWidgets();
    }, 300);
}

// Add button behavior — keep your original animation flow
const addButton = document.querySelector('.add-widget-btn');
const grid = document.getElementById('home-grid');

if (addButton && grid) {
    addButton.addEventListener('click', () => {
        const newWidget = document.createElement('div');
        newWidget.classList.add('widget', 'medium');
        newWidget.dataset.id = generateID();

        // append to grid (no absolute positioning)
        grid.appendChild(newWidget);
        newWidget.style.visibility = 'hidden';

        // Create clone and blur it (use DOM rect for animation)
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
            clone.classList.add('active');
            clone.style.transform = 'scale(1, 1)'; // placeholder
        });

        setTimeout(() => {
            clone.classList.remove('active');
            clone.remove();
            newWidget.style.visibility = 'visible';

            // Persist after adding
            saveWidgets();
        }, 300);

        newWidget.addEventListener('click', () => {
            resizeWidget(newWidget);
        });
    });
}

// Save only id, size, index (index = order inside grid)
async function saveWidgets() {
    const widgets = Array.from(document.querySelectorAll('.widget')).map((widget, idx) => {
        return {
            id: widget.dataset.id || generateID(),
            size: widget.classList.contains('small') ? 'small'
                  : widget.classList.contains('medium') ? 'medium'
                  : 'large',
            index: idx
        };
    });

    try {
        await fetch('/os/save-widgets', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({widgets})
        });
    } catch (err) {
        console.error('Failed to save widgets:', err);
    }
}

// Load: reconstruct DOM order, do NOT set absolute positions (let CSS grid do layout)
async function loadWidgets() {
    try {
        const res = await fetch('/os/load-widgets');
        if (!res.ok) return;
        const data = await res.json();
        const widgetsData = Array.isArray(data.widgets) ? data.widgets : (data.widgets || []);
        const grid = document.getElementById('home-grid');
        grid.innerHTML = '';

        // sort by index to ensure correct DOM order
        widgetsData.sort((a, b) => (a.index || 0) - (b.index || 0));

        widgetsData.forEach(wd => {
            const widget = document.createElement('div');
            widget.classList.add('widget', wd.size || 'medium');
            widget.dataset.id = wd.id || generateID();
            grid.appendChild(widget);

            widget.addEventListener('click', () => resizeWidget(widget));
        });
    } catch (err) {
        console.error('Failed to load widgets:', err);
    }
}

// init
window.addEventListener('DOMContentLoaded', loadWidgets);
