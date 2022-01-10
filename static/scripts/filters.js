document.getElementById('filters-button').addEventListener('click', 
function() {
    document.querySelector('.bg-modal-filters').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click',
function() {
    document.querySelector('.bg-modal-filters').style.display = 'none';
});


/* LOAD MORE ARTISTS  */

const loadMoreBtn = document.querySelector(".load-more-btn");
const text = document.querySelector(".artists");

loadMoreBtn.addEventListener("click", (e) => {
  text.classList.toggle("show-more");
  if (loadMoreBtn.innerText === "+ See more") {
    loadMoreBtn.innerText = " - See less";
  } else {
    loadMoreBtn.innerText = "+ See more";
  }
});
