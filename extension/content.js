(() => {
    if (window.__filePickerListenerAdded__) return;
    window.__filePickerListenerAdded__ = true;
  
    chrome.runtime.onMessage.addListener((msg) => {
      if (msg.type === "TRIGGER_FILE_PICKER") {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "application/pdf";
        input.style.display = "none";
  
        input.addEventListener("change", async (event) => {
          const file = event.target.files[0];
          if (file) {
            try {
              console.log("Local file selected:", file.name);
              const reader = new FileReader();
              reader.onload = () => {
                const base64 = reader.result.split(",")[1];
  
                chrome.runtime.sendMessage({
                  type: "PDF_SELECTED",
                  fileName: file.name,
                  base64: base64,
                });
  
                document.body.removeChild(input);
              };
              reader.onerror = (err) => {
                console.error("Error reading file:", err);
              };
              reader.readAsDataURL(file);
            } catch (err) {
              console.error("Error reading file:", err);
            }
          }
        });
  
        document.body.appendChild(input);
        input.click();
      }
    });
  })();
  