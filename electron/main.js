const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let backendProcess = null;
let mainWindow = null;

const BACKEND_PORT = 8001;
const BACKEND_HEALTH_URL = `http://127.0.0.1:${BACKEND_PORT}/api/`;

function startBackend() {
  const isDev = !app.isPackaged;
  const backendDir = isDev
    ? path.join(__dirname, '..', 'backend')
    : path.join(process.resourcesPath, 'backend');

  // Python must be installed on user's system; or use PyInstaller one-file exe
  backendProcess = spawn(
    'python',
    ['-m', 'uvicorn', 'server:app', '--host', '127.0.0.1', '--port', String(BACKEND_PORT)],
    { cwd: backendDir, shell: true }
  );

  backendProcess.stdout.on('data', d => console.log(`[backend] ${d}`));
  backendProcess.stderr.on('data', d => console.error(`[backend] ${d}`));
  backendProcess.on('close', code => console.log(`[backend] exited ${code}`));
}

function waitForBackend(cb, retries = 60) {
  const req = http.get(BACKEND_HEALTH_URL, res => {
    if (res.statusCode === 200) return cb();
    retry();
  });
  req.on('error', retry);

  function retry() {
    if (retries <= 0) return cb(new Error('Backend not ready'));
    setTimeout(() => waitForBackend(cb, retries - 1), 500);
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    backgroundColor: '#0A0A0A',
    title: 'Optidriver',
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    autoHideMenuBar: true,
  });

  const isDev = !app.isPackaged;
  const frontendUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '..', 'frontend', 'build', 'index.html')}`;

  mainWindow.loadURL(frontendUrl);

  // Open external links in default browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(() => {
  startBackend();
  waitForBackend(err => {
    if (err) console.error('Backend failed to start:', err);
    createWindow();
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (backendProcess) backendProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  if (backendProcess) backendProcess.kill();
});
