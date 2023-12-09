function Drop(event) {
    event.preventDefault();
  }  
  function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
  
    const givenFile = event.dataTransfer.files[0];
  // pdf checker
    if (givenFile.type === 'application/pdf') {
      const fileInput = document.getElementById("file");
      fileInput.files = event.dataTransfer.files;
      updateFile();
      alert(`File "${givenFile.name}" has been uploaded`);
    } else {
      // pdf validation
      alert('Invalid file, please upload a pdf.');
    }
  }
  function deleteFile(event) {
    event.preventDefault();
    const input = document.querySelector(".file");
    input.remove();
    document.getElementById("file").value = "";
    localStorage.removeItem("file-name");
  }
  function updateFile() {
    const container = document.querySelector(".file-container");
    const input = document.querySelector(".file");
    if (input) input.remove();
    const inputFile = document.getElementById("file")?.files[0];
    if (inputFile?.type === 'application/pdf') {
      localStorage["file-name"] = inputFile.name
      container.innerHTML = `
        <div class="file">
          <span>${inputFile.name}</span>
          <button onclick="deletePDF(event)">X</button>
        </div>
      `;
    }
  }

  function handleFileUpload(event) {
    const fileInput = event.target;
    const files = fileInput.files;
    if (files.length > 0) {
      const givenFile = files[0];

      if (givenFile.type === 'application/pdf') {
        // Update the UI with the new PDF file information
        updateFile();
        alert(`File "${givenFile.name}" has been uploaded`);
      } else {
        // Display an alert if the selected file is not a PDF
        alert('Invalid file, please upload a pdf.');
      }
    }
  }
  
  updateFile();
  