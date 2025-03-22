
async function get_access_token(){

    const refresh_token = localStorage.getItem("refresh_token");
    const data = {
        refresh: refresh_token,
    };

    try {
        const response = await fetch(refresh_token_url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.access) {
                localStorage.setItem("access_token", data.access);
                console.log("Access token refreshed successfully!");
            } else {
                console.error("Failed to refresh token, user needs to log in again.");
            }
        } else {
            console.error("Token refresh failed. Logging out user.");
            logout_api();
        }
    } catch (error) {
        console.error("Error refreshing token:", error);
        logout_api();
    }
}