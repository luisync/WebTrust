
// Find the current active tab the user is viewing.
async function getCurrentTab() {
    const tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    return tabs[0];
}

// Redirect the user's current tab to a "Blocked site" tab, if the security's rating is poor.
async function redirectPorrSite(tabId, domain){
    const blockedUrl = chrome.runtime.getURL(`blocked.html?domain=${encodeURIComponent(domain)}&rating=poor`);

    // Commence an update event.
    await chrome.tabs.update(tabId, { url: blockedUrl });
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
            document.getElementById("score").textContent = "Unknown company";

            return;
        }

        // Get the company's score and rating.
        const company = await response.json();
        const score = document.getElementById("score");
        const rating = document.getElementById("rating");

        // Display the company's rating on the popup.
        score.textContent = company.trust_score;
        rating.textContent = company.rating;

        // Display a popup to the user if the website is unsafe.
        if (company.rating === "Poor") {
            // Stop the current tab from running.
            await redirectPorrSite(tab.id, domain);
        }

        // Affix the rating of the company as a class in the HTML tag.
        rating.className = "rating";
        rating.classList.add(company.rating.toLowerCase());
    }

    // Search was unable to be conducted because of failure in the API.
    catch (error) {
        document.getElementById("score").textContent = "API unavailable";

        console.error(error);
    }
}

main();