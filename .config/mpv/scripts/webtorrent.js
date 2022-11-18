"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
var webTorrentRunning = false;
var active = false;
var initialyActive = false;
var overlayText = '';
var playlist = [];
// Sync with options in webtorrent.node.ts
var options = {
    path: './',
    maxConns: 100,
    port: 8888,
    utp: false,
    dht: true,
    // Text style. from stats.lua
    font: 'sans',
    font_mono: 'monospace',
    font_size: 8,
    font_color: 'FFFFFF',
    border_size: 0.8,
    border_color: '262626',
    shadow_x_offset: 0.0,
    shadow_y_offset: 0.0,
    shadow_color: '000000',
    alpha: '11',
    // Node
    node_path: 'node'
};
mp.options.read_options(options, 'stats');
mp.options.read_options(options);
options.path = mp.command_native(['expand-path', options.path]);
function keyPressHandler() {
    if (active || initialyActive) {
        clearOverlay();
    }
    else {
        showOverlay();
    }
}
function showOverlay() {
    initialyActive = false;
    active = true;
    printOverlay();
}
function printOverlay() {
    if (!overlayText) {
        return;
    }
    if (active || initialyActive) {
        var expanded = mp.command_native(['expand-text', overlayText]);
        mp.osd_message(expanded, 10);
    }
}
function clearOverlay() {
    active = false;
    initialyActive = false;
    mp.osd_message('', 0);
}
function openPlaylist() {
    for (var i = 0; i < playlist.length; i++) {
        var item = playlist[i];
        if (!item) {
            continue;
        }
        if (i === 0) {
            mp.commandv('loadfile', item);
        }
        else {
            mp.commandv('loadfile', item, 'append');
        }
    }
}
function onData(_data) {
    overlayText = _data;
    printOverlay();
}
function onPlaylist(_playlist) {
    playlist = JSON.parse(_playlist);
    openPlaylist();
}
function onInfo() {
    var _a;
    var _info = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        _info[_i] = arguments[_i];
    }
    (_a = mp.msg).info.apply(_a, __spreadArray([], __read(_info), false));
}
function onFileLoaded() {
    initialyActive = false;
    if (!active) {
        clearOverlay();
    }
}
function onIdleActiveChange(name, idleActive) {
    if (idleActive && playlist.length) {
        mp.set_property('pause', 'yes');
        setTimeout(openPlaylist, 1000);
    }
}
function onLoadHook() {
    var url = mp.get_property('stream-open-filename', '');
    try {
        if (/^magnet:/i.test(url)) {
            runHook(url);
        }
        else if (/\.torrent$/i.test(url)) {
            runHook(url);
        }
        else if (/^[0-9A-F]{40}$/i.test(url)) {
            runHook(url);
        }
        else if (/^[0-9A-Z]{32}$/i.test(url)) {
            runHook(url);
        }
    }
    catch (_e) {
        var e = _e;
        mp.msg.error(e.message);
    }
}
function runHook(url) {
    mp.msg.info('Running WebTorrent hook');
    mp.set_property('stream-open-filename', 'null://');
    if (webTorrentRunning) {
        throw new Error('WebTorrent already running. Only one instance is allowed.');
    }
    var socketName = getSocketName();
    var scriptPath = getNodeScriptPath();
    webTorrentRunning = true;
    initialyActive = true;
    mp.set_property('idle', 'yes');
    mp.set_property('force-window', 'yes');
    mp.set_property('keep-open', 'yes');
    mp.register_script_message('osd-data', onData);
    mp.register_script_message('playlist', onPlaylist);
    mp.register_script_message('info', onInfo);
    mp.register_event('file-loaded', onFileLoaded);
    mp.observe_property('idle-active', 'bool', onIdleActiveChange);
    var args = __assign({ torrentId: url, socketName: socketName }, options);
    mp.command_native_async({
        name: 'subprocess',
        args: [options.node_path, scriptPath, JSON.stringify(args)],
        playback_only: false,
        capture_stderr: true
    }, onWebTorrentExit);
    mp.add_key_binding('p', 'toggle-info', keyPressHandler);
}
function getSocketName() {
    var socketName = mp.get_property('input-ipc-server');
    if (!socketName) {
        mp.set_property('input-ipc-server', "/tmp/webtorrent-mpv-hook-socket-".concat(mp.utils.getpid(), "-").concat(Date.now()));
        socketName = mp.get_property('input-ipc-server');
    }
    if (!socketName) {
        throw new Error("Couldn't get input-ipc-server");
    }
    return socketName;
}
function getNodeScriptPath() {
    var _a, _b;
    var realPath = mp.command_native({
        name: 'subprocess',
        args: [options.node_path, '-p', "require('fs').realpathSync('".concat(mp.get_script_file().replace(/\\/g, '\\\\'), "')")],
        playback_only: false,
        capture_stdout: true
    });
    try {
        var scriptPath = (_b = (_a = realPath.stdout.split(/\r\n|\r|\n/)) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.replace(/webtorrent\.js$/, 'webtorrent.node.js');
        if (!scriptPath) {
            throw new Error();
        }
        return scriptPath;
    }
    catch (e) {
        throw new Error("Failed to get node script path. Possible causes are \"".concat(options.node_path, "\" not available in path or incorrect symlink."));
    }
}
function onWebTorrentExit(success, _result) {
    webTorrentRunning = false;
    overlayText = '';
    clearOverlay();
    var result = _result;
    if (!success) {
        mp.msg.error('Failed to start WebTorrent');
    }
    else if (result.stderr) {
        mp.msg.error(result.stderr);
    }
    else if (result.status) {
        mp.msg.error('WebTorrent exited with error');
    }
    mp.unregister_script_message('osd-data');
    mp.unregister_script_message('playlist');
    mp.unregister_script_message('info');
    mp.unregister_event(onFileLoaded);
    mp.unobserve_property(onIdleActiveChange);
    mp.remove_key_binding('toggle-info');
}
mp.add_hook('on_load', 50, onLoadHook);
