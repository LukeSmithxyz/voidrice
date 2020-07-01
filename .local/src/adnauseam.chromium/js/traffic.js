/*******************************************************************************

    uBlock Origin - a browser extension to block requests.
    Copyright (C) 2014-present Raymond Hill

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see {http://www.gnu.org/licenses/}.

    Home: https://github.com/gorhill/uBlock
*/

'use strict';

/******************************************************************************/

// Start isolation from global scope

µBlock.webRequest = (( ) => {

/******************************************************************************/

const AcceptHeaders = {
    chrome: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    firefox: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
};
const CommonUserAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36';

let exports = {};

/********************************* ADN ****************************************/

// Called before each outgoing request (ADN:)
const onBeforeSendHeaders = function (details) {

  const headers = details.requestHeaders, prefs = µBlock.userSettings, adn = µBlock.adnauseam;

  // if clicking/hiding is enabled with DNT, then send the DNT header
  const respectDNT = ((prefs.clickingAds && prefs.disableClickingForDNT) ||
    (prefs.hidingAds && prefs.disableHidingForDNT));

  if (respectDNT) {

    const pageStore = µBlock.mustPageStoreFromTabId(details.tabId);

    // add it only if the browser is not sending it already
    if (pageStore.getNetFilteringSwitch() && !hasDNT(headers)) {

      if (details.type === 'main_frame') // minimize logging
        adn.logNetEvent('[HEADER]', 'Append', 'DNT:1', details.url);

      addHeader(headers, 'DNT', '1');
    }
  }

  // Is this an XMLHttpRequest ?
  if (vAPI.isBehindTheSceneTabId(details.tabId)) {

    // If so, is it one of our Ad visits ?
    const ad = adn.lookupAd(details.url, details.requestId);

    // if so, handle the headers (cookies, ua, referer, dnt)
    ad && beforeAdVisit(details, headers, prefs, ad, respectDNT);

    //if (ad) console.log('ADN=VISIfT: '+details.url, 'DNT? '+hasDNT(headers), ad);
  }

  // ADN: if this was an adn-allowed request, do we block cookies, etc.? TODO
  return { requestHeaders: headers };
};

// ADN: remove outgoing cookies, reset user-agent, strip referer
const beforeAdVisit = function (details, headers, prefs, ad, respectDNT) {

  const referer = ad.pageUrl, refererIdx = -1, dbug = 1;
  let uirIdx = -1;

  ad.requestId = details.requestId; // needed?

  dbug && console.log('[HEADERS] (Outgoing'+(ad.targetUrl===details.url ? ')' : '-redirect)'), details.url);

  for (let i = headers.length - 1; i >= 0; i--) {

    dbug && console.log(i + ") " + headers[i].name, headers[i].value);
    const name = headers[i].name.toLowerCase();

    if ((name === 'http_x_requested_with') ||
      (name === 'x-devtools-emulate-network-conditions-client-id') ||
      (prefs.noOutgoingCookies && name === 'cookie') ||
      (prefs.noOutgoingUserAgent && name === 'user-agent'))
    {
      setHeader(headers[i], '');

      // Block outgoing cookies and user-agent here if specified
      if (prefs.noOutgoingCookies && name === 'cookie') {

        µBlock.adnauseam.logNetEvent('[COOKIE]', 'Strip', headers[i].value, details.url);
      }

      // Replace user-agent with most common string, if specified
      if (prefs.noOutgoingUserAgent && name === 'user-agent') {

         headers[i].value = CommonUserAgent;
         µBlock.adnauseam.logNetEvent('[UAGENT]', 'Default', headers[i].value, details.url);
      }
    }

    if (name === 'referer') refererIdx = i;

    if (vAPI.chrome && name === 'upgrade-insecure-requests') uirIdx = i;

    if (name === 'accept') { // Set browser-specific accept header
      setHeader(headers[i], vAPI.firefox ? AcceptHeaders.firefox : AcceptHeaders.chrome);
    }
  }

  // Add UIR header if chrome
  if (vAPI.chrome && uirIdx < 0) {
    addHeader(headers, 'Upgrade-Insecure-Requests', '1');
  }

  // add DNT header if needed and not included
  if (respectDNT && !hasDNT(headers)) {
    addHeader(headers, 'DNT', '1');
  }

  handleRefererForVisit(prefs, refererIdx, referer, details.url, headers);
};

const handleRefererForVisit = function (prefs, refIdx, referer, url, headers) {

  // console.log('handleRefererForVisit()', arguments);

  // Referer cases (4):
  // noOutgoingReferer=true  / no refIdx:     no-op
  // noOutgoingReferer=true  / have refIdx:   setHeader('')
  // noOutgoingReferer=false / no refIdx:     addHeader(referer)
  // noOutgoingReferer=false / have refIdx:   no-op
  if (refIdx > -1 && prefs.noOutgoingReferer) {

    // will never happen when using XMLHttpRequest
    µBlock.adnauseam.logNetEvent('[REFERER]', 'Strip', referer, url);
    setHeader(headers[refIdx], '');

  } else if (!prefs.noOutgoingReferer && refIdx < 0) {

    µBlock.adnauseam.logNetEvent('[REFERER]', 'Allow', referer, url);
    addHeader(headers, 'Referer', referer);
  }
};

function dumpHeaders(headers) {

  const s = '\n\n';
  for (let i = headers.length - 1; i >= 0; i--) {
    s += headers[i].name + ': ' + headers[i].value + '\n';
  }
  return s;
}

const setHeader = function (header, value) {

  if (header) header.value = value;
};

const addHeader = function (headers, name, value) {
  headers.push({
    name: name,
    value: value
  });
};

const hasDNT = function (headers) {

  for (let i = headers.length - 1; i >= 0; i--) {
    if (headers[i].name === 'DNT' && headers[i].value === '1') {
      return true;
    }
  }
  return false;
}

/******************************************************************************/

// Platform-specific behavior.

// https://github.com/uBlockOrigin/uBlock-issues/issues/42
// https://bugzilla.mozilla.org/show_bug.cgi?id=1376932
//   Add proper version number detection once issue is fixed in Firefox.
let dontCacheResponseHeaders =
    vAPI.webextFlavor.soup.has('firefox');

// https://github.com/gorhill/uMatrix/issues/967#issuecomment-373002011
//   This can be removed once Firefox 60 ESR is released.
let cantMergeCSPHeaders =
    vAPI.webextFlavor.soup.has('firefox') && vAPI.webextFlavor.major < 59;


// The real actual webextFlavor value may not be set in stone, so listen
// for possible future changes.
window.addEventListener('webextFlavor', function() {
    dontCacheResponseHeaders =
        vAPI.webextFlavor.soup.has('firefox');
    cantMergeCSPHeaders =
        vAPI.webextFlavor.soup.has('firefox') &&
        vAPI.webextFlavor.major < 59;
}, { once: true });

/******************************************************************************/

// Intercept and filter web requests.

const onBeforeRequest = function(details) {
    const fctxt = µBlock.filteringContext.fromWebrequestDetails(details);

    // Special handling for root document.
    // https://github.com/chrisaljoudi/uBlock/issues/1001
    // This must be executed regardless of whether the request is
    // behind-the-scene
    if ( details.type === 'main_frame' ) {
        return onBeforeRootFrameRequest(fctxt);
    }

    // ADN: return here (AFTER onPageLoad) if prefs say not to block
    if (µBlock.userSettings.blockingMalware === false) return;

    // Special treatment: behind-the-scene requests
    const tabId = details.tabId;
    if ( tabId < 0 ) {
        return onBeforeBehindTheSceneRequest(fctxt);
    }

    // Lookup the page store associated with this tab id.
    const µb = µBlock;
    let pageStore = µb.pageStoreFromTabId(tabId);
    if ( pageStore === null ) {
        const tabContext = µb.tabContextManager.mustLookup(tabId);
        if ( tabContext.tabId < 0 ) {
            return onBeforeBehindTheSceneRequest(fctxt);
        }
        vAPI.tabs.onNavigation({ tabId, frameId: 0, url: tabContext.rawURL });
        pageStore = µb.pageStoreFromTabId(tabId);
    }

    const result = pageStore.filterRequest(fctxt);

    pageStore.journalAddRequest(fctxt.getHostname(), result);

    if ( µb.logger.enabled ) {
        fctxt.setRealm('network').toLogger();
    }

    // Not blocked
    if ( result !== 1 ) {
        if (
            details.parentFrameId !== -1 &&
            details.type === 'sub_frame' &&
            details.aliasURL === undefined
        ) {
            pageStore.setFrame(details.frameId, details.url);
        }
        if ( result === 2 ) {
            return { cancel: false };
        }
        return;
    }

    // Blocked

    // https://github.com/gorhill/uBlock/issues/949
    //   Redirect blocked request?
    if ( µb.hiddenSettings.ignoreRedirectFilters !== true ) {
        const url = µb.redirectEngine.toURL(fctxt);
        if ( url !== undefined ) {
            // µb.adnauseam.logRedirect(requestURL, url); // ADN, log redirects (not needed)
            pageStore.internalRedirectionCount += 1;
            if ( µb.logger.enabled ) {
                fctxt.setRealm('redirect')
                     .setFilter({ source: 'redirect', raw: µb.redirectEngine.resourceNameRegister })
                     .toLogger();
            }
            return { redirectUrl: url };
        }
    }

    return { cancel: true };
};

/******************************************************************************/

const onBeforeRootFrameRequest = function(fctxt) {
    const µb = µBlock;
    const requestURL = fctxt.url;

    // Special handling for root document.
    // https://github.com/chrisaljoudi/uBlock/issues/1001
    //   This must be executed regardless of whether the request is
    //   behind-the-scene
    const requestHostname = fctxt.getHostname();
    const logEnabled = µb.logger.enabled;
    let result = 0,
        logData;

    // If the site is whitelisted, disregard strict blocking
    if ( µb.getNetFilteringSwitch(requestURL) === false ) {
        result = 2;
        if ( logEnabled ) {
            logData = { engine: 'u', result: 2, raw: 'whitelisted' };
        }
    }

    // Permanently unrestricted?
    if (
        result === 0 &&
        µb.sessionSwitches.evaluateZ('no-strict-blocking', requestHostname)
    ) {
        result = 2;
        if ( logEnabled ) {
            logData = { engine: 'u', result: 2, raw: 'no-strict-blocking: ' + µb.sessionSwitches.z + ' true' };
        }
    }

    // Temporarily whitelisted?
    if ( result === 0 && strictBlockBypasser.isBypassed(requestHostname) ) {
        result = 2;
        if ( logEnabled ) {
            logData = { engine: 'u', result: 2, raw: 'no-strict-blocking: true (temporary)' };
        }
    }

    // Static filtering: We always need the long-form result here.
    const snfe = µb.staticNetFilteringEngine;

    // Check for specific block
    if ( result === 0 ) {
        fctxt.type = 'main_frame';
        result = snfe.matchString(fctxt, 0b0001);
        if ( result !== 0 || logEnabled ) {
            logData = snfe.toLogData();
        }
    }

    // Check for generic block
    if ( result === 0 ) {
        fctxt.type = 'no_type';
        result = snfe.matchString(fctxt, 0b0001);
        if ( result !== 0 || logEnabled ) {
            logData = snfe.toLogData();
        }
        // https://github.com/chrisaljoudi/uBlock/issues/1128
        // Do not block if the match begins after the hostname, except when
        // the filter is specifically of type `other`.
        // https://github.com/gorhill/uBlock/issues/490
        // Removing this for the time being, will need a new, dedicated type.
        if (
            result === 1 &&
            toBlockDocResult(requestURL, requestHostname, logData) === false
        ) {
            result = 0;
            logData = undefined;
        }
    }

    // ADN: Tell the core we have a new page
    µb.adnauseam.onPageLoad(fctxt.tabId, requestURL);

    // ADN: return here if prefs say not to block
    if (µb.userSettings.blockingMalware === false) return;

    // Log
    fctxt.type = 'main_frame';
    const pageStore = µb.bindTabToPageStats(fctxt.tabId, 'beforeRequest');
    if ( pageStore ) {
        pageStore.journalAddRootFrame('uncommitted', requestURL);
        pageStore.journalAddRequest(requestHostname, result);
    }

    if ( logEnabled ) {
        fctxt.setRealm('network').setFilter(logData).toLogger();
    }

    // Not blocked
    if ( result !== 1 ) { return; }

    // No log data means no strict blocking (because we need to report why
    // the blocking occurs.
    if ( logData === undefined  ) { return; }

    // Blocked
    const query = encodeURIComponent(JSON.stringify({
        url: requestURL,
        hn: requestHostname,
        dn: fctxt.getDomain() || requestHostname,
        fs: logData.raw
    }));

    vAPI.tabs.replace(
        fctxt.tabId,
        vAPI.getURL('document-blocked.html?details=') + query
    );

};

/******************************************************************************/

// https://github.com/gorhill/uBlock/issues/3208
//   Mind case insensitivity.

const toBlockDocResult = function(url, hostname, logData) {
    if ( typeof logData.regex !== 'string' ) { return false; }
    const re = new RegExp(logData.regex, 'i');
    const match = re.exec(url.toLowerCase());
    if ( match === null ) { return false; }

    // https://github.com/chrisaljoudi/uBlock/issues/1128
    // https://github.com/chrisaljoudi/uBlock/issues/1212
    //   Verify that the end of the match is anchored to the end of the
    //   hostname.
    const end = match.index + match[0].length -
                url.indexOf(hostname) - hostname.length;
    return end === 0 || end === 1;
};

/******************************************************************************/

// Intercept and filter behind-the-scene requests.

// https://github.com/gorhill/uBlock/issues/870
// Finally, Chromium 49+ gained the ability to report network request of type
// `beacon`, so now we can block them according to the state of the
// "Disable hyperlink auditing/beacon" setting.

const onBeforeBehindTheSceneRequest = function(fctxt) {

    if (µBlock.userSettings.blockingMalware === false) return; // ADN

    const µb = µBlock,
        pageStore = µb.pageStoreFromTabId(fctxt.tabId);
    if ( pageStore === null ) { return; }

    // https://bugs.chromium.org/p/chromium/issues/detail?id=637577#c15
    //   Do not filter behind-the-scene network request of type `beacon`: there
    //   is no point. In any case, this will become a non-issue once
    //   <https://bugs.chromium.org/p/chromium/issues/detail?id=522129> is
    //   fixed.

    // Blocking behind-the-scene requests can break a lot of stuff: prevent
    // browser updates, prevent extension updates, prevent extensions from
    // working properly, etc.
    // So we filter if and only if the "advanced user" mode is selected.
    // https://github.com/gorhill/uBlock/issues/3150
    //   Ability to globally block CSP reports MUST also apply to
    //   behind-the-scene network requests.

    // 2018-03-30:
    //   Filter all behind-the-scene network requests like any other network
    //   requests. Hopefully this will not break stuff as it used to be the
    //   case.

    let result = 0;

    // https://github.com/uBlockOrigin/uBlock-issues/issues/339
    //   Need to also test against `-scheme` since tabOrigin is normalized.
    //   Not especially elegant but for now this accomplishes the purpose of
    //   not dealing with network requests fired from a synthetic scope,
    //   that is unless advanced user mode is enabled.

    if (
        fctxt.tabOrigin.endsWith('-scheme') === false &&
        µb.URI.isNetworkURI(fctxt.tabOrigin) ||
        µb.userSettings.advancedUserEnabled ||
        fctxt.type === 'csp_report'
    ) {
        result = pageStore.filterRequest(fctxt);

        // The "any-tab" scope is not whitelist-able, and in such case we must
        // use the origin URL as the scope. Most such requests aren't going to
        // be blocked, so we further test for whitelisting and modify the
        // result only when the request is being blocked.
        if (
            result === 1 &&
            µb.getNetFilteringSwitch(fctxt.tabOrigin) === false
        ) {
            result = 2;
            fctxt.filter = { engine: 'u', result: 2, raw: 'whitelisted' };
        }
    }

    if ( µb.logger.enabled ) {
        fctxt.setRealm('network').toLogger();
    }

    // Blocked?
    if ( result === 1 ) {
        // ADN: Blocked xhr
        µb.adnauseam.logNetBlock(fctxt.type, fctxt.url);
        return { cancel: true };
    }

};

/******************************************************************************/

// https://github.com/gorhill/uBlock/issues/3140

const onBeforeMaybeSpuriousCSPReport = (function() {
    let textDecoder;

    return function(details) {
        const fctxt = µBlock.filteringContext.fromWebrequestDetails(details);

        // Ignore behind-the-scene requests.
        if ( fctxt.tabId < 0 ) { return; }

        // Lookup the page store associated with this tab id.
        const pageStore = µBlock.pageStoreFromTabId(fctxt.tabId);
        if ( pageStore === null ) { return; }

        // If uBO is disabled for the page, it can't possibly causes CSP
        // reports to be triggered.
        if ( pageStore.getNetFilteringSwitch() === false ) { return; }

        // A resource was redirected to a neutered one?
        // TODO: mind injected scripts/styles as well.
        if ( pageStore.internalRedirectionCount === 0 ) { return; }

        if (
            textDecoder === undefined &&
            typeof self.TextDecoder === 'function'
        ) {
            textDecoder = new TextDecoder();
        }

        // Find out whether the CSP report is a potentially spurious CSP report.
        // If from this point on we are unable to parse the CSP report data,
        // the safest assumption to protect users is to assume the CSP report
        // is spurious.
        if (
            textDecoder !== undefined &&
            details.method === 'POST'
        ) {
            const raw = details.requestBody && details.requestBody.raw;
            if (
                Array.isArray(raw) &&
                raw.length !== 0 &&
                raw[0] instanceof Object &&
                raw[0].bytes instanceof ArrayBuffer
            ) {
                let data;
                try {
                    data = JSON.parse(textDecoder.decode(raw[0].bytes));
                } catch (ex) {
                }
                if ( data instanceof Object ) {
                    const report = data['csp-report'];
                    if ( report instanceof Object ) {
                        const blocked =
                            report['blocked-uri'] || report['blockedURI'];
                        const validBlocked = typeof blocked === 'string';
                        const source =
                            report['source-file'] || report['sourceFile'];
                        const validSource = typeof source === 'string';
                        if (
                            (validBlocked || validSource) &&
                            (!validBlocked || !blocked.startsWith('data')) &&
                            (!validSource || !source.startsWith('data'))
                        ) {
                            return;
                        }
                    }
                }
            }
        }

        // At this point, we have a potentially spurious CSP report.

        if ( µBlock.logger.enabled ) {
            fctxt.setRealm('network')
                 .setType('csp_report')
                 .setFilter({ result: 1, source: 'global', raw: 'no-spurious-csp-report' })
                 .toLogger();
        }

        return { cancel: true };
    };
})();

/******************************************************************************/
const handleIncomingCookiesForAdVisits = function(details) {
  let ad, modified; //ADN
  const dbug = 0; //ADN
  const µb = µBlock;
  const tabId = details.tabId;

  if (vAPI.isBehindTheSceneTabId(tabId)) {

    // ADN: handle incoming cookies for our visits
    if (µb.userSettings.noIncomingCookies) {

        dbug && console.log('onHeadersReceived: ', details.url, details.responseHeaders);
        // ADN
        ad = µb.adnauseam.lookupAd(details.url, details.requestId);
        if (ad) {
          // this is an ADN request
          modified = µb.adnauseam.blockIncomingCookies(details.responseHeaders, details.url, ad.targetUrl);
        }
        else if (dbug && vAPI.chrome) {
          console.log('Ignoring non-ADN response', details.url);
        }
    }
    // don't return an empty headers array
    return modified && modified.length ? modified : null;
  }
}
// To handle:
// - Media elements larger than n kB
// - Scriptlet injection (requires ability to modify response body)
// - HTML filtering (requires ability to modify response body)
// - CSP injection
const adnOnHeadersRecieved = function(details) {

  // 1: check ad visit
  const modifiedHeadersForAdVisits = handleIncomingCookiesForAdVisits(details);
  if (typeof modifiedHeadersForAdVisits != "boolean") return { responseHeaders: modifiedHeadersForAdVisits }

  // 2: ublock filtering for the following request types:
  let headers;
  const ublock_filtering_types = ['main_frame','sub_frame','image','media','xmlhttprequest'];
  if (ublock_filtering_types.indexOf(details.type) > -1) {
    headers = onHeadersReceived(details)
  }

  if (headers == undefined) {
    // ublock doesn't modified it
    headers = details.responseHeaders;
  }

  // 3: Check for AdNauseam allowed
  const fctxt = µb.filteringContext.fromWebrequestDetails(details);
  const pageStore = µb.pageStoreFromTabId(fctxt.tabId);
  const modifiedHeadersForAdNauseamAllowed = pageStore && µBlock.adnauseam.checkAllowedException
          (headers, details.url, pageStore.rawURL);

  if (typeof modifiedHeadersForAdNauseamAllowed != "boolean") {
    return {responseHeaders: modifiedHeadersForAdNauseamAllowed}
  }
}
const onHeadersReceived = function(details) {
    // https://github.com/uBlockOrigin/uBlock-issues/issues/610
    // Process behind-the-scene requests in a special way.
    if (
        details.tabId < 0 &&
        normalizeBehindTheSceneResponseHeaders(details) === false
    ) {
        return;
    }

    const µb = µBlock;
    const fctxt = µb.filteringContext.fromWebrequestDetails(details);
    const requestType = fctxt.type;
    const isRootDoc = requestType === 'main_frame';
    const isDoc = isRootDoc || requestType === 'sub_frame';

    let pageStore = µb.pageStoreFromTabId(fctxt.tabId);

    if ( pageStore === null ) {
        if ( isRootDoc === false ) { return; }
        pageStore = µb.bindTabToPageStats(fctxt.tabId, 'beforeRequest');
    }
    if ( pageStore.getNetFilteringSwitch(fctxt) === false ) { return; }

    // Keep in mind response headers will be modified in-place if needed, so
    // `details.responseHeaders` will always point to the modified response
    // headers.
    const responseHeaders = details.responseHeaders;

    if ( requestType === 'image' || requestType === 'media' ) {
        return foilLargeMediaElement(fctxt, pageStore, responseHeaders);
    }

    if ( isDoc === false ) { return; }
    // https://github.com/gorhill/uBlock/issues/2813
    //   Disable the blocking of large media elements if the document is itself
    //   a media element: the resource was not prevented from loading so no
    //   point to further block large media elements for the current document.
    if ( isRootDoc ) {
        const contentType = headerValueFromName('content-type', responseHeaders);
        if ( reMediaContentTypes.test(contentType) ) {
            pageStore.allowLargeMediaElementsUntil = Date.now() + 86400000;
            return;
        }
    }

    // At this point we have a HTML document.

    const filteredHTML = µb.canFilterResponseData &&
                         filterDocument(pageStore, fctxt, details) === true;

    let modifiedHeaders = injectCSP(fctxt, pageStore, responseHeaders) === true;

    // https://bugzilla.mozilla.org/show_bug.cgi?id=1376932
    //   Prevent document from being cached by the browser if we modified it,
    //   either through HTML filtering and/or modified response headers.
    // https://github.com/uBlockOrigin/uBlock-issues/issues/229
    //   Use `no-cache` instead of `no-cache, no-store, must-revalidate`, this
    //   allows Firefox's offline mode to work as expected.
    if ( (filteredHTML || modifiedHeaders) && dontCacheResponseHeaders ) {
        let cacheControl = µb.hiddenSettings.cacheControlForFirefox1376932;
        if ( cacheControl !== 'unset' ) {
            let i = headerIndexFromName('cache-control', responseHeaders);
            if ( i !== -1 ) {
                responseHeaders[i].value = cacheControl;
            } else {
                responseHeaders.push({ name: 'Cache-Control', value: cacheControl });
            }
            modifiedHeaders = true;
        }
    }

    if ( modifiedHeaders ) {
        return { responseHeaders: responseHeaders };
    }
};

const reMediaContentTypes = /^(?:audio|image|video)\//;

/******************************************************************************/

// https://github.com/uBlockOrigin/uBlock-issues/issues/610

const normalizeBehindTheSceneResponseHeaders = function(details) {
    if ( details.type !== 'xmlhttprequest' ) { return false; }
    const headers = details.responseHeaders;
    if ( Array.isArray(headers) === false ) { return false; }
    const contentType = headerValueFromName('content-type', headers);
    if ( contentType === '' ) { return false; }
    if ( reMediaContentTypes.test(contentType) === false ) { return false; }
    if ( contentType.startsWith('image') ) {
        details.type = 'image';
    } else {
        details.type = 'media';
    }
    return true;
};

/*******************************************************************************

    The response body filterer is responsible for:

    - HTML filtering

    In the spirit of efficiency, the response body filterer works this way:

    If:
        - HTML filtering: no.
    Then:
        No response body filtering is initiated.

    If:
        - HTML filtering: yes.
    Then:
        Assemble all response body data into a single buffer. Once all the
        response data has been received, create a document from it. Then:
        - Remove all DOM elements matching HTML filters.
        Then serialize the resulting modified document as the new response
        body.

**/

const filterDocument = (function() {
    const µb = µBlock;
    const filterers = new Map();
    let domParser, xmlSerializer,
        utf8TextDecoder, textDecoder, textEncoder;

    const textDecode = function(encoding, buffer) {
        if (
            textDecoder !== undefined &&
            textDecoder.encoding !== encoding
        ) {
            textDecoder = undefined;
        }
        if ( textDecoder === undefined ) {
            textDecoder = new TextDecoder(encoding);
        }
        return textDecoder.decode(buffer);
    };

    const reContentTypeDocument = /^(?:text\/html|application\/xhtml\+xml)/i;
    const reContentTypeCharset = /charset=['"]?([^'" ]+)/i;

    const mimeFromContentType = function(contentType) {
        const match = reContentTypeDocument.exec(contentType);
        if ( match !== null ) {
            return match[0].toLowerCase();
        }
    };

    const charsetFromContentType = function(contentType) {
        const match = reContentTypeCharset.exec(contentType);
        if ( match !== null ) {
            return match[1].toLowerCase();
        }
    };

    const charsetFromDoc = function(doc) {
        let meta = doc.querySelector('meta[charset]');
        if ( meta !== null ) {
            return meta.getAttribute('charset').toLowerCase();
        }
        meta = doc.querySelector(
            'meta[http-equiv="content-type" i][content]'
        );
        if ( meta !== null ) {
            return charsetFromContentType(meta.getAttribute('content'));
        }
    };

    const streamClose = function(filterer, buffer) {
        if ( buffer !== undefined ) {
            filterer.stream.write(buffer);
        } else if ( filterer.buffer !== undefined ) {
            filterer.stream.write(filterer.buffer);
        }
        filterer.stream.close();
    };

    const onStreamData = function(ev) {
        const filterer = filterers.get(this);
        if ( filterer === undefined ) {
            this.write(ev.data);
            this.disconnect();
            return;
        }
        if (
            this.status !== 'transferringdata' &&
            this.status !== 'finishedtransferringdata'
        ) {
            filterers.delete(this);
            this.disconnect();
            return;
        }
        // TODO:
        // - Possibly improve buffer growth, if benchmarking shows it's worth
        //   it.
        // - Also evaluate whether keeping a list of buffers and then decoding
        //   them in sequence using TextDecoder's "stream" option is more
        //   efficient. Can the data buffers be safely kept around for later
        //   use?
        // - Informal, quick benchmarks seem to show most of the overhead is
        //   from calling TextDecoder.decode() and TextEncoder.encode(), and if
        //   confirmed, there is nothing which can be done uBO-side to reduce
        //   overhead.
        if ( filterer.buffer === null ) {
            filterer.buffer = new Uint8Array(ev.data);
            return;
        }
        const buffer = new Uint8Array(
            filterer.buffer.byteLength +
            ev.data.byteLength
        );
        buffer.set(filterer.buffer);
        buffer.set(new Uint8Array(ev.data), filterer.buffer.byteLength);
        filterer.buffer = buffer;
    };

    const onStreamStop = function() {
        const filterer = filterers.get(this);
        filterers.delete(this);
        if ( filterer === undefined || filterer.buffer === null ) {
            this.close();
            return;
        }
        if ( this.status !== 'finishedtransferringdata' ) { return; }

        if ( domParser === undefined ) {
            domParser = new DOMParser();
            xmlSerializer = new XMLSerializer();
        }
        if ( textEncoder === undefined ) {
            textEncoder = new TextEncoder();
        }

        let doc;

        // If stream encoding is still unknnown, try to extract from document.
        let charsetFound = filterer.charset,
            charsetUsed = charsetFound;
        if ( charsetFound === undefined ) {
            if ( utf8TextDecoder === undefined ) {
                utf8TextDecoder = new TextDecoder();
            }
            doc = domParser.parseFromString(
              utf8TextDecoder.decode(filterer.buffer.slice(0, 1024)),
              filterer.mime
            );
            charsetFound = charsetFromDoc(doc);
            charsetUsed = µb.textEncode.normalizeCharset(charsetFound);
            if ( charsetUsed === undefined ) {
                return streamClose(filterer);
            }
        }

        doc = domParser.parseFromString(
            textDecode(charsetUsed, filterer.buffer),
            filterer.mime
        );

        // https://github.com/gorhill/uBlock/issues/3507
        //   In case of no explicit charset found, try to find one again, but
        //   this time with the whole document parsed.
        if ( charsetFound === undefined ) {
            charsetFound = µb.textEncode.normalizeCharset(charsetFromDoc(doc));
            if ( charsetFound !== charsetUsed ) {
                if ( charsetFound === undefined ) {
                    return streamClose(filterer);
                }
                charsetUsed = charsetFound;
                doc = domParser.parseFromString(
                    textDecode(charsetFound, filterer.buffer),
                    filterer.mime
                );
            }
        }

        let modified = false;
        if ( filterer.selectors !== undefined ) {
            if ( µb.htmlFilteringEngine.apply(doc, filterer) ) {
                modified = true;
            }
        }

        if ( modified === false ) {
            return streamClose(filterer);
        }

        // https://stackoverflow.com/questions/6088972/get-doctype-of-an-html-as-string-with-javascript/10162353#10162353
        const doctypeStr = doc.doctype instanceof Object ?
                xmlSerializer.serializeToString(doc.doctype) + '\n' :
                '';

        // https://github.com/gorhill/uBlock/issues/3391
        let encodedStream = textEncoder.encode(
            doctypeStr +
            doc.documentElement.outerHTML
        );
        if ( charsetUsed !== 'utf-8' ) {
            encodedStream = µb.textEncode.encode(
                charsetUsed,
                encodedStream
            );
        }

        streamClose(filterer, encodedStream);
    };

    const onStreamError = function() {
        filterers.delete(this);
    };

    return function(pageStore, fctxt, extras) {
        // https://github.com/gorhill/uBlock/issues/3478
        const statusCode = extras.statusCode || 0;
        if ( statusCode !== 0 && (statusCode < 200 || statusCode >= 300) ) {
            return;
        }

        const hostname = fctxt.getHostname();
        if ( hostname === '' ) { return; }

        const domain = fctxt.getDomain();

        const request = {
            stream: undefined,
            tabId: fctxt.tabId,
            url: fctxt.url,
            hostname: hostname,
            domain: domain,
            entity: µb.URI.entityFromDomain(domain),
            selectors: undefined,
            buffer: null,
            mime: 'text/html',
            charset: undefined
        };

        request.selectors = µb.htmlFilteringEngine.retrieve(request);
        if ( request.selectors === undefined ) { return; }

        const headers = extras.responseHeaders;
        const contentType = headerValueFromName('content-type', headers);
        if ( contentType !== '' ) {
            request.mime = mimeFromContentType(contentType);
            if ( request.mime === undefined ) { return; }
            let charset = charsetFromContentType(contentType);
            if ( charset !== undefined ) {
                charset = µb.textEncode.normalizeCharset(charset);
                if ( charset === undefined ) { return; }
                request.charset = charset;
            }
        }
        // https://bugzilla.mozilla.org/show_bug.cgi?id=1426789
        if ( headerValueFromName('content-disposition', headers) ) { return; }

        const stream = request.stream =
            browser.webRequest.filterResponseData(extras.requestId);
        stream.ondata = onStreamData;
        stream.onstop = onStreamStop;
        stream.onerror = onStreamError;
        filterers.set(stream, request);

        return true;
    };
})();

/******************************************************************************/

const injectCSP = function(fctxt, pageStore, responseHeaders) {
    const µb = µBlock;
    const loggerEnabled = µb.logger.enabled;
    const cspSubsets = [];

    // Start collecting policies >>>>>>>>

    // ======== built-in policies

    const builtinDirectives = [];

    if ( pageStore.filterScripting(fctxt, true) === 1 ) {
        builtinDirectives.push(µBlock.cspNoScripting);
        if ( loggerEnabled ) {
            fctxt.setRealm('network').setType('scripting').toLogger();
        }
    }
    // https://github.com/uBlockOrigin/uBlock-issues/issues/422
    //   We need to derive a special context for filtering `inline-script`,
    //   as the embedding document for this "resource" will always be the
    //   frame itself, not that of the parent of the frame.
    else {
        const fctxt2 = fctxt.duplicate();
        fctxt2.type = 'inline-script';
        fctxt2.setDocOriginFromURL(fctxt.url);
        const result = pageStore.filterRequest(fctxt2);
        if ( result === 1 ) {
            builtinDirectives.push(µBlock.cspNoInlineScript);
        }
        if ( result === 2 && loggerEnabled ) {
            fctxt2.setRealm('network').toLogger();
        }
    }

    // https://github.com/gorhill/uBlock/issues/1539
    // - Use a CSP to also forbid inline fonts if remote fonts are blocked.
    fctxt.type = 'inline-font';
    if ( pageStore.filterRequest(fctxt) === 1 ) {
        builtinDirectives.push(µBlock.cspNoInlineFont);
        if ( loggerEnabled ) {
            fctxt.setRealm('network').toLogger();
        }
    }

    if ( builtinDirectives.length !== 0 ) {
        cspSubsets[0] = builtinDirectives.join(', ');
    }

    // ======== filter-based policies

    // Static filtering.

    const staticDirectives =
        µb.staticNetFilteringEngine.matchAndFetchData(fctxt, 'csp');
    for ( const directive of staticDirectives ) {
        if ( directive.result !== 1 ) { continue; }
        cspSubsets.push(directive.getData('csp'));
    }

    // URL filtering `allow` rules override static filtering.
    if (
        cspSubsets.length !== 0 &&
        µb.sessionURLFiltering.evaluateZ(
            fctxt.getTabHostname(),
            fctxt.url,
            'csp'
        ) === 2
    ) {
        if ( loggerEnabled ) {
            fctxt.setRealm('network')
                 .setType('csp')
                 .setFilter(µb.sessionURLFiltering.toLogData())
                 .toLogger();
        }
        return;
    }

    // Dynamic filtering `allow` rules override static filtering.
    if (
        cspSubsets.length !== 0 &&
        µb.userSettings.advancedUserEnabled &&
        µb.sessionFirewall.evaluateCellZY(
            fctxt.getTabHostname(),
            fctxt.getTabHostname(),
            '*'
        ) === 2
    ) {
        if ( loggerEnabled ) {
            fctxt.setRealm('network')
                 .setType('csp')
                 .setFilter(µb.sessionFirewall.toLogData())
                 .toLogger();
        }
        return;
    }

    // <<<<<<<< All policies have been collected

    // Static CSP policies will be applied.

    if ( loggerEnabled && staticDirectives.length !== 0 ) {
        fctxt.setRealm('network').setType('csp');
        for ( const directive of staticDirectives ) {
            fctxt.setFilter(directive.logData()).toLogger();
        }
    }

    if ( cspSubsets.length === 0 ) { return; }

    µb.updateToolbarIcon(fctxt.tabId);

    // Use comma to merge CSP directives.
    // Ref.: https://www.w3.org/TR/CSP2/#implementation-considerations
    //
    // https://github.com/gorhill/uMatrix/issues/967
    //   Inject a new CSP header rather than modify an existing one, except
    //   if the current environment does not support merging headers:
    //   Firefox 58/webext and less can't merge CSP headers, so we will merge
    //   them here.

    if ( cantMergeCSPHeaders ) {
        const i = headerIndexFromName(
            'content-security-policy',
            responseHeaders
        );
        if ( i !== -1 ) {
            cspSubsets.unshift(responseHeaders[i].value.trim());
            responseHeaders.splice(i, 1);
        }
    }

    responseHeaders.push({
        name: 'Content-Security-Policy',
        value: cspSubsets.join(', ')
    });

    return true;
};

/******************************************************************************/

// https://github.com/gorhill/uBlock/issues/1163
//   "Block elements by size"

const foilLargeMediaElement = function(fctxt, pageStore, responseHeaders) {
    let size = 0;
    if ( µBlock.userSettings.largeMediaSize !== 0 ) {
        const i = headerIndexFromName('content-length', responseHeaders);
        if ( i === -1 ) { return; }
        size = parseInt(responseHeaders[i].value, 10) || 0;
    }

    const result = pageStore.filterLargeMediaElement(fctxt, size);
    if ( result === 0 ) { return; }

    if ( µBlock.logger.enabled ) {
        fctxt.setRealm('network').toLogger();
    }

    return { cancel: true };
};

/******************************************************************************/

// Caller must ensure headerName is normalized to lower case.

const headerIndexFromName = function(headerName, headers) {
    let i = headers.length;
    while ( i-- ) {
        if ( headers[i].name.toLowerCase() === headerName ) {
            return i;
        }
    }
    return -1;
};

const headerValueFromName = function(headerName, headers) {
    const i = headerIndexFromName(headerName, headers);
    return i !== -1 ? headers[i].value : '';
};


const strictBlockBypasser = {
    hostnameToDeadlineMap: new Map(),
    cleanupTimer: undefined,

    cleanup: function() {
        for ( const [ hostname, deadline ] of this.hostnameToDeadlineMap ) {
            if ( deadline <= Date.now() ) {
                this.hostnameToDeadlineMap.delete(hostname);
            }
        }
    },

    bypass: function(hostname) {
        if ( typeof hostname !== 'string' || hostname === '' ) { return; }
        this.hostnameToDeadlineMap.set(
            hostname,
            Date.now() + µBlock.hiddenSettings.strictBlockingBypassDuration * 1000
        );
    },

    isBypassed: function(hostname) {
        if ( this.hostnameToDeadlineMap.size === 0 ) { return false; }
        let bypassDuration =
            µBlock.hiddenSettings.strictBlockingBypassDuration * 1000;
        if ( this.cleanupTimer === undefined ) {
            this.cleanupTimer = vAPI.setTimeout(
                ( ) => {
                    this.cleanupTimer = undefined;
                    this.cleanup();
                },
                bypassDuration + 10000
            );
        }
        for (;;) {
            const deadline = this.hostnameToDeadlineMap.get(hostname);
            if ( deadline !== undefined ) {
                if ( deadline > Date.now() ) {
                    this.hostnameToDeadlineMap.set(
                        hostname,
                        Date.now() + bypassDuration
                    );
                    return true;
                }
                this.hostnameToDeadlineMap.delete(hostname);
            }
            const pos = hostname.indexOf('.');
            if ( pos === -1 ) { break; }
            hostname = hostname.slice(pos + 1);
        }
        return false;
    }
};

/******************************************************************************/

return {
    start: (( ) => {
        vAPI.net = new vAPI.Net();
        vAPI.net.suspend(true);

        return function() {
            vAPI.net.setSuspendableListener(onBeforeRequest);
            vAPI.net.addListener(
                'onHeadersReceived',
                adnOnHeadersRecieved,
                {
                    // types: [
                    //     'main_frame',
                    //     'sub_frame',
                    //     'image',
                    //     'media',
                    //     'xmlhttprequest',
                    // ],
                    urls: [ 'http://*/*', 'https://*/*' ],
                },
                navigator.userAgent.includes('Firefox/') ? [ 'blocking', 'responseHeaders'] : ['blocking', 'responseHeaders', 'extraHeaders']// ADN: https://developer.chrome.com/extensions/webRequest
            );
            vAPI.net.addListener(
              'onBeforeSendHeaders',
               onBeforeSendHeaders,
               {
                   'urls': [ '<all_urls>' ],
                   'types': undefined // ADN
               },
               navigator.userAgent.includes('Firefox/') ? [ 'blocking', 'requestHeaders'] : ['blocking', 'requestHeaders', 'extraHeaders'] //ADN
           );
            if ( vAPI.net.validTypes.has('csp_report') ) {
                vAPI.net.addListener(
                    'onBeforeRequest',
                    onBeforeMaybeSpuriousCSPReport,
                    {
                        types: [ 'csp_report' ],
                        urls: [ 'http://*/*', 'https://*/*' ]
                    },
                    [ 'blocking', 'requestBody' ]
                );
            }
            vAPI.net.unsuspend(true);
        };
    })(),

    strictBlockBypass: function(hostname) {
        strictBlockBypasser.bypass(hostname);
    }
};

/******************************************************************************/

})();

/******************************************************************************/
