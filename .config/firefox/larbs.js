// These are changes made on top of the Arkenfox JS file to tweak it as
// desired. Any of these settings can be overridden by the user.

// Disable the Twitter/R*ddit/Faceberg ads in the URL bar:
user_pref("browser.urlbar.quicksuggest.enabled", false);
user_pref("browser.urlbar.suggest.topsites", false); // [FF78+]

// Do not suggest web history in the URL bar:
user_pref("browser.urlbar.suggest.history", false);

// Do not prefil forms:
user_pref("signon.prefillForms", false);

// Do not autocomplete in the URL bar:
user_pref("browser.urlbar.autoFill", false);

// Enable the addition of search keywords:
user_pref("keyword.enabled", true);

// Allow access to http (i.e. not https) sites:
user_pref("dom.security.https_only_mode", false);

// Keep cookies until expiration or user deletion:
user_pref("network.cookie.lifetimePolicy", 0);

user_pref("dom.webnotifications.serviceworker.enabled", false);

// Disable push notifications:
user_pref("dom.push.enabled", false);

// Disable the pocket antifeature:
user_pref("extensions.pocket.enabled", false);

// Don't autodelete cookies on shutdown:
user_pref("privacy.clearOnShutdown.cookies", false);

// Enable custom userChrome.js:
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// This could otherwise cause some issues on bank logins and other annoying sites:
user_pref("network.http.referer.XOriginPolicy", 0);

// Disable Firefox sync and its menu entries
user_pref("identity.fxaccounts.enabled", false);

// Fix the issue where right mouse button instantly clicks
user_pref("ui.context_menus.after_mouseup", true);
