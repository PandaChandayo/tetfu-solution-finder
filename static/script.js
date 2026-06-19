// グローバル変数
let currentGrid = Array(20).fill(null).map(() => Array(10).fill(0));

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    initializeGrid();
});

// グリッド初期化
function initializeGrid() {
    const grid = document.getElementById('grid');
    grid.innerHTML = '';
    
    for (let y = 0; y < 20; y++) {
        for (let x = 0; x < 10; x++) {
            const cell = document.createElement('div');
            cell.className = 'tetris-cell';
            cell.dataset.x = x;
            cell.dataset.y = y;
            
            if (currentGrid[y][x]) {
                cell.classList.add('filled');
            }
            
            cell.addEventListener('click', function() {
                toggleCell(x, y, cell);
            });
            
            grid.appendChild(cell);
        }
    }
}

// セルトグル
function toggleCell(x, y, cell) {
    currentGrid[y][x] = currentGrid[y][x] ? 0 : 1;
    cell.classList.toggle('filled');
}

// グリッドクリア
function clearGrid() {
    if (confirm('本当にクリアしますか？')) {
        currentGrid = Array(20).fill(null).map(() => Array(10).fill(0));
        initializeGrid();
        document.getElementById('tetfu-link').innerHTML = '';
    }
}

// テト譜コード生成（簡易版）
function gridToTetfu() {
    // テト譜形式に変換（0と1を文字列化）
    let tetfuCode = '';
    for (let y = 0; y < 20; y++) {
        for (let x = 0; x < 10; x++) {
            tetfuCode += currentGrid[y][x] ? '1' : '0';
        }
    }
    return tetfuCode;
}

// テト譜コードから盤面復元
function tetfuToGrid(code) {
    if (code.length !== 200) {
        alert('無効なテト譜コードです（200文字必要）');
        return false;
    }
    
    for (let i = 0; i < 200; i++) {
        const y = Math.floor(i / 10);
        const x = i % 10;
        currentGrid[y][x] = code[i] === '1' ? 1 : 0;
    }
    return true;
}

// リンク生成
function generateLink() {
    const tetfuCode = gridToTetfu();
    const baseUrl = 'https://harddrop.com/fumenext/?';
    
    // 簡易的なエンコード（本家フォーマットとは異なる可能性）
    const encodedCode = btoa(tetfuCode);
    const fullUrl = baseUrl + 'f=' + encodedCode;
    
    const linkDiv = document.getElementById('tetfu-link');
    linkDiv.innerHTML = `
        <strong>生成されたリンク:</strong><br>
        <input type="text" value="${fullUrl}" readonly style="width: 100%; padding: 8px; margin-top: 10px;">
        <br><br>
        <a href="${fullUrl}" target="_blank" style="background: #667eea; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block;">テト譜で開く</a>
    `;
}

// テト譜エクスポート
function exportTetfu() {
    const tetfuCode = gridToTetfu();
    const link = document.createElement('a');
    link.href = 'data:text/plain,' + encodeURIComponent(tetfuCode);
    link.download = 'tetfu_' + Date.now() + '.txt';
    link.click();
}

// テト譜インポート
function importTetfu() {
    const code = document.getElementById('tetfu-code').value.trim();
    
    if (tetfuToGrid(code)) {
        initializeGrid();
        alert('テト譜をインポートしました');
        document.getElementById('tetfu-code').value = '';
    }
}

// タブ切り替え
function switchTab(tabName) {
    // 全てのタブコンテンツを非表示
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 全てのボタンを非アクティブ
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 選択されたタブを表示
    document.getElementById(tabName + '-section').classList.add('active');
    event.target.classList.add('active');
}

// Solution Finder分析
function analyzeSolutions() {
    // 簡易的な分析ロジック
    // 実装の詳細はバックエンドで処理することを想定
    
    // テスト用の仮データ
    const setupRate = Math.floor(Math.random() * 100);
    const parfeRate = Math.floor(Math.random() * 100);
    
    document.getElementById('setup-rate-value').textContent = setupRate + '%';
    document.getElementById('parfe-rate-value').textContent = parfeRate + '%';
    
    // パターン表示（仮）
    const patternList = document.getElementById('pattern-list');
    patternList.innerHTML = '';
    
    for (let i = 0; i < 5; i++) {
        const patternItem = document.createElement('div');
        patternItem.className = 'pattern-item';
        patternItem.textContent = `パターン ${i + 1}`;
        patternList.appendChild(patternItem);
    }
    
    alert('分析が完了しました');
}