const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('optidriver', {
  version: '1.0.0',
  platform: process.platform,
  isElectron: true,
});
