import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_KEY
);

const loginButton = document.getElementById("login-button");
const logoutButton = document.getElementById("logout-button");
const authenticated = document.getElementById("authenticated");
const unauthenticated = document.getElementById("unauthenticated");

loginButton.addEventListener('click', async () => {
    const manifest = chrome.runtime.getManifest();
    const clientId = manifest.oauth2.client_id;
    const scopes = manifest.oauth2.scopes.join(' ');
    const redirectUri = `https://${chrome.runtime.id}.chromiumapp.org`;
  
    const authUrl = new URL('https://accounts.google.com/o/oauth2/auth');
    authUrl.searchParams.set('client_id', clientId);
    authUrl.searchParams.set('response_type', 'token id_token');
    authUrl.searchParams.set('redirect_uri', redirectUri);
    authUrl.searchParams.set('scope', scopes);
    authUrl.searchParams.set('prompt', 'consent');

    chrome.identity.launchWebAuthFlow(
        {
            url: authUrl.toString(),
            interactive: true,
        },
        async (redirectUrl) => {
            if (chrome.runtime.lastError || !redirectUrl) {
                return new Error(
                  `WebAuthFlow failed: ${chrome.runtime.lastError.message}`,
                )
            }

            try {
                const redirected = new URL(redirectUrl);
                const params = new URLSearchParams(redirected.hash.substring(1));
                const idToken = params.get('id_token');
                const accessToken = params.get('access_token');

                sessionStorage.setItem('google_access_token', accessToken);
                sessionStorage.setItem('google_id_token', idToken);
        
                const { data, error } = await supabase.auth.signInWithIdToken({
                    provider: "google",
                    token: idToken
                });

                const user = data.user;
                const email = user.email;

                if (error) {
                    console.log(`Error authenticating with supabase: ${error.message}`);
                } else {
                    console.log("Success");
                    isAuthenticated = true;
                    authenticated.classList.remove("hidden");
                    unauthenticated.classList.add("hidden");
                    
                    document.getElementById("profileEmail").innerText = email;
                }
            } catch (e) {
                console.log(e);
            }
        }
    )
});

logoutButton.addEventListener('click', async () => {
    await supabase.auth.signOut();
    sessionStorage.removeItem('google_access_token');
    sessionStorage.removeItem('google_id_token');
  
    authenticated.classList.add("hidden");
    unauthenticated.classList.remove("hidden");
});

// document.getElementById("loadCalendar").addEventListener('click', async () => {
//     const { data, error } = await supabase.storage.from('pdfs').upload("/", pdfFile);
//     if (error) {
//         console.log(`Error uploading PDF to Supabase Storage`);
//     } else {
//         console.log(`Successfully uploaded PDF to Supabase Storage!`)
//     }
// });

// async function uploadFile(pdf, filename) {
//     const { data, error } = await supabase.storage.from('pdfs').upload(`syllabi/${filename}`, pdf);
//     if (error) {
//         console.log(`Error uploading PDF to Supabase Storage`);
//     } else {
//         console.log(`Successfully uploaded PDF to Supabase Storage!`)
//     }
// }

document.getElementById("uploadPdf").addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
    });

    chrome.tabs.sendMessage(tab.id, { type: "TRIGGER_FILE_PICKER" });
});

// document.getElementById("filePicker").addEventListener('change', async (event) => {
//     const file = event.target.files[0];
//     if (file) {
//         console.log("Local file selected:", file.name);
//         pdfFile = await file.arrayBuffer();
//     }
// });