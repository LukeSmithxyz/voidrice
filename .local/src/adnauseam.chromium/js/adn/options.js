/*******************************************************************************

    AdNauseam - Fight back against advertising surveillance.
    Copyright (C) 2014-2016 Daniel C. Howe

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

    Home: https://github.com/dhowe/AdNauseam
*/

/* global vAPI, uDom */

(function () {

  'use strict';


  /******************************************************************************/

  const handleImportFilePicker = function() {
      const file = this.files[0];
      if ( file === undefined || file.name === '' ) { return; }
      if ( file.type.indexOf('text') !== 0 ) { return; }

      const filename = file.name;

      const fileReaderOnLoadHandler = function() {
          let userData;
          try {
              userData = JSON.parse(this.result);
              if ( typeof userData !== 'object' ) {
                  throw 'Invalid';
              }
              if ( typeof userData.userSettings !== 'object' ) {
                  throw 'Invalid';
              }
              if (
                  Array.isArray(userData.whitelist) === false &&
                  typeof userData.netWhitelist !== 'string'
              ) {
                  throw 'Invalid';
              }
              if (
                  typeof userData.filterLists !== 'object' &&
                  Array.isArray(userData.selectedFilterLists) === false
              ) {
                  throw 'Invalid';
              }
          }
          catch (e) {
              userData = undefined;
          }
          if ( userData === undefined ) {
              window.alert(vAPI.i18n('aboutRestoreDataError').replace(/uBlock₀/g, 'AdNauseam'));
              return;
          }
          const time = new Date(userData.timeStamp);
          const msg = vAPI.i18n('aboutRestoreDataConfirm')
                          .replace('{{time}}', time.toLocaleString());
          const proceed = window.confirm(msg);
          if ( proceed !== true ) { return; }
          vAPI.messaging.send('dashboard', {
              what: 'restoreUserData',
              userData,
              file: filename,
          });
      };

      const fr = new FileReader();
      fr.onload = fileReaderOnLoadHandler;
      fr.readAsText(file);
  };

  /******************************************************************************/

  const startImportFilePicker = function() {
      const input = document.getElementById('restoreFilePicker');
      // Reset to empty string, this will ensure an change event is properly
      // triggered if the user pick a file, even if it is the same as the last
      // one picked.
      input.value = '';
      input.click();
  };

  /******************************************************************************/

  const onLocalDataReceived = function(details) {
      uDom('#localData > ul > li:nth-of-type(1)').text(
          vAPI.i18n('settingsStorageUsed').replace('{{value}}', details.storageUsed.toLocaleString()).replace(/uBlock₀/g, 'AdNauseam')
      );

      const timeOptions = {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: 'numeric',
          minute: 'numeric',
          timeZoneName: 'short'
      };

      const lastBackupFile = details.lastBackupFile || '';
      if ( lastBackupFile !== '' ) {
          const dt = new Date(details.lastBackupTime);
          uDom('#localData > ul > li:nth-of-type(2) > ul > li:nth-of-type(1)').text(dt.toLocaleString('fullwide', timeOptions));
          //uDom('#localData > ul > li:nth-of-type(2) > ul > li:nth-of-type(2)').text(lastBackupFile);
          uDom('#localData > ul > li:nth-of-type(2)').css('display', '');
      }

      const lastRestoreFile = details.lastRestoreFile || '';
      uDom('#localData > p:nth-of-type(3)');
      if ( lastRestoreFile !== '' ) {
          const dt = new Date(details.lastRestoreTime);
          uDom('#localData > ul > li:nth-of-type(3) > ul > li:nth-of-type(1)').text(dt.toLocaleString('fullwide', timeOptions));
          uDom('#localData > ul > li:nth-of-type(3) > ul > li:nth-of-type(2)').text(lastRestoreFile);
          uDom('#localData > ul > li:nth-of-type(3)').css('display', '');
      }

      if ( details.cloudStorageSupported === false ) {
          uDom('#cloud-storage-enabled').attr('disabled', '');
      }

      if ( details.privacySettingsSupported === false ) {
          uDom('#prefetching-disabled').attr('disabled', '');
          uDom('#hyperlink-auditing-disabled').attr('disabled', '');
          uDom('#webrtc-ipaddress-hidden').attr('disabled', '');
      }
  };

  /******************************************************************************/

  const resetUserData = function() {
      const msg = vAPI.i18n('adnAboutResetDataConfirm'); // ADN
      const proceed = window.confirm(msg); // ADN: changed from vAPI.confirm merge1.14.12
      if ( proceed ) {
          vAPI.messaging.send('dashboard', { what: 'resetUserData' });
      }
  };

  /******************************************************************************/

  const synchronizeDOM = function() {
      document.body.classList.toggle(
          'advancedUser',
          uDom.nodeFromId('advanced-user-enabled').checked === true
      );
  };

  /******************************************************************************/

  const changeUserSettings = function(name, value) {
    Promise.all([
        vAPI.messaging.send('dashboard', {
            what: 'userSettings',
            name,
            value,
        }),
    ]).then(() => {
        updateGroupState();
    });

  };

  /******************************************************************************/
  // ADN
  const ClickProbabilityChanged = function() {
      const selection = uDom('input[id="slider"]');
      const slideVal = selection.nodes[0].value;

      selection.val(slideVal);
      vAPI.messaging.send('dashboard', {
          what: 'userSettings',
          name: 'clickProbability',
          value: Number(slideVal)
      })

  };

  /******************************************************************************/

  const onInputChanged = function(ev) {
      const input = ev.target;
      const name = this.getAttribute('data-setting-name');
      let value = input.value;
      if ( name === 'largeMediaSize' ) {
          value = Math.min(Math.max(Math.floor(parseInt(value, 10) || 0), 0), 1000000);
      }
      if ( value !== input.value ) {
          input.value = value;
      }
      changeUserSettings(name, value);
  };
  /******************************************************************************/

  // Workaround for:
  // https://github.com/gorhill/uBlock/issues/1448

  const onPreventDefault = function(ev) {
      ev.target.focus();
      ev.preventDefault();
  };
  /******************************************************************************/

  // if any of 3 main toggles are off, disabled their subgroups
  const updateGroupState = function () {

    uDom('.hidingAds-child').prop('disabled', !uDom('#hidingAds').prop('checked'));
    uDom('.clickingAds-child').prop('disabled', !uDom('#clickingAds').prop('checked'));
    uDom('.blockingMalware-child').prop('disabled', !uDom('#blockingMalware').prop('checked'));
  }

   /******************************************************************************/

    const exportDialog = function() {
       uDom('#export-dialog').removeClass("hide");
     };

    const exportTo = function() {
        const action = uDom('#export-dialog input:checked').nodes[0].id;
        exportToFile(action)
        closeDialog();
    };

    const closeDialog = function() {
       uDom('#export-dialog').addClass("hide");
    }



  /******************************************************************************/

  // TODO: use data-* to declare simple settings

  const onUserSettingsReceived = function (details) {

    // console.log('onUserSettingsReceived', details);

    if (isMobile()) { // ADN
      uDom('.dntOption').css('display', 'none');
    }

    uDom('input[type="range"]').on('change', ClickProbabilityChanged); //ADN

    uDom('[data-setting-type="bool"]').forEach(function(uNode) {
        uNode.prop('checked', details[uNode.attr('data-setting-name')] === true)
             .on('change', function() {
                    changeUserSettings(
                        this.getAttribute('data-setting-name'),
                        this.checked
                    );
                    synchronizeDOM();
                });
    });

    uDom('[data-setting-name="noLargeMedia"] ~ label:first-of-type > input[type="number"]')
        .attr('data-setting-name', 'largeMediaSize')
        .attr('data-setting-type', 'input');

    uDom('[data-setting-type="input"]').forEach(function(uNode) {
        uNode.val(details[uNode.attr('data-setting-name')])
             .on('change', onInputChanged)
             .on('click', onPreventDefault);
    });

    // Minor text fixes
    if (uDom('#exportDialog').text() === "Back up to file")
      uDom('#exportDialog').text("Backup to file");
    uDom('#import').text(uDom('#import').text().replace('...',''));
    uDom('#resetOptions').text(uDom('#resetOptions').text().replace('...',''));

    // On click events
    uDom('#reset').on('click', clearAds);
    uDom('#exportDialog').on('click', exportDialog);
    uDom('#export').on('click', exportTo);
    uDom('#import').on('click', startImportFilePicker);
    uDom('#importFilePicker').on('change', handleImportFilePicker);
    uDom('#resetOptions').on('click', resetUserData);
    uDom('#export-dialog .close').on('click', closeDialog);
    uDom('#confirm-close').on('click', function (e) {
      e.preventDefault();
      window.open(location, '_self').close();
    });

    updateGroupState();
  };

  /******************************************************************************/

  Promise.all([
      vAPI.messaging.send('dashboard', { what: 'userSettings' }),
      vAPI.messaging.send('dashboard', { what: 'getLocalData' }),
  ]).then(results => {
      onUserSettingsReceived(results[0]);
      onLocalDataReceived(results[1]);
  });

  // https://github.com/uBlockOrigin/uBlock-issues/issues/591
  document.querySelector(
      '[data-i18n-title="settingsAdvancedUserSettings"]'
  ).addEventListener(
      'click',
      self.uBlockDashboard.openOrSelectPage
  );
  /******************************************************************************/

})();
