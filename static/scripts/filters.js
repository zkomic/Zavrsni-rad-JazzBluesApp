document.getElementById('filters-button').addEventListener('click', 
function() {
    document.querySelector('.bg-modal-filters').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click',
function() {
    document.querySelector('.bg-modal-filters').style.display = 'none';
});

const loadMoreBtn = document.querySelector(".load-more-btn");
const text = document.querySelector(".artists");

loadMoreBtn.addEventListener("click", (e) => {
  text.classList.toggle("show-more");
  if (loadMoreBtn.innerText === "Read More") {
    loadMoreBtn.innerText = "Read Less";
  } else {
    loadMoreBtn.innerText = "Read More";
  }
});
