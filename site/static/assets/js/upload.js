window.onload = () => {

    const uploadFile = document.getElementById("attach");
    const uploadBtn = document.getElementById("upload-btn");
    const uploadText = document.getElementById("upload-text");

    uploadFile.addEventListener("change", function() {
        if(uploadFile.value) {
            uploadText.innerText = uploadFile.value.match(/[\/\\]([\w\d\s\.\-(\)]+)$/)[1];
        }else {
            uploadText.innerText = "Файл не выбран";
        }
    })
}