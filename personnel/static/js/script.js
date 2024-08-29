const inputVisible = document.querySelectorAll(".inputVisible");
const inputHidden = document.querySelectorAll(".inputHidden");

for (let i = 0; i <= 2; i++) {
    inputHidden[i].addEventListener('change', () => {
        inputVisible[i].value = inputHidden[i].files[0].name;
        console.log(inputHidden[i].files);
    });
}