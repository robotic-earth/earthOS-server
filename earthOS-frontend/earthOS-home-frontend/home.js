document.addEventListener('DOMContentLoaded', function() {
  const grid = document.getElementById('home-grid');
  const navButtons = document.querySelectorAll('.nav-btn');

  navButtons.forEach(button => {
    button.addEventListener('click', function(event) {
      const targetPage = event.currentTarget.getAttribute('data-page');

      // Toggle active button style
      navButtons.forEach(btn => btn.classList.remove('is-active'));
      event.currentTarget.classList.add('is-active');

      if (targetPage === 'home') {
        grid.classList.remove('hidden'); // fade in
      } else if (targetPage === 'settings') {
        grid.classList.add('hidden'); // fade out
      }
    });
  });
});