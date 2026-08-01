
// Find the current active tab the user is viewing.
async function getCurrentTab() {
    const tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    return tabs[0];
}

async function main() {
    // Get an object of the current tab.
    const tab = await getCurrentTab();
    const url = new URL(tab.url);
    
    // Format the URL.
    const domain = url.hostname.replace(/^www\./, "");

    // Show the URL in the extension's popup screen.
    document.getElementById("domain").textContent = domain;

    // Attempt to search the databases for the domain for the current website. 
    try {
        const response = await fetch(`http://localhost:8000/companies?domain=${domain}`);
        
        // Domain not found.
        if (!response.ok) {
            document.getElementById("score").textContent =
                "Unknown company";

            return;
        }

        // Update the popup elements to display the company's score and rating.
        const company = await response.json();
        document.getElementById("score").textContent = `Trust Score: ${company.trust_score}`;
        document.getElementById("rating").textContent =`Rating: ${company.rating}`;
    }

    // Search was unable to be conducted because of failure in the API.
    catch (error) {
        document.getElementById("score").textContent =
            "API unavailable";

        console.error(error);
    }
}

main();