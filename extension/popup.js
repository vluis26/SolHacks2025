import { createClient } from "@supabase/supabase-js";


const loginButton = document.getElementById("login-button")

loginButton.addEventListener('click', async () => {
    const manifest = chrome.runtime.getManifest()
    const clientId = manifest.oauth2.client_id
    const scopes = manifest.oauth2.scopes.join(' ')
    const redirectUri = `https://${chrome.runtime.id}.chromiumapp.org`
  
    const authUrl = new URL('https://accounts.google.com/o/oauth2/auth')
    authUrl.searchParams.set('client_id', clientId)
    authUrl.searchParams.set('response_type', 'token id_token')
    authUrl.searchParams.set('redirect_uri', redirectUri)
    authUrl.searchParams.set('scope', scopes)
    authUrl.searchParams.set('prompt', 'consent')
    

    chrome.identity.launchWebAuthFlow(
        {
            url: authUrl.toString(),
            interactive: true,
        },
        async (redirectUrl) => {
            // if (chrome.runtime.lastError || !redirectUrl) {
            //     return new Error(
            //       `WebAuthFlow failed: ${chrome.runtime.lastError.message}`,
            //     )
            // }

            try {
                const redirected = new URL(redirectUrl);
                const params = new URLSearchParams(redirected.hash.substring[1]);
                const idToken = params.get('id_token');
                const accessToken = params.get('access_token');

                sessionStorage.setItem('google_access_token', accessToken);
                sessionStorage.setItem('google_id_token', idToken);
        
                const { data, error } = await supabase.auth.signInWithIdToken({
                    provider: "google",
                    token: idToken
                });

                if (error) {
                    console.log(`Error authenticating with supabase: ${error.message}`);
                } else {
                    console.log("Success");
                }
            } catch (e) {
                console.log(e);
            }
        }
    )
});