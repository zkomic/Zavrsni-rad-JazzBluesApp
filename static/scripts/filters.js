document.getElementById('filters-button').addEventListener('click', 
function() {
    document.querySelector('.bg-modal-filters').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click',
function() {
    document.querySelector('.bg-modal-filters').style.display = 'none';
});