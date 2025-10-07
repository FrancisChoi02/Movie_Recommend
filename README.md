"""
智能重叠策略 vs 滑动窗口策略对比示例
直观展示两种策略的工作原理和效果差异
"""

import re
from typing import List, Tuple
from dataclasses import dataclass

def chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
    """Split text into smaller chunks for embedding and clean problematic characters."""
    text = "".join(c for c in text if c.isprintable()).strip()
    text = " ".join(text.split())

    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1
        if current_length > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print(f"Created {len(chunks)} chunks")
    return chunks


def overlapping_chunking(text: str, chunk_size: int = 500, overlap_size: int = 100) -> List[str]:
    """重叠分块策略，保持上下文连续性"""
    words = text.split()
    chunks = []
    
    # 计算每块的词数
    words_per_chunk = chunk_size // 6  # 假设平均每词6字符
    overlap_words = overlap_size // 6
    
    start = 0
    while start < len(words):
        end = min(start + words_per_chunk, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        
        # 下一块的起始位置考虑重叠
        start = end - overlap_words
        if start >= len(words):
            break
    
    return chunks


def sliding_window_chunking(text: str, window_size: int = 500, step_size: int = 250) -> List[str]:
    """滑动窗口分块，确保信息不丢失"""
    chunks = []
    text_length = len(text)
    
    start = 0
    while start < text_length:
        end = min(start + window_size, text_length)
        
        # 尝试在句子边界结束
        if end < text_length:
            # 向后查找句子结束符
            for i in range(end, min(end + 50, text_length)):
                if text[i] in '.!?':
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start += step_size
    
    return chunks

def smart_overlap_chunking(text: str, target_size: int = 500, overlap_ratio: float = 0.2) -> List[str]:
    """智能重叠：在语义边界处重叠"""
    sentences = re.split(r'[.!?]+\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    overlap_size = int(target_size * overlap_ratio)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_length = len(sentence)
        
        if current_length + sentence_length > target_size and current_chunk:
            # 创建当前块
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            
            # 计算重叠内容
            overlap_text = chunk_text[-overlap_size:] if len(chunk_text) > overlap_size else chunk_text
            
            # 开始新块，包含重叠内容
            current_chunk = [overlap_text, sentence]
            current_length = len(overlap_text) + sentence_length + 1
        else:
            current_chunk.append(sentence)
            current_length += sentence_length + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks



@dataclass
class ChunkResult:
    """分块结果"""
    content: str
    start_pos: int
    end_pos: int
    overlap_info: str = ""


class SlidingWindowChunker:
    """滑动窗口分块器"""
    
    def chunk(self, text: str, window_size: int = 100, step_size: int = 50) -> List[ChunkResult]:
        """滑动窗口分块：固定大小，机械式移动"""
        chunks = []
        text_length = len(text)
        
        start = 0
        chunk_index = 0
        
        while start < text_length:
            end = min(start + window_size, text_length)
            chunk_content = text[start:end]
            
            # 计算重叠信息
            overlap_info = ""
            if chunk_index > 0:
                overlap_start = max(0, start - step_size)
                overlap_end = start
                if overlap_start < overlap_end:
                    overlap_info = f"与前一块重叠: {overlap_end - overlap_start} 字符"
            
            chunk = ChunkResult(
                content=chunk_content,
                start_pos=start,
                end_pos=end,
                overlap_info=overlap_info
            )
            
            chunks.append(chunk)
            start += step_size
            chunk_index += 1
            
            if start >= text_length:
                break
        
        return chunks


class SmartOverlapChunker:
    """智能重叠分块器"""
    
    def chunk(self, text: str, target_size: int = 100, overlap_ratio: float = 0.3) -> List[ChunkResult]:
        """智能重叠分块：语义边界，智能重叠"""
        sentences = self._split_sentences(text)
        chunks = []
        current_chunk_sentences = []
        current_length = 0
        
        overlap_size = int(target_size * overlap_ratio)
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # 检查是否需要开始新块
            if current_length + sentence_length > target_size and current_chunk_sentences:
                # 创建当前块
                chunk_content = ''.join(current_chunk_sentences)
                
                # 计算智能重叠内容
                overlap_content = self._get_smart_overlap(chunk_content, overlap_size)
                overlap_sentences = self._split_sentences(overlap_content)
                
                chunk = ChunkResult(
                    content=chunk_content,
                    start_pos=0,  # 简化位置计算
                    end_pos=len(chunk_content),
                    overlap_info=f"智能重叠: {len(overlap_sentences)} 个完整句子"
                )
                chunks.append(chunk)
                
                # 开始新块，包含重叠内容
                current_chunk_sentences = overlap_sentences + [sentence]
                current_length = len(''.join(current_chunk_sentences))
            else:
                current_chunk_sentences.append(sentence)
                current_length += sentence_length
        
        # 处理最后一个块
        if current_chunk_sentences:
            chunk_content = ''.join(current_chunk_sentences)
            chunk = ChunkResult(
                content=chunk_content,
                start_pos=0,
                end_pos=len(chunk_content),
                overlap_info="最后一块"
            )
            chunks.append(chunk)
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """按句子分割，保持标点符号"""
        # 改进的句子分割，保持完整性
        sentences = re.split(r'([.!?。！？]+)', text)
        result = []
        
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                sentence = sentences[i] + sentences[i + 1]
                if sentence.strip():
                    result.append(sentence)
        
        return result
    
    def _get_smart_overlap(self, content: str, overlap_size: int) -> str:
        """获取智能重叠内容：选择完整的句子"""
        if len(content) <= overlap_size:
            return content
        
        # 从末尾开始，找到完整的句子作为重叠内容
        sentences = self._split_sentences(content)
        overlap_sentences = []
        current_length = 0
        
        # 从后往前选择句子
        for sentence in reversed(sentences):
            if current_length + len(sentence) <= overlap_size:
                overlap_sentences.insert(0, sentence)
                current_length += len(sentence)
            else:
                break
        
        return ''.join(overlap_sentences) if overlap_sentences else content[-overlap_size:]


def compare_strategies():
    """对比两种策略的效果"""
    
    # 测试文本
    sample_text = """
    人工智能是计算机科学的一个重要分支。它致力于创建能够模拟人类智能的系统。
    机器学习是人工智能的核心技术之一。它使计算机能够从数据中学习和改进。
    深度学习是机器学习的一个子集。它使用神经网络来处理复杂的数据模式。
    自然语言处理专注于计算机与人类语言的交互。它包括文本分析和语言生成等任务。
    """.strip()
    
    print("=" * 60)
    print("📊 智能重叠策略 vs 滑动窗口策略对比")
    print("=" * 60)
    print(f"\n📝 原始文本 ({len(sample_text)} 字符):")
    print(f'"{sample_text}"')
    
    # 滑动窗口策略
    print("\n" + "🔄 滑动窗口策略".center(50, "-"))
    sliding_chunker = SlidingWindowChunker()
    sliding_chunks = sliding_chunker.chunk(sample_text, window_size=80, step_size=40)
    
    for i, chunk in enumerate(sliding_chunks, 1):
        print(f"\n块 {i}: ({chunk.start_pos}-{chunk.end_pos})")
        print(f'内容: "{chunk.content}"')
        print(f"重叠信息: {chunk.overlap_info}")
        print(f"问题: {'❌ 可能截断句子' if not chunk.content.endswith(('.', '!', '?', '。', '！', '？')) else '✅ 完整结束'}")
    
    # 智能重叠策略
    print("\n" + "🧠 智能重叠策略".center(50, "-"))
    smart_chunker = SmartOverlapChunker()
    smart_chunks = smart_chunker.chunk(sample_text, target_size=80, overlap_ratio=0.3)
    
    for i, chunk in enumerate(smart_chunks, 1):
        print(f"\n块 {i}:")
        print(f'内容: "{chunk.content}"')
        print(f"重叠信息: {chunk.overlap_info}")
        print(f"语义完整性: {'✅ 保持完整' if chunk.content.strip().endswith(('.', '!', '?', '。', '！', '？')) else '⚠️ 需要检查'}")
    
    # 对比总结
    print("\n" + "📈 策略对比总结".center(50, "="))
    print(f"""
    滑动窗口策略:
    ✅ 实现简单，计算效率高
    ✅ 重叠大小可精确控制
    ❌ 可能在句子中间分割，破坏语义
    ❌ 重叠内容可能不完整
    ❌ 不考虑文本的语义结构
    
    智能重叠策略:
    ✅ 保持语义完整性
    ✅ 重叠内容是完整的语义单元
    ✅ 适应文本的自然结构
    ✅ 更好的上下文保持
    ❌ 实现相对复杂
    ❌ 重叠大小可能不够精确
    """)


def demonstrate_edge_cases():
    """演示边界情况的处理差异"""
    
    print("\n" + "🔍 边界情况处理对比".center(50, "="))
    
  