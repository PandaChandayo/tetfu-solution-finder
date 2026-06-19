"""
Solution Finder: テトリスのパフェ分析エンジン
"""

from itertools import permutations
from typing import List, Dict, Tuple

class SolutionFinder:
    """
    テトリス盤面のパフェ率、セットアップ率、パフェパターンを計算
    """
    
    # テトリミノ形状定義（相対座標）
    TETRIMINOS = {
        'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
        'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
        'T': [(0, 0), (1, 0), (2, 0), (1, 1)],
        'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
        'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
        'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
        'L': [(2, 0), (0, 1), (1, 1), (2, 1)],
    }
    
    def __init__(self):
        self.board_width = 10
        self.board_height = 20
    
    def analyze(self, board: List[List[int]]) -> Dict:
        """
        盤面を分析してセットアップ率、パフェ率を計算
        
        Args:
            board: 2次元のボード配列 (20行 x 10列)
        
        Returns:
            分析結果��辞書
        """
        setup_rate = self._calculate_setup_rate(board)
        parfe_rate = self._calculate_parfe_rate(board)
        
        return {
            'setup_rate': setup_rate,
            'parfe_rate': parfe_rate,
            'board': board
        }
    
    def _calculate_setup_rate(self, board: List[List[int]]) -> float:
        """
        セットアップ率を計算（盤面の埋まり具合から推定）
        
        Args:
            board: ボード配列
        
        Returns:
            セットアップ率（0-100%）
        """
        total_cells = self.board_height * self.board_width
        filled_cells = sum(sum(row) for row in board)
        
        # 埋まったセルの割合がセットアップ率の一つの指標
        rate = (filled_cells / total_cells) * 100
        return round(rate, 1)
    
    def _calculate_parfe_rate(self, board: List[List[int]]) -> float:
        """
        パフェ率を計算（現在の盤面でパフェ可能な確率）
        
        Args:
            board: ボード配列
        
        Returns:
            パフェ率（0-100%）
        """
        # 簡易実装：盤面の高さが均一ほどパフェ率が高い
        heights = self._get_column_heights(board)
        
        if not heights:
            return 0.0
        
        max_height = max(heights)
        min_height = min(heights)
        
        # 高さの差が小さいほどパフェ率が高い
        diff = max_height - min_height
        parfe_rate = max(0, 100 - (diff * 5))
        
        return round(parfe_rate, 1)
    
    def _get_column_heights(self, board: List[List[int]]) -> List[int]:
        """
        各列の高さを計算
        
        Args:
            board: ボード配列
        
        Returns:
            各列の高さのリスト
        """
        heights = []
        
        for x in range(self.board_width):
            height = 0
            for y in range(self.board_height - 1, -1, -1):
                if board[y][x] == 1:
                    height = self.board_height - y
                    break
            heights.append(height)
        
        return heights
    
    def get_patterns(self, board: List[List[int]]) -> List[Dict]:
        """
        パフェ可能なパターンを取得
        
        Args:
            board: ボード配列
        
        Returns:
            パターンのリスト
        """
        patterns = []
        
        # 簡易実装：テトリミノの配置パターンを生成
        heights = self._get_column_heights(board)
        
        for i, height in enumerate(heights):
            pattern = {
                'column': i,
                'height': height,
                'potential': 100 - (height * 2)  # 簡易スコア
            }
            patterns.append(pattern)
        
        # ポテンシャルでソート
        patterns.sort(key=lambda x: x['potential'], reverse=True)
        
        return patterns[:5]  # 上位5パターン返す
    
    def is_parfe_possible(self, board: List[List[int]]) -> bool:
        """
        現在の盤面がパフェ可能かどうかを判定
        
        Args:
            board: ボード配列
        
        Returns:
            パフェ可能ならTrue
        """
        heights = self._get_column_heights(board)
        
        # 全ての列が同じ高さ、またはほぼ同じならパフェ可能
        if not heights:
            return False
        
        max_height = max(heights)
        min_height = min(heights)
        
        return (max_height - min_height) <= 2
    
    def find_optimal_setup(self, board: List[List[int]]) -> List[Dict]:
        """
        最適なセットアップパターンを提案
        
        Args:
            board: ボード配列
        
        Returns:
            セットアップ提案のリスト
        """
        suggestions = []
        heights = self._get_column_heights(board)
        max_height = max(heights) if heights else 0
        
        # 低い列を高くする提案
        for i, height in enumerate(heights):
            if height < max_height - 2:
                suggestions.append({
                    'column': i,
                    'action': 'build_up',
                    'priority': max_height - height
                })
        
        # 優先度でソート
        suggestions.sort(key=lambda x: x['priority'], reverse=True)
        
        return suggestions