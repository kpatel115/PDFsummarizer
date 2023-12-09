function copyToClipboard() {
    const summary = document.getElementById("summary").innerText;
    navigator.clipboard.writeText(summary);
    alert("Copied to Clipboard");
  }