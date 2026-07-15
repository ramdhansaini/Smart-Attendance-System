const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const startButton = document.getElementById("startCamera");
const captureButton = document.getElementById("captureImage");
const hiddenInput = document.getElementById("capturedImage");
let stream = null;
async function startCamera(){
    try{
        stream = await navigator.mediaDevices.getUserMedia({video : true});
        video.srcObject = stream;
    }
    catch(error){
        console.error("Camera Error:", error);
        alert(error.message);
    }
}
function captureImage(){
    if(!stream){
        alert("Please start the camera first.");
        return;
    }
    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/jpeg");
    hiddenInput.value = imageData;
    alert("Image Captured Successfully.");
}
startButton.addEventListener("click", startCamera);
captureButton.addEventListener("click", captureImage);
window.addEventListener("beforeunload", () => {
    if (stream)
    {
        stream.getTracks().forEach(track => {track.stop();
        });
    }
});