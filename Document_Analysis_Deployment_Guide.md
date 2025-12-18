# Document Analysis Feature Deployment Guide
# 文档分析功能部署指南

## Overview | 概述

This guide explains how to deploy the document analysis feature that allows users to upload .docx courseware files and receive AI-powered analysis.

本指南说明如何部署文档分析功能，该功能允许用户上传 .docx 课件文件并获得 AI 驱动的分析。

**Key Features | 主要功能:**
- Upload .docx files | 上传 .docx 文件
- Extract text content | 提取文本内容
- AI-powered analysis | AI 驱动的分析
- Display structured results | 显示结构化结果

---

## Prerequisites | 前置要求

- DeepSeek AI assistant already deployed | 已部署 DeepSeek AI 助手
- Python 3.8+
- Node.js 16+
- Backend and frontend servers running | 后端和前端服务器运行中

---

## Implementation Steps | 实施步骤

### Step 1: Install Dependencies | 步骤 1：安装依赖

**Backend | 后端:**

Add `python-docx` to `requirements.txt`:

在 `requirements.txt` 中添加 `python-docx`：

\`\`\`text
python-docx>=0.8.11
\`\`\`

**Install | 安装:**
\`\`\`bash
cd backend
pip install python-docx
\`\`\`

---

### Step 2: Create Document Service | 步骤 2：创建文档服务

**File: `backend/app/services/document_service.py`**

This service handles document text extraction and AI analysis.

此服务处理文档文本提取和 AI 分析。

**Key Functions | 关键功能:**

1. **`extract_text_from_docx(file_path)`** - Extract text from .docx files
   
   从 .docx 文件中提取文本

2. **`analyze_document(text_content)`** - Send text to DeepSeek for analysis
   
   将文本发送到 DeepSeek 进行分析

3. **`_parse_text_response(response)`** - Parse AI response into structured data
   
   将 AI 响应解析为结构化数据

**Implementation Details | 实现细节:**

\`\`\`python
import os
from docx import Document
from flask import current_app
from app.services.ai_service import DeepseekAPIService

class DocumentAnalysisService:
    def __init__(self):
        self.ai_service = DeepseekAPIService()
    
    def extract_text_from_docx(self, file_path):
        """Extract text from .docx file"""
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        return '\\n'.join(full_text)
    
    def analyze_document(self, text_content):
        """Analyze document with AI"""
        analysis_prompt = f"""
Analyze the following educational courseware content and provide:

1. Key Topics: List 3-5 main topics covered
2. Learning Objectives: List 3-5 specific learning objectives  
3. Suggested Activities: List 3-5 teaching activities

Content to analyze:
{text_content[:3000]}
"""
        response = self.ai_service.generate_text(analysis_prompt)
        return self._parse_text_response(response)
\`\`\`

---

### Step 3: Add File Upload Endpoint | 步骤 3：添加文件上传端点

**File: `backend/app/api/ai_assistant.py`**

Add the `/analyze-document` endpoint:

添加 `/analyze-document` 端点：

\`\`\`python
@ai.route('/analyze-document', methods=['POST'])
def analyze_document():
    """
    Analyze uploaded courseware document.
    分析上传的课件文档。
    """
    # Check file presence
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Validate file type
    if not file.filename.endswith('.docx'):
        return jsonify({'error': 'Only .docx files supported'}), 400
    
    # Save and analyze
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    try:
        doc_service = DocumentAnalysisService()
        text_content = doc_service.extract_text_from_docx(filepath)
        analysis = doc_service.analyze_document(text_content)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
\`\`\`

---

### Step 4: Update Frontend | 步骤 4：更新前端

**File: `frontend/src/views/AIAssistantView.vue`**

**Add State Variables | 添加状态变量:**

\`\`\`javascript
const analysisData = ref(null)
\`\`\`

**Update File Upload Handler | 更新文件上传处理器:**

\`\`\`javascript
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.name.endsWith('.docx')) {
    // Show error message
    return
  }

  // Upload and analyze
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('http://127.0.0.1:5000/api/ai/analyze-document', {
    method: 'POST',
    body: formData
  })

  const data = await response.json()
  analysisData.value = data.analysis
  showAnalysis.value = true
}
\`\`\`

**Update Analysis Panel | 更新分析面板:**

\`\`\`html
<div v-if="showAnalysis && analysisData" class="visualization-panel">
  <div class="analysis-grid">
    <div class="analysis-card">
      <h4>Key Topics</h4>
      <ul>
        <li v-for="topic in analysisData.key_topics" :key="topic">
          {{ topic }}
        </li>
      </ul>
    </div>
    <!-- Similar for Learning Objectives and Suggested Activities -->
  </div>
</div>
\`\`\`

---

## How It Works | 工作原理

### Workflow | 工作流程

\`\`\`
1. User uploads .docx file
   用户上传 .docx 文件
   ↓
2. Frontend sends file to backend
   前端将文件发送到后端
   ↓
3. Backend extracts text using python-docx
   后端使用 python-docx 提取文本
   ↓
4. Text is sent to DeepSeek AI
   文本发送到 DeepSeek AI
   ↓
5. AI analyzes and returns results
   AI 分析并返回结果
   ↓
6. Backend parses response
   后端解析响应
   ↓
7. Frontend displays structured results
   前端显示结构化结果
\`\`\`

### AI Analysis Prompt | AI 分析提示

The system sends a structured prompt to DeepSeek:

系统向 DeepSeek 发送结构化提示：

- **Request Format | 请求格式:** Plain text with clear instructions
- **Content Limit | 内容限制:** First 3000 characters of document
- **Expected Output | 预期输出:** Three categories of analysis

### Response Parsing | 响应解析

Since DeepSeek may return text instead of JSON, we use a fallback parser:

由于 DeepSeek 可能返回文本而不是 JSON，我们使用备用解析器：

**Parser Features | 解析器特性:**
- Detects section headers (Key Topics, Learning Objectives, etc.)
- Extracts list items starting with `-`, `•`, `*`, or numbers
- Filters out very short items to avoid noise
- Returns structured data regardless of AI response format

检测章节标题、提取列表项、过滤短项、返回结构化数据。

---

## Testing | 测试

### Manual Testing Steps | 手动测试步骤

1. **Start Servers | 启动服务器**
   \`\`\`bash
   # Backend
   cd backend
   python run.py
   
   # Frontend
   cd frontend
   npm run dev
   \`\`\`

2. **Access Application | 访问应用**
   - Navigate to: http://localhost:5173
   - Login as admin
   - Go to AI Assistant page

3. **Upload Document | 上传文档**
   - Click "Upload Courseware" button
   - Select a .docx file
   - Wait for analysis

4. **Verify Results | 验证结果**
   - Check "Courseware Analysis" panel appears
   - Verify Key Topics are displayed
   - Verify Learning Objectives are displayed
   - Verify Suggested Activities are displayed

---

## Troubleshooting | 故障排除

### Issue 1: Empty Analysis Results | 问题 1：分析结果为空

**Symptoms | 症状:**
- Analysis panel shows but cards are empty
- 分析面板显示但卡片为空

**Solution | 解决方案:**
1. Check backend logs for AI response
2. Verify DeepSeek API is working
3. Ensure text extraction succeeded
4. Check parser logic

检查后端日志、验证 API、确保文本提取成功、检查解析逻辑。

### Issue 2: File Upload Fails | 问题 2：文件上传失败

**Symptoms | 症状:**
- Error message: "Only .docx files supported"
- 错误消息："仅支持 .docx 文件"

**Solution | 解决方案:**
- Ensure file has .docx extension
- Check file is not corrupted
- Verify file size is reasonable

确保文件扩展名为 .docx、检查文件未损坏、验证文件大小合理。

### Issue 3: Module Not Found | 问题 3：模块未找到

**Symptoms | 症状:**
- Error: "No module named 'docx'"
- 错误："没有名为 'docx' 的模块"

**Solution | 解决方案:**
\`\`\`bash
pip install python-docx
# Then restart backend server
# 然后重启后端服务器
\`\`\`

---

## Files Modified | 修改的文件

### Backend | 后端
1. **`requirements.txt`** - Added python-docx dependency
2. **`app/services/document_service.py`** - New file for document analysis
3. **`app/api/ai_assistant.py`** - Added /analyze-document endpoint

### Frontend | 前端
1. **`src/views/AIAssistantView.vue`** - Updated file upload and analysis display

---

## Summary | 总结

You have successfully deployed the document analysis feature with:

您已成功部署文档分析功能，具备：

✅ **File Upload** - Support for .docx files | 支持 .docx 文件
✅ **Text Extraction** - Automatic content extraction | 自动内容提取
✅ **AI Analysis** - DeepSeek-powered insights | DeepSeek 驱动的洞察
✅ **Structured Display** - Organized results | 组织化的结果
✅ **Error Handling** - Robust fallback parsing | 健壮的备用解析

**Next Steps | 下一步:**
- Add support for more file formats (PDF, PPT)
- Implement conversation history
- Add export functionality

添加更多文件格式支持、实现对话历史、添加导出功能。
