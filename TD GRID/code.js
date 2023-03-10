const demo = document.querySelector(".demo");


demo.addEventListener("click", ({ target }) => {
    const bloc = target.closest("li");
    bloc.classList.toggle("overlay");
}, { passive: true });
