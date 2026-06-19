from flask import Flask, render_template, request, jsonify
import json
from solution_finder import SolutionFinder

app = Flask(__name__)

# Solution Finderインスタンス
finder = SolutionFinder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    盤面データを受け取り、Solution Finderで分析
    """
    try:
        data = request.json
        board = data.get('board')
        
        if not board or len(board) != 200:
            return jsonify({'error': '無効な盤面データです'}), 400
        
        # 盤面を2次元配列に変換
        grid = []
        for i in range(20):
            row = []
            for j in range(10):
                row.append(int(board[i * 10 + j]))
            grid.append(row)
        
        # 分析実行
        results = finder.analyze(grid)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns', methods=['POST'])
def get_patterns():
    """
    パフェパターンを取得
    """
    try:
        data = request.json
        board = data.get('board')
        
        if not board or len(board) != 200:
            return jsonify({'error': '無効な盤面データです'}), 400
        
        # 盤面を2次元配列に変換
        grid = []
        for i in range(20):
            row = []
            for j in range(10):
                row.append(int(board[i * 10 + j]))
            grid.append(row)
        
        # パターン取得
        patterns = finder.get_patterns(grid)
        
        return jsonify({'patterns': patterns})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')