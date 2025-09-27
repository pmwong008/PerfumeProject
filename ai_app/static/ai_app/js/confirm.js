const svgOptions = document.querySelectorAll('.svg-option');
  let selectedValue = null;

  svgOptions.forEach(svg => {
  svg.addEventListener('click', () => {
    svgOptions.forEach(s => s.classList.remove('selected'));
    svg.classList.add('selected');
    selectedValue = svg.getAttribute('data-value');
    document.getElementById('svgValueInput').value = selectedValue; // 同步值
  });
});

document.getElementById('submit-btn').addEventListener('click', (e) => {
  if (!selectedValue) {
    e.preventDefault(); // 阻止提交
    alert('Please choose one symbol');
    return;
  }
});