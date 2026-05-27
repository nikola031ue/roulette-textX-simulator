const { LanguageClient, TransportKind } = require('vscode-languageclient/node');
const vscode = require('vscode');
const path = require('path');

let client;

function activate(context) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Roul LSP: No workspace folder open.');
        return;
    }

    const serverScript = path.join(workspaceFolder, 'language_server.py');
    const pythonPath = vscode.workspace
        .getConfiguration('python')
        .get('defaultInterpreterPath') || 'python';

    const serverOptions = {
        command: pythonPath,
        args: [serverScript],
        transport: TransportKind.stdio,
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'roul' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.roul'),
        },
    };

    client = new LanguageClient(
        'roulLanguageServer',
        'Roul Language Server',
        serverOptions,
        clientOptions,
    );

    client.start();
}

function deactivate() {
    if (client) return client.stop();
}

module.exports = { activate, deactivate };
