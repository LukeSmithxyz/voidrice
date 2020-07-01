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

/* global CodeMirror, uDom */

'use strict';

/******************************************************************************/

self.uBlockDashboard = self.uBlockDashboard || {};

/******************************************************************************/

// Helper for client panes:
//   Remove literal duplicate lines from a set based on another set.

self.uBlockDashboard.mergeNewLines = function(text, newText) {
    // Step 1: build dictionary for existing lines.
    const fromDict = new Map();
    let lineBeg = 0;
    let textEnd = text.length;
    while ( lineBeg < textEnd ) {
        let lineEnd = text.indexOf('\n', lineBeg);
        if ( lineEnd === -1 ) {
            lineEnd = text.indexOf('\r', lineBeg);
            if ( lineEnd === -1 ) {
                lineEnd = textEnd;
            }
        }
        const line = text.slice(lineBeg, lineEnd).trim();
        lineBeg = lineEnd + 1;
        if ( line.length === 0 ) { continue; }
        const hash = line.slice(0, 8);
        const bucket = fromDict.get(hash);
        if ( bucket === undefined ) {
            fromDict.set(hash, line);
        } else if ( typeof bucket === 'string' ) {
            fromDict.set(hash, [ bucket, line ]);
        } else /* if ( Array.isArray(bucket) ) */ {
            bucket.push(line);
        }
    }

    // Step 2: use above dictionary to filter out duplicate lines.
    const out = [ '' ];
    lineBeg = 0;
    textEnd = newText.length;
    while ( lineBeg < textEnd ) {
        let lineEnd = newText.indexOf('\n', lineBeg);
        if ( lineEnd === -1 ) {
            lineEnd = newText.indexOf('\r', lineBeg);
            if ( lineEnd === -1 ) {
                lineEnd = textEnd;
            }
        }
        const line = newText.slice(lineBeg, lineEnd).trim();
        lineBeg = lineEnd + 1;
        if ( line.length === 0 ) {
            if ( out[out.length - 1] !== '' ) {
                out.push('');
            }
            continue;
        }
        const bucket = fromDict.get(line.slice(0, 8));
        if ( bucket === undefined ) {
            out.push(line);
            continue;
        }
        if ( typeof bucket === 'string' && line !== bucket ) {
            out.push(line);
            continue;
        }
        if ( bucket.indexOf(line) === -1 ) {
            out.push(line);
            /* continue; */
        }
    }

    const append = out.join('\n').trim();
    if ( text !== '' && append !== '' ) {
        text += '\n\n';
    }
    return text + append;
};

/******************************************************************************/

self.uBlockDashboard.dateNowToSensibleString = function() {
    const now = new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000);
    return now.toISOString().replace(/\.\d+Z$/, '')
                            .replace(/:/g, '.')
                            .replace('T', '_');
};

/******************************************************************************/

self.uBlockDashboard.patchCodeMirrorEditor = (function() {
    let grabFocusTimer;
    let grabFocusTarget;

    const grabFocus = function() {
        grabFocusTarget.focus();
        grabFocusTimer = grabFocusTarget = undefined;
    };
    const grabFocusAsync = function(cm) {
        grabFocusTarget = cm;
        if ( grabFocusTimer === undefined ) {
            grabFocusTimer = vAPI.setTimeout(grabFocus, 1);
        }
    };

    // https://github.com/gorhill/uBlock/issues/3646
    const patchSelectAll = function(cm, details) {
        var vp = cm.getViewport();
        if ( details.ranges.length !== 1 ) { return; }
        var range = details.ranges[0],
            lineFrom = range.anchor.line,
            lineTo = range.head.line;
        if ( lineTo === lineFrom ) { return; }
        if ( range.head.ch !== 0 ) { lineTo += 1; }
        if ( lineFrom !== vp.from || lineTo !== vp.to ) { return; }
        details.update([
            {
                anchor: { line: 0, ch: 0 },
                head: { line: cm.lineCount(), ch: 0 }
            }
        ]);
        grabFocusAsync(cm);
    };

    let lastGutterClick = 0;
    let lastGutterLine = 0;

    const onGutterClicked = function(cm, line) {
        const delta = Date.now() - lastGutterClick;
        if ( delta >= 500 || line !== lastGutterLine ) {
            cm.setSelection(
                { line: line, ch: 0 },
                { line: line + 1, ch: 0 }
            );
            lastGutterClick = Date.now();
            lastGutterLine = line;
        } else {
            cm.setSelection(
                { line: 0, ch: 0 },
                { line: cm.lineCount(), ch: 0 },
                { scroll: false }
            );
            lastGutterClick = 0;
        }
        grabFocusAsync(cm);
    };

    let resizeTimer,
        resizeObserver;
    const resize = function(cm) {
        resizeTimer = undefined;
        const child = document.querySelector('.codeMirrorFillVertical');
        if ( child === null ) { return; }
        const prect = document.documentElement.getBoundingClientRect();
        const crect = child.getBoundingClientRect();
        const cssHeight = Math.floor(Math.max(prect.bottom - crect.top, 80)) + 'px';
        if ( child.style.height === cssHeight ) { return; }
        child.style.height = cssHeight;
        // https://github.com/gorhill/uBlock/issues/3694
        //   Need to call cm.refresh() when resizing occurs. However the
        //   cursor position may end up outside the viewport, hence we also
        //   call cm.scrollIntoView() to address this.
        //   Reference: https://codemirror.net/doc/manual.html#api_sizing
        if ( cm instanceof CodeMirror ) {
            cm.refresh();
            cm.scrollIntoView(null);
        }
    };
    const resizeAsync = function(cm, delay) {
        if ( resizeTimer !== undefined ) { return; }
        resizeTimer = vAPI.setTimeout(
            resize.bind(null, cm),
            typeof delay === 'number' ? delay : 66
        );
    };

    return function(cm) {
        if ( document.querySelector('.codeMirrorFillVertical') !== null ) {
            const boundResizeAsync = resizeAsync.bind(null, cm);
            window.addEventListener('resize', boundResizeAsync);
            resizeObserver = new MutationObserver(boundResizeAsync);
            resizeObserver.observe(document.querySelector('.body'), {
                childList: true,
                subtree: true
            });
            resizeAsync(cm, 1);
        }
        if ( cm.options.inputStyle === 'contenteditable' ) {
            cm.on('beforeSelectionChange', patchSelectAll);
        }
        cm.on('gutterClick', onGutterClicked);
    };
})();

/******************************************************************************/

self.uBlockDashboard.openOrSelectPage = function(url, options = {}) {
    let ev;
    if ( url instanceof MouseEvent ) {
        ev = url;
        url = ev.target.getAttribute('href');
    } 
    const details = Object.assign({ url, select: true, index: -1 }, options);
    vAPI.messaging.send('default', {
        what: 'gotoURL',
        details,
    });
    if ( ev ) {
        ev.preventDefault();
    }
};

/******************************************************************************/

// Open links in the proper window
uDom('a').attr('target', '_blank');
uDom('a[href*="dashboard.html"]').attr('target', '_parent');
uDom('.whatisthis').on('click', function() {
    uDom(this)
        .parent()
        .descendants('.whatisthis-expandable')
        .first()
        .toggleClass('whatisthis-expanded');
});
