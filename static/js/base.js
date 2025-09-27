//search
document.querySelector('#searchForm1 .search-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('searchForm1').submit();
    }
});

//change color
const logo = document.getElementById('logo');
const colorPanel = document.getElementById('colorPanel');
const header = document.querySelector('header');
const footer = document.querySelector('footer');

logo.addEventListener('click', () => {
  if(colorPanel.style.left === '0px'){
    colorPanel.style.left = '-200px';
  } else {
    colorPanel.style.left = '0px';
  }
});

document.addEventListener('DOMContentLoaded', function() {
  const color = localStorage.getItem('chosenColor');
  if (color) {
    header.style.backgroundColor = color;
    footer.style.backgroundColor = color;

  }
});

document.querySelectorAll('.color-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    localStorage.setItem('chosenColor', e.target.style.backgroundColor);
    location.reload();
  });
});

document.querySelector('.default-btn').addEventListener('click', () => {
    localStorage.removeItem('chosenColor');
    location.reload();
});

//logout
document.addEventListener('click', function(e) {
    if (e.target.matches('.dropdown-item.btn-logout') ||
        e.target.closest('.dropdown-item.btn-logout')) {
        e.preventDefault();
        document.getElementById('logoutForm').submit();
    }
});
