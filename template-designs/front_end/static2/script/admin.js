var el = document.getElementById('wrapper');
var toggleButton = document.getElementById('menu-toggle');
toggleButton.onclick = function () {
  el.classList.toggle('toggled');
};

function auto_height(elem) {
  elem.style.height = '1px';
  elem.style.height = elem.scrollHeight + 'px';
}

const selectBtn = document.querySelector('.select-btn'),
  items = document.querySelectorAll('.item');

selectBtn.addEventListener('click', () => {
  selectBtn.classList.toggle('open');
});
