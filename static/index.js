
const form = document.getElementById("upload-form")
const photos = document.getElementById("photos")
const testPhoto = document.getElementById("test-photo")
const photoDisplay = document.getElementById("test-photo-display")

/* images zip upload */
form.addEventListener("submit", async (e) => {
  e.preventDefault()

  const formData = new FormData()
  formData.append("images", photos.files[0])
  
  await fetch("http://127.0.0.1:5000/images", {
    method: "POST",
    body: formData
  })
})

/* test photo upload */
testPhoto.addEventListener("change", (e) => {
  console.dir(testPhoto)

  const reader = new FileReader()
  reader.readAsDataURL(testPhoto.files[0])

  reader.onload = function(e) {
    photoDisplay.style.display = "block"
    photoDisplay.src = e.target.result
  }
})

/* Download model */
function download(data) {
  const a = document.createElement("a")
  const url = URL.createObjectURL(data)

  a.href = url
  a.download = "model.pkl"
  a.click()

  return url
}

const downloadBtn = document.getElementById("download-model")
downloadBtn.addEventListener("click", async function (_) {
  const response = await fetch("http://127.0.0.1:5000/download") 
  const blob = await response.blob()

  const url = download(new Blob([blob]))
  URL.revokeObjectURL(url)

})


/* Upload model */


