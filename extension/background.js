console.log("Hello, world!");

import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_KEY
);

chrome.runtime.onMessage.addListener(async (msg, sender, sendResponse) => {
    if (msg.type === "PDF_SELECTED") {
        const binary = atob(msg.base64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
          bytes[i] = binary.charCodeAt(i);
        }
        const blob = new Blob([bytes], { type: "application/pdf" });
        const datetime = Date.now();
        const { data, error } = await supabase.storage
            .from("pdfs")
            .upload(`syllabi/${msg.fileName}${datetime}`, blob, {
                contentType: "application/pdf",
                upset: true
            });

        if (error) {
            console.error("Upload failed:", error);
          } else {
            console.log("Uploaded:", data);
        }

        sendResponse({ success: !error });
        return true;
    }
});