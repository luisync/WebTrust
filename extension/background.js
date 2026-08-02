// Create an Id for the rule that restricts this domain from being connected to.
function ruleIdForDomain(domain){
    let hash = 0;

    for (let i = 0; i < domain.length; i++) {
        hash = ((hash << 5) - hash) + domain.charCodeAt(i);
        hash |= 0;
    }

    return Math.abs(hash) + 1;
}

// Fetch the company's domain.
async function getCompanyByDomain(domain){
    const response = await fetch(`http://localhost:8000/companies?domain=${encodeURIComponent(domain)}`);

    if (!response.ok) {
        return null;
    }

    return await response.json()
}

// Blocks the browser from connecting to a certain domain.
async function blockDomain(domain, tabId) {
    const ruleId = ruleIdForDomain(domain);

    const blockedUrl = chrome.runtime.getURL(
        `blocked-page-dist/blocked.html?domain=${encodeURIComponent(domain)}&rating=critical`
    );

    // Define the rule that defines this block.
    const rule = {
        id: ruleId,
        priority: 1,
        action: {
            type: "redirect",
            redirect: {
                extensionPath: "/blocked-page-dist/blocked.html"
            }
        },
        condition: {
            requestDomains: [domain],
            resourceTypes: ["main_frame"]
        }
    };

    // Apply the rule and redirect the user.
    await chrome.declarativeNetRequest.updateSessionRules({
        removeRuleIds: [ruleId],
        addRules: [rule]
    });

    if (typeof tabId === "number") {
        await chrome.tabs.update(tabId, { url: blockedUrl });
    }
}

// Listen for when a page is updated.
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    // Ensure that it is an actual website the user is visiting.
    if (changeInfo.status !== "loading" || !tab.url) {
        return;
    }

    try {
        // Format the URL.
        const url = new URL(tab.url);
        const domain = url.hostname.replace(/^www\./, "");

        // Attempt to link to domain to a company in the database.
        const company = await getCompanyByDomain(domain);
        
        // No company found in the database with a matching domain.
        if (!company) {
            return
        }

        // Block the domain if the company it belongs to is marked as critical.
        if (company.rating === "Critical") {
            await blockDomain(domain, tabId);
        }
    } catch (error) {
        console.error("WebTrust background check falied: ", error)
    }
});
