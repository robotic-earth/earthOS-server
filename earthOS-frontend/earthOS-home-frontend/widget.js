document.querySelectorAll('.widget').forEach(widget => {
    widget.addEventListener('click', () => {
        if (widget.classList.contains('small')){
            widget.classList.remove('small');
            widget.classList.add('medium')
        }
        else if (widget.classList.contains('medium')){
            widget.classList.remove('medium');
            widget.classList.add('large');
        }
        else {
            widget.classList.remove('large');
            widget.classList.add('small');
        }
    })
})


const addButton = document.querySelector('.add-widget-btn');
const grid = document.getElementById('home-grid');

if (addButton && grid) {
    addButton.addEventListener('click', () => {
        const newWidget = document.createElement('div');
        newWidget.classList.add('widget', 'medium');
        
        // Add the same click-to-resize behavior as the other widgets
        newWidget.addEventListener('click', () => {
            if (newWidget.classList.contains('small')){
                newWidget.classList.remove('small');
                newWidget.classList.add('medium');
            }
            else if (newWidget.classList.contains('medium')){
                newWidget.classList.remove('medium');
                newWidget.classList.add('large');
            }
            else {
                newWidget.classList.remove('large');
                newWidget.classList.add('small');
            }
        });

        grid.appendChild(newWidget);
    });
}

