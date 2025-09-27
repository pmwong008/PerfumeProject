const color = localStorage.getItem('chosenColor');
document.querySelectorAll('.card-body').forEach(cb => cb.style.backgroundColor = color);