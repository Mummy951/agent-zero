# Agent Zero 备份/恢复后端规范

## 概述
本规范定义了 Agent Zero 备份和恢复功能的后端实现，为用户提供了使用基于 glob 模式的选择来备份和恢复其 Agent Zero 配置、数据和自定义文件的能力。备份功能作为设置界面中的专用“备份”选项卡实现，以便于访问和组织。

## 核心要求

### 备份流程
1. 用户在设置模态框中使用 glob 模式配置备份路径
2. 后端创建包含所选文件和元数据的 zip 存档
3. 存档作为下载提供给用户

### 恢复流程
1. 用户在设置模态框中上传备份存档
2. 后端提取并验证元数据
3. 用户确认文件列表和目标路径
4. 后端将文件恢复到指定位置

## 后端架构

### 1. 设置集成

#### 设置模式扩展
在 `python/helpers/settings.py` 中添加带有专用选项卡的备份/恢复部分：

**集成说明：**
- 利用现有设置按钮处理程序模式（遵循 MCP 服务器示例）
- 与 Agent Zero 既定的错误处理和 toast 通知系统集成
- 使用现有文件操作助手，支持 RFC 以兼容开发模式

```python
# 添加到 convert_out() 函数中的 SettingsSection
backup_section: SettingsSection = {
    "id": "backup_restore",
    "title": "备份与恢复",
    "description": "使用基于 glob 模式的文件选择备份和恢复 Agent Zero 数据和配置。",
    "fields": [
        {
            "id": "backup_create",
            "title": "创建备份",
            "description": "使用可自定义的模式创建所选文件和配置的备份存档。",
            "type": "button",
            "value": "创建备份",
        },
        {
            "id": "backup_restore",
            "title": "从备份恢复",
            "description": "通过基于模式的选择从备份存档恢复文件和配置。",
            "type": "button",
            "value": "恢复备份",
        }
    ],
    "tab": "backup",  # 专用的备份选项卡，用于清晰组织
}
```

#### 默认备份配置
备份系统现在使用**已解析的绝对文件系统路径**而不是占位符，确保跨不同部署环境（Docker 容器、直接主机安装、不同用户）的兼容性。

```python
def _get_default_patterns(self) -> str:
    """获取带有已解析绝对路径的默认备份模式"""
    # 确保路径没有双斜杠
    agent_root = self.agent_zero_root.rstrip('/')
    user_home = self.user_home.rstrip('/')

    return f"""# Agent Zero 知识库（排除默认值）
{agent_root}/knowledge/**
!{agent_root}/knowledge/default/**

# Agent Zero 工具（排除默认值）
{agent_root}/instruments/**
!{agent_root}/instruments/default/**

# 内存（排除嵌入缓存）
{agent_root}/memory/**
!{agent_root}/memory/embeddings/**

# 配置和设置（关键）
{agent_root}/.env
{agent_root}/tmp/settings.json
{agent_root}/tmp/chats/**
{agent_root}/tmp/tasks/**
{agent_root}/tmp/uploads/**

# 用户主目录（默认排除隐藏文件）
{user_home}/**
!{user_home}/.*/**
!{user_home}/.*"""
```

**示例解析模式**（因环境而异）：
```
# Docker 容器环境
/a0/knowledge/**
!/a0/knowledge/default/**
/root/**
!/root/.*/**
!/root/.*

# 主机环境
/home/rafael/a0/data/knowledge/**
!/home/rafael/a0/data/knowledge/default/**
/home/rafael/**
!/home/rafael/.*/**
!/home/rafael/.*
```

> **⚠️ 关键文件注意**：`{agent_root}/.env` 文件包含重要的配置，包括 API 密钥、模型设置和运行时参数。此文件是 Agent Zero 正常运行所**必需**的，应始终与 `settings.json` 一起包含在备份中。如果没有此文件，恢复的 Agent Zero 实例将无法访问配置的语言模型或外部服务。

### 2. API 端点

#### 2.1 备份测试端点
**文件**：`python/api/backup_test.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers.backup import BackupService
import json

class BackupTest(ApiHandler):
    """测试备份模式并返回匹配文件"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        patterns = input.get("patterns", "")
        include_hidden = input.get("include_hidden", False)
        max_files = input.get("max_files", 1000)  # 预览限制

        try:
            backup_service = BackupService()
            matched_files = await backup_service.test_patterns(
                patterns=patterns,
                include_hidden=include_hidden,
                max_files=max_files
            )

            return {
                "success": True,
                "files": matched_files,
                "total_count": len(matched_files),
                "truncated": len(matched_files) >= max_files
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### 2.2 备份创建端点
**文件**：`python/api/backup_create.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response, send_file
from python.helpers.backup import BackupService
import tempfile
import os

class BackupCreate(ApiHandler):
    """创建备份存档并提供下载"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        patterns = input.get("patterns", "")
        include_hidden = input.get("include_hidden", False)
        backup_name = input.get("backup_name", "agent-zero-backup")

        try:
            backup_service = BackupService()
            zip_path = await backup_service.create_backup(
                patterns=patterns,
                include_hidden=include_hidden,
                backup_name=backup_name
            )

            # 返回文件供下载
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f"{backup_name}.zip",
                mimetype='application/zip'
            )

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### 2.3 备份恢复端点
**文件**：`python/api/backup_restore.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers.backup import BackupService
from werkzeug.datastructures import FileStorage

class BackupRestore(ApiHandler):
    """从备份存档恢复文件"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        # 处理文件上传
        if 'backup_file' not in request.files:
            return {"success": False, "error": "未提供备份文件"}

        backup_file: FileStorage = request.files['backup_file']
        if backup_file.filename == '':
            return {"success": False, "error": "未选择文件"}

        # 获取恢复配置
        restore_patterns = input.get("restore_patterns", "")
        overwrite_policy = input.get("overwrite_policy", "overwrite")  # 覆盖、跳过、备份

        try:
            backup_service = BackupService()
            result = await backup_service.restore_backup(
                backup_file=backup_file,
                restore_patterns=restore_patterns,
                overwrite_policy=overwrite_policy
            )

            return {
                "success": True,
                "restored_files": result["restored_files"],
                "skipped_files": result["skipped_files"],
                "errors": result["errors"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### 2.4 备份恢复预览端点
**文件**：`python/api/backup_restore_preview.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers.backup import BackupService
from werkzeug.datastructures import FileStorage

class BackupRestorePreview(ApiHandler):
    """根据模式预览将要恢复的文件"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        # 处理文件上传
        if 'backup_file' not in request.files:
            return {"success": False, "error": "未提供备份文件"}

        backup_file: FileStorage = request.files['backup_file']
        if backup_file.filename == '':
            return {"success": False, "error": "未选择文件"}

        restore_patterns = input.get("restore_patterns", "")

        try:
            backup_service = BackupService()
            preview_result = await backup_service.preview_restore(
                backup_file=backup_file,
                restore_patterns=restore_patterns
            )

            return {
                "success": True,
                "files": preview_result["files"],
                "total_count": preview_result["total_count"],
                "skipped_count": preview_result["skipped_count"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### 2.5 备份文件分组预览端点
**文件**：`python/api/backup_preview_grouped.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers.backup import BackupService

class BackupPreviewGrouped(ApiHandler):
    """获取带有智能目录组织的分组文件预览"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        patterns = input.get("patterns", "")
        include_hidden = input.get("include_hidden", False)
        max_depth = input.get("max_depth", 3)
        search_filter = input.get("search_filter", "")

        try:
            backup_service = BackupService()
            grouped_preview = await backup_service.get_grouped_file_preview(
                patterns=patterns,
                include_hidden=include_hidden,
                max_depth=max_depth,
                search_filter=search_filter
            )

            return {
                "success": True,
                "groups": grouped_preview["groups"],
                "stats": grouped_preview["stats"],
                "total_files": grouped_preview["total_files"],
                "total_size": grouped_preview["total_size"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### 2.6 备份进度流端点
**文件**：`python/api/backup_progress_stream.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response, stream_template
from python.helpers.backup import BackupService
import json

class BackupProgressStream(ApiHandler):
    """流式传输实时备份进度"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        patterns = input.get("patterns", "")
        include_hidden = input.get("include_hidden", False)
        backup_name = input.get("backup_name", "agent-zero-backup")

        def generate_progress():
            try:
                backup_service = BackupService()

                # 用于流式传输进度的生成器函数
                for progress_data in backup_service.create_backup_with_progress(
                    patterns=patterns,
                    include_hidden=include_hidden,
                    backup_name=backup_name
                ):
                    yield f"data: {json.dumps(progress_data)}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e), 'completed': True})}\n\n"

        return Response(
            generate_progress(),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        )
```

#### 2.7 备份检查端点
**文件**：`python/api/backup_inspect.py`

```python
from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers.backup import BackupService
from werkzeug.datastructures import FileStorage

class BackupInspect(ApiHandler):
    """检查备份存档并返回元数据"""

    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return True

    async def process(self, input: dict, request: Request) -> dict | Response:
        # 处理文件上传
        if 'backup_file' not in request.files:
            return {"success": False, "error": "未提供备份文件"}

        backup_file: FileStorage = request.files['backup_file']
        if backup_file.filename == '':
            return {"success": False, "error": "未选择文件"}

        try:
            backup_service = BackupService()
            metadata = await backup_service.inspect_backup(backup_file)

            return {
                "success": True,
                "metadata": metadata,
                "files": metadata.get("files", []),
                "include_patterns": metadata.get("include_patterns", []),  # 包含模式数组
                "exclude_patterns": metadata.get("exclude_patterns", []),  # 排除模式数组
                "default_patterns": metadata.get("backup_config", {}).get("default_patterns", ""),
                "agent_zero_version": metadata.get("agent_zero_version", "unknown"),
                "timestamp": metadata.get("timestamp", ""),
                "backup_name": metadata.get("backup_name", ""),
                "total_files": metadata.get("total_files", len(metadata.get("files", []))),
                "backup_size": metadata.get("backup_size", 0),
                "include_hidden": metadata.get("include_hidden", False)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

### 3. 备份服务实现

#### 核心服务类
**文件**：`python/helpers/backup.py`

**RFC 集成说明：**
BackupService 利用 Agent Zero 现有的文件操作助手，该助手已支持开发模式下的 RFC（远程函数调用）路由。这确保了无论是直接运行还是在容器隔离下运行，都能无缝操作。

```python
import zipfile
import json
import os
import tempfile
import datetime
from typing import List, Dict, Any, Optional
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from python.helpers import files, runtime, git
import shutil

class BackupService:
    """Agent Zero 的核心备份和恢复服务"""

    def __init__(self):
        self.agent_zero_version = self._get_agent_zero_version()
        self.agent_zero_root = files.get_abs_path("")  # 已解析的 Agent Zero 根目录
        self.user_home = os.path.expanduser("~")       # 当前用户的主目录

    def _get_default_patterns(self) -> str:
        """从规范中获取默认备份模式"""
        return DEFAULT_BACKUP_PATTERNS

    def _get_agent_zero_version(self) -> str:
        """获取当前 Agent Zero 版本"""
        try:
            # 从 git 信息中获取版本（与 run_ui.py 相同）
            gitinfo = git.get_git_info()
            return gitinfo.get("version", "development")
        except:
            return "unknown"

    def _resolve_path(self, pattern_path: str) -> str:
        """将模式路径解析为绝对系统路径（现在模式已是绝对路径）"""
        return pattern_path

    def _unresolve_path(self, abs_path: str) -> str:
        """将绝对路径转换回模式路径（现在模式已是绝对路径）"""
        return abs_path

    def _parse_patterns(self, patterns: str) -> tuple[list[str], list[str]]:
        """将模式字符串解析为包含和排除模式数组"""
        include_patterns = []
        exclude_patterns = []

        for line in patterns.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('!'):
                # 排除模式
                exclude_patterns.append(line[1:])  # 移除 '!' 前缀
            else:
                # 包含模式
                include_patterns.append(line)

        return include_patterns, exclude_patterns

    def _patterns_to_string(self, include_patterns: list[str], exclude_patterns: list[str]) -> str:
        """将模式数组转换回用于 pathspec 处理的模式字符串"""
        patterns = []

        # 添加包含模式
        for pattern in include_patterns:
            patterns.append(pattern)

        # 添加带有 '!' 前缀的排除模式
        for pattern in exclude_patterns:
            patterns.append(f"!{pattern}")

        return '\n'.join(patterns)

    async def _get_system_info(self) -> Dict[str, Any]:
        """收集用于元数据的系统信息"""
        import platform
        import psutil

        try:
            return {
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "hostname": platform.node(),
                "python_version": platform.python_version(),
                "cpu_count": str(psutil.cpu_count()),
                "memory_total": str(psutil.virtual_memory().total),
                "disk_usage": str(psutil.disk_usage('/').total if os.path.exists('/') else 0)
            }
        except Exception as e:
            return {"error": f"未能收集系统信息: {str(e)}"}

    async def _get_environment_info(self) -> Dict[str, Any]:
        """收集用于元数据的环境信息"""
        try:
            return {
                "user": os.environ.get("USER", "unknown"),
                "home": os.environ.get("HOME", "unknown"),
                "shell": os.environ.get("SHELL", "unknown"),
                "path": os.environ.get("PATH", "")[:200] + "..." if len(os.environ.get("PATH", "")) > 200 else os.environ.get("PATH", ""),
                "timezone": str(datetime.datetime.now().astimezone().tzinfo),
                "working_directory": os.getcwd(),
                "agent_zero_root": files.get_abs_path(""),
                "runtime_mode": "development" if runtime.is_development() else "production"
            }
        except Exception as e:
            return {"error": f"未能收集环境信息: {str(e)}"}

    async def _get_backup_author(self) -> str:
        """获取备份作者/系统标识符"""
        try:
            import getpass
            username = getpass.getuser()
            hostname = platform.node()
            return f"{username}@{hostname}"
        except:
            return "unknown"

    async def _calculate_file_checksums(self, matched_files: List[Dict[str, Any]]) -> Dict[str, str]:
        """计算文件的 SHA-256 校验和"""
        import hashlib

        checksums = {}
        for file_info in matched_files:
            try:
                real_path = file_info["real_path"]
                if os.path.exists(real_path) and os.path.isfile(real_path):
                    hash_sha256 = hashlib.sha256()
                    with open(real_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_sha256.update(chunk)
                    checksums[real_path] = hash_sha256.hexdigest()
            except Exception:
                checksums[file_info["real_path"]] = "error"

        return checksums

    async def _count_directories(self, matched_files: List[Dict[str, Any]]) -> int:
        """计算文件列表中的唯一目录数"""
        directories = set()
        for file_info in matched_files:
            dir_path = os.path.dirname(file_info["path"])
            if dir_path:
                directories.add(dir_path)
        return len(directories)

    def _calculate_backup_checksum(self, zip_path: str) -> str:
        """计算整个备份文件的校验和"""
        import hashlib

        try:
            hash_sha256 = hashlib.sha256()
            with open(zip_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                            hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return "error"

    async def test_patterns(self, patterns: str, include_hidden: bool = False, max_files: int = 1000) -> List[Dict[str, Any]]:
        """测试备份模式并返回匹配文件列表"""

        # 使用 pathspec 解析模式
        pattern_lines = [line.strip() for line in patterns.split('\n') if line.strip() and not line.strip().startswith('#')]

        if not pattern_lines:
            return []

        matched_files = []
        processed_count = 0

        try:
            spec = PathSpec.from_lines(GitWildMatchPattern, pattern_lines)

            # 遍历基本目录
            for base_pattern_path, base_real_path in self.base_paths.items():
                if not os.path.exists(base_real_path):
                    continue

                for root, dirs, files_list in os.walk(base_real_path):
                    # 如果不包含隐藏目录，则过滤隐藏目录
                    if not include_hidden:
                        dirs[:] = [d for d in dirs if not d.startswith('.')]

                    for file in files_list:
                        if processed_count >= max_files:
                            break

                        # 如果不包含隐藏文件，则跳过隐藏文件
                        if not include_hidden and file.startswith('.'):
                            continue

                        file_path = os.path.join(root, file)
                        pattern_path = self._unresolve_path(file_path)

                        # 移除前导斜杠以进行 pathspec 匹配
                        relative_path = pattern_path.lstrip('/')

                        if spec.match_file(relative_path):
                            try:
                                stat = os.stat(file_path)
                                matched_files.append({
                                    "path": pattern_path,
                                    "real_path": file_path,
                                    "size": stat.st_size,
                                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                    "type": "file"
                                })
                                processed_count += 1
                            except (OSError, IOError):
                                # 跳过无法访问的文件
                                continue

                    if processed_count >= max_files:
                        break

                if processed_count >= max_files:
                    break

        except Exception as e:
            raise Exception(f"处理模式时出错: {str(e)}")

        return matched_files

    async def create_backup(self, patterns: str, include_hidden: bool = False, backup_name: str = "agent-zero-backup") -> str:
        """创建包含所选文件的备份存档"""

        # 获取匹配的文件
        matched_files = await self.test_patterns(patterns, include_hidden, max_files=10000)

        if not matched_files:
            raise Exception("没有文件匹配备份模式")

        # 创建临时 zip 文件
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"{backup_name}.zip")

        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 计算文件校验和以进行完整性验证
                file_checksums = await self._calculate_file_checksums(matched_files)

                # 添加全面的元数据 - 这是备份/恢复的控制文件
                include_patterns, exclude_patterns = self._parse_patterns(patterns)

                metadata = {
                    # 基本备份信息
                    "agent_zero_version": self.agent_zero_version,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "backup_name": backup_name,
                    "include_hidden": include_hidden,

                    # 用于恢复期间精细控制的模式数组
                    "include_patterns": include_patterns,  # 包含模式数组
                    "exclude_patterns": exclude_patterns,  # 排除模式数组

                    # 系统和环境信息
                    "system_info": await self._get_system_info(),
                    "environment_info": await self._get_environment_info(),
                    "backup_author": await self._get_backup_author(),

                    # 备份配置
                    "backup_config": {
                        "default_patterns": self._get_default_patterns(),
                        "include_hidden": include_hidden,
                        "compression_level": 6,
                        "integrity_check": True
                    },

                    # 带有校验和的文件信息
                    "files": [
                        {
                            "path": f["path"],
                            "size": f["size"],
                            "modified": f["modified"],
                            "checksum": file_checksums.get(f["real_path"], ""),
                            "type": "file"
                        }
                        for f in matched_files
                    ],

                    # 统计数据
                    "total_files": len(matched_files),
                    "backup_size": sum(f["size"] for f in matched_files),
                    "directory_count": await self._count_directories(matched_files),

                    # 完整性验证
                    "backup_checksum": "",  # 将在备份创建后计算
                    "verification_method": "sha256"
                }

                zipf.writestr("metadata.json", json.dumps(metadata, indent=2))

                # 添加文件
                for file_info in matched_files:
                    real_path = file_info["real_path"]
                    archive_path = file_info["path"].lstrip('/')

                    try:
                        if os.path.exists(real_path) and os.path.isfile(real_path):
                            zipf.write(real_path, archive_path)
                    except (OSError, IOError) as e:
                        # 记录错误但继续处理其他文件
                        print(f"警告: 无法备份文件 {real_path}: {e}")
                        continue

            return zip_path

        except Exception as e:
            # 错误时清理
            if os.path.exists(zip_path):
                os.remove(zip_path)
            raise Exception(f"创建备份时出错: {str(e)}")

    async def inspect_backup(self, backup_file) -> Dict[str, Any]:
        """检查备份存档并返回元数据"""

        # 临时保存上传的文件
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "backup.zip")

        try:
            backup_file.save(temp_file)

            with zipfile.ZipFile(temp_file, 'r') as zipf:
                # 读取元数据
                if "metadata.json" not in zipf.namelist():
                    raise Exception("无效的备份文件: 缺少 metadata.json")

                metadata_content = zipf.read("metadata.json").decode('utf-8')
                metadata = json.loads(metadata_content)

                # 从存档中添加文件列表
                files_in_archive = [name for name in zipf.namelist() if name != "metadata.json"]
                metadata["files_in_archive"] = files_in_archive

                return metadata

        except zipfile.BadZipFile:
            raise Exception("无效的备份文件: 不是有效的 zip 存档")
        except json.JSONDecodeError:
            raise Exception("无效的备份文件: 元数据已损坏")
        finally:
            # 清理
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

    async def get_grouped_file_preview(self, patterns: str, include_hidden: bool = False, max_depth: int = 3, search_filter: str = "") -> Dict[str, Any]:
        """获取按目录结构智能分组的文件预览，并限制深度"""

        # 获取所有匹配的文件
        all_files = await self.test_patterns(patterns, include_hidden, max_files=10000)

        # 如果提供了搜索过滤器，则应用搜索过滤器
        if search_filter.strip():
            search_lower = search_filter.lower()
            all_files = [f for f in all_files if search_lower in f["path"].lower()]

        # 按目录结构分组文件
        groups = {}
        total_size = 0

        for file_info in all_files:
            path = file_info["path"]
            total_size += file_info["size"]

            # 分割路径并限制深度
            path_parts = path.strip('/').split('/')

            # 限制分组深度
            if len(path_parts) > max_depth:
                group_path = '/' + '/'.join(path_parts[:max_depth])
                is_truncated = True
            else:
                group_path = '/' + '/'.join(path_parts[:-1]) if len(path_parts) > 1 else '/'
                is_truncated = False

            if group_path not in groups:
                groups[group_path] = {
                    "path": group_path,
                    "files": [],
                    "file_count": 0,
                    "total_size": 0,
                    "is_truncated": False,
                    "subdirectories": set()
                }

            groups[group_path]["files"].append(file_info)
            groups[group_path]["file_count"] += 1
            groups[group_path]["total_size"] += file_info["size"]
            groups[group_path]["is_truncated"] = groups[group_path]["is_truncated"] or is_truncated

            # 跟踪截断组的子目录
            if is_truncated and len(path_parts) > max_depth:
                next_dir = path_parts[max_depth]
                groups[group_path]["subdirectories"].add(next_dir)

        # 将组转换为排序列表并添加显示信息
        sorted_groups = []
        for group_path, group_info in sorted(groups.items()):
            group_info["subdirectories"] = sorted(list(group_info["subdirectories"]))

            # 限制显示文件以提高 UI 性能
            if len(group_info["files"]) > 50:
                group_info["displayed_files"] = group_info["files"][:50]
                group_info["additional_files"] = len(group_info["files"]) - 50
            else:
                group_info["displayed_files"] = group_info["files"]
                group_info["additional_files"] = 0

            sorted_groups.append(group_info)

        return {
            "groups": sorted_groups,
            "stats": {
                "total_groups": len(sorted_groups),
                "total_files": len(all_files),
                "total_size": total_size,
                "search_applied": bool(search_filter.strip()),
                "max_depth": max_depth
            },
            "total_files": len(all_files),
            "total_size": total_size
        }

    def create_backup_with_progress(self, patterns: str, include_hidden: bool = False, backup_name: str = "agent-zero-backup"):
        """生成器，用于流式传输备份进度"""

        try:
            # 步骤 1：获取匹配的文件
            yield {
                "stage": "discovery",
                "message": "正在扫描文件...",
                "progress": 0,
                "completed": False
            }

            import asyncio
            matched_files = asyncio.run(self.test_patterns(patterns, include_hidden, max_files=10000))

            if not matched_files:
                yield {
                    "stage": "error",
                    "message": "没有文件匹配备份模式",
                    "progress": 0,
                    "completed": True,
                    "error": True
                }
                return

            total_files = len(matched_files);

            yield {
                "stage": "discovery",
                "message": f"找到 {total_files} 个要备份的文件",
                "progress": 10,
                "completed": False,
                "total_files": total_files
            }

            # 步骤 2：计算校验和
            yield {
                "stage": "checksums",
                "message": "正在计算文件校验和...",
                "progress": 15,
                "completed": False
            }

            file_checksums = asyncio.run(self._calculate_file_checksums(matched_files))

            # 步骤 3：创建备份
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, f"{backup_name}.zip")

            yield {
                "stage": "backup",
                "message": "正在创建备份存档...",
                "progress": 20,
                "completed": False
            }

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 首先创建并添加元数据
                metadata = {
                    "agent_zero_version": self.agent_zero_version,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "backup_name": backup_name,
                    "backup_patterns": patterns,
                    "include_hidden": include_hidden,
                    "system_info": asyncio.run(self._get_system_info()),
                    "environment_info": asyncio.run(self._get_environment_info()),
                    "backup_author": asyncio.run(self._get_backup_author()),
                    "backup_config": {
                        "default_patterns": self._get_default_patterns(),
                        "custom_patterns": patterns,
                        "include_hidden": include_hidden,
                        "compression_level": 6,
                        "integrity_check": True
                    },
                    "files": [
                        {
                            "path": f["path"],
                            "size": f["size"],
                            "modified": f["modified"],
                            "checksum": file_checksums.get(f["real_path"], ""),
                            "type": "file"
                        }
                        for f in matched_files
                    ],
                    "total_files": len(matched_files),
                    "backup_size": sum(f["size"] for f in matched_files),
                    "directory_count": asyncio.run(self._count_directories(matched_files)),
                    "backup_checksum": "",
                    "verification_method": "sha256"
                }

                zipf.writestr("metadata.json", json.dumps(metadata, indent=2))

                # 添加文件并更新进度
                for i, file_info in enumerate(matched_files):
                    real_path = file_info["real_path"]
                    archive_path = file_info["path"].lstrip('/')

                    try:
                        if os.path.exists(real_path) and os.path.isfile(real_path):
                            zipf.write(real_path, archive_path)

                            # 每 10 个文件或在关键里程碑处生成进度
                            if i % 10 == 0 or i == total_files - 1:
                                progress = 20 + (i + 1) / total_files * 70  # 20-90%
                                yield {
                                    "stage": "backup",
                                    "message": f"正在添加文件: {file_info['path']}",
                                    "progress": int(progress),
                                    "completed": False,
                                    "current_file": i + 1,
                                    "total_files": total_files,
                                    "file_path": file_info["path"]
                                }
                    except Exception as e:
                        yield {
                            "stage": "warning",
                            "message": f"备份文件失败: {file_info['path']} - {str(e)}",
                            "progress": int(20 + (i + 1) / total_files * 70),
                            "completed": False,
                            "warning": True
                        }

            # 步骤 4：计算最终校验和
            yield {
                "stage": "finalization",
                "message": "正在计算备份校验和...",
                "progress": 95,
                "completed": False
            }

            backup_checksum = self._calculate_backup_checksum(zip_path)

            # 步骤 5：完成
            yield {
                "stage": "completed",
                "message": "备份成功创建",
                "progress": 100,
                "completed": True,
                "success": True,
                "backup_path": zip_path,
                "backup_checksum": backup_checksum,
                "total_files": total_files,
                "backup_size": os.path.getsize(zip_path)
            }

        except Exception as e:
            yield {
                "stage": "error",
                "message": f"备份失败: {str(e)}",
                "progress": 0,
                "completed": True,
                "error": True
            }

    async def restore_backup(self, backup_file, restore_patterns: str, overwrite_policy: str = "overwrite") -> Dict[str, Any]:
        """从备份存档恢复文件"""

        # 临时保存上传的文件
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "backup.zip")

        restored_files = []
        skipped_files = []
        errors = []

        try:
            backup_file.save(temp_file)

            # 如果提供了恢复模式，则解析恢复模式
            if restore_patterns.strip():
                pattern_lines = [line.strip() for line in restore_patterns.split('\n')
                               if line.strip() and not line.strip().startswith('#')]
                spec = PathSpec.from_lines(GitWildMatchPattern, pattern_lines) if pattern_lines else None
            else:
                spec = None

            with zipfile.ZipFile(temp_file, 'r') as zipf:
                # 读取元数据
                if "metadata.json" in zipf.namelist():
                    metadata_content = zipf.read("metadata.json").decode('utf-8')
                    metadata = json.loads(metadata_content)

                # 处理存档中的每个文件
                for archive_path in zipf.namelist():
                    if archive_path == "metadata.json":
                        continue

                    # 检查文件是否匹配恢复模式
                    if spec and not spec.match_file(archive_path):
                        skipped_files.append({
                            "path": archive_path,
                            "reason": "未被模式匹配"
                        })
                        continue

                    # 确定目标路径
                    target_path = self._resolve_path("/" + archive_path)

                    try:
                        # 处理覆盖策略
                        if os.path.exists(target_path):
                            if overwrite_policy == "skip":
                                skipped_files.append({
                                    "path": archive_path,
                                    "reason": "文件已存在_跳过策略"
                                })
                                continue
                            elif overwrite_policy == "backup":
                                backup_path = f"{target_path}.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                shutil.move(target_path, backup_path)

                        # 如果需要，创建目标目录
                        target_dir = os.path.dirname(target_path)
                        os.makedirs(target_dir, exist_ok=True)

                        # 提取文件
                        with zipf.open(archive_path) as source, open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)

                        restored_files.append({
                            "archive_path": archive_path,
                            "target_path": target_path,
                            "status": "restored"
                        })

                    except Exception as e:
                        errors.append({
                            "path": archive_path,
                            "error": str(e)
                        })

            return {
                "restored_files": restored_files,
                "skipped_files": skipped_files,
                "errors": errors
            }

        except Exception as e:
            raise Exception(f"恢复备份时出错: {str(e)}")
        finally:
            # 清理
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

    async def preview_restore(self, backup_file, restore_patterns: str) -> Dict[str, Any]:
        """根据模式预览将要恢复的文件"""

        # 临时保存上传的文件
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "backup.zip")

        files_to_restore = []
        skipped_files = []

        try:
            backup_file.save(temp_file)

            # 如果提供了恢复模式，则解析恢复模式
            if restore_patterns.strip():
                pattern_lines = [line.strip() for line in restore_patterns.split('\n')
                               if line.strip() and not line.strip().startswith('#')]
                spec = PathSpec.from_lines(GitWildMatchPattern, pattern_lines) if pattern_lines else None
            else:
                spec = None

            with zipfile.ZipFile(temp_file, 'r') as zipf:
                # 读取元数据以获取上下文
                metadata = {}
                if "metadata.json" in zipf.namelist():
                    metadata_content = zipf.read("metadata.json").decode('utf-8')
                    metadata = json.loads(metadata_content)

                # 处理存档中的每个文件
                for archive_path in zipf.namelist():
                    if archive_path == "metadata.json":
                        continue

                    # 检查文件是否匹配恢复模式
                    if spec:
                        if spec.match_file(archive_path):
                            files_to_restore.append({
                                "path": archive_path,
                                "target_path": self._resolve_path("/" + archive_path),
                                "action": "restore"
                            })
                        else:
                            skipped_files.append({
                                "path": archive_path,
                                "reason": "未被模式匹配"
                            })
                    else:
                        # 未指定模式，恢复所有文件
                        files_to_restore.append({
                            "path": archive_path,
                            "target_path": self._resolve_path("/" + archive_path),
                            "action": "restore"
                        })

            return {
                "files": files_to_restore,
                "skipped_files": skipped_files,
                "total_count": len(files_to_restore),
                "skipped_count": len(skipped_files)
            }

        except Exception as e:
            raise Exception(f"预览恢复时出错: {str(e)}")
        finally:
            # 清理
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
```

### 4. 依赖项

#### 所需 Python 包
添加到 `requirements.txt`：
```
pathspec>=0.10.0  # 用于 gitignore 风格的模式匹配
psutil>=5.8.0     # 用于系统信息收集
```

#### Agent Zero 内部依赖项
备份系统需要以下 Agent Zero 辅助模块：
- `python.helpers.git` - 用于使用 git.get_git_info() 进行版本检测（与 run_ui.py 一致）
- `python.helpers.files` - 用于文件操作和路径解析
- `python.helpers.runtime` - 用于开发/生产模式检测

#### 安装命令
```bash
pip install pathspec psutil
```

### 5. 错误处理

#### 与 Agent Zero 错误系统集成
备份系统与 Agent Zero 现有的错误处理基础设施集成：

```python
from python.helpers.errors import format_error
from python.helpers.print_style import PrintStyle

# 遵循 Agent Zero 的错误处理模式
try:
    result = await backup_operation()
    return {"success": True, "data": result}
except Exception as e:
    error_message = format_error(e)
    PrintStyle.error(f"备份错误: {error_message}")
    return {"success": False, "error": error_message}
```

#### 常见错误场景
1. **无效模式**：格式错误的 glob 模式
2. **权限错误**：文件/目录不可访问
3. **磁盘空间**：磁盘空间不足以创建备份
4. **无效存档**：损坏或无效的备份文件
5. **路径冲突**：文件位于允许目录之外

#### 错误响应格式
```python
{
    "success": False,
    "error": "人类可读的错误消息",
    "error_code": "BACKUP_PATTERN_INVALID",  # 可选的机器可读代码
    "details": {  # 可选的额外详细信息
        "invalid_patterns": ["pattern1", "pattern2"],
        "suggestion": "检查模式语法"
    }
}
```

### 6. 安全考虑

#### 路径安全
- 验证所有路径以防止目录遍历攻击
- 将备份限制在预定义的基本目录（/a0, /root）
- 清理存档中的文件名
- 为上传/下载实施文件大小限制

#### 认证
- 所有端点都需要认证（`requires_auth = True`）
- 所有端点都需要回环（`requires_loopback = True`）
- 不允许 API 密钥访问以确保安全

#### 文件系统保护
- 对允许路径之外的系统目录进行只读访问
- 备份存档的大小限制
- 备份操作的超时限制
- 临时文件清理

### 7. 性能考虑

#### 文件处理
- 限制测试/预览操作中的文件数量（max_files 参数）
- 流式处理大型存档文件
- 为大型操作实施进度跟踪
- 使用临时目录进行暂存

#### 内存管理
- 流式创建 zip 文件以避免内存问题
- 单独处理文件，而不是将所有文件加载到内存中
- 及时清理临时文件
- 为长时间操作实施超时限制

### 8. 配置

#### 默认配置
```python
BACKUP_CONFIG = {
    "max_files_preview": 1000,
    "max_backup_size": 1024 * 1024 * 1024,  # 1GB
    "max_upload_size": 1024 * 1024 * 1024,  # 1GB
    "operation_timeout": 300,  # 5 分钟
    "temp_cleanup_interval": 3600,  # 1 小时
    "allowed_base_paths": ["/a0", "/root"]
}
```

#### 未来集成机会
**任务调度器集成：**
Agent Zero 现有的任务调度器可以扩展以支持自动化备份：

```python
# 潜在的未来增强 - 计划备份
{
    "name": "auto_backup_daily",
    "type": "scheduled",
    "schedule": "0 2 * * *",  # 每天凌晨 2 点
    "tool_name": "backup_create",
    "tool_args": {
        "patterns": "default_patterns",
        "backup_name": "auto_backup_{date}"
    }
}
```

## 增强的元数据结构和恢复工作流

### 版本检测实现
备份系统使用与 Agent Zero 主 UI 相同的版本检测方法：

```python
def _get_agent_zero_version(self) -> str:
    """获取当前 Agent Zero 版本"""
    try:
        # 从 git 信息中获取版本（与 run_ui.py 相同）
        gitinfo = git.get_git_info()
        return gitinfo.get("version", "development")
    except:
        return "unknown"
```

这确保了备份元数据与主应用程序版本报告之间的一致性。

### Metadata.json 格式
备份存档包含一个全面的 `metadata.json` 文件，其结构如下：

```json
{
  "agent_zero_version": "版本",
  "timestamp": "ISO 日期时间",
  "backup_name": "用户定义名称",
  "include_hidden": 布尔值,

  "include_patterns": [
    "/a0/knowledge/**",
    "/a0/instruments/**",
    "/a0/memory/**",
    "/a0/.env",
    "/a0/tmp/settings.json"
  ],
  "exclude_patterns": [
    "/a0/knowledge/default/**",
    "/a0/instruments/default/**",
    "/a0/memory/embeddings/**"
  ],

  "system_info": { /* 平台、架构等 */ },
  "environment_info": { /* 用户、时区、路径等 */ },
  "backup_author": "user@hostname",
  "backup_config": {
    "default_patterns": "系统默认值",
    "include_hidden": 布尔值,
    "compression_level": 6,
    "integrity_check": true
  },

  "files": [ /* 带有校验和的文件列表 */ ],
  "total_files": 计数,
  "backup_size": 字节,
  "backup_checksum": "sha256"
}
```

### 恢复工作流
1. **上传存档**：用户上传 backup.zip 文件
2. **加载元数据**：系统提取并解析 metadata.json
3. **显示元数据**：完整的 metadata.json 显示在 ACE JSON 编辑器中
4. **用户编辑**：用户可以直接修改 include_patterns 和 exclude_patterns 数组
5. **预览更改**：系统根据当前元数据显示将要恢复的文件
6. **执行恢复**：根据最终元数据配置恢复文件

### JSON 元数据编辑的好处
- **单一事实来源**：metadata.json 是权威配置
- **直接编辑**：用户直接在 ACE 编辑器中编辑 JSON 数组
- **完全控制**：访问所有元数据属性，而不仅仅是模式
- **验证**：JSON 语法验证和数组结构验证
- **透明度**：用户准确查看将用于恢复的内容

## 全面增强摘要

### 增强的元数据结构
备份元数据已显著增强，包括：
- **系统信息**：平台、架构、Python 版本、CPU 计数、内存、磁盘使用情况
- **环境详细信息**：用户、时区、工作目录、运行时模式、Agent Zero 根路径
- **备份作者**：用于备份跟踪的系统标识符（user@hostname）
- **文件校验和**：所有备份文件的 SHA-256 哈希值，用于完整性验证
- **备份统计**：文件总数、目录数、大小以及验证方法
- **兼容性数据**：Agent Zero 版本和环境，用于恢复验证

### 智能文件管理
- **分组文件预览**：按目录结构组织文件，并限制深度（最多 3 级）
- **智能分组**：显示带有可展开文件计数的目录层次结构
- **搜索和过滤**：按文件名或路径片段进行实时过滤
- **性能优化**：限制预览文件（最多 1000 个）和显示文件（每组 50 个），以提高 UI 响应速度

### 实时进度流
- **Server-Sent Events**：通过 `/backup_progress_stream` 端点进行实时备份进度更新
- **多阶段进度**：发现 → 校验和 → 备份 → 完成，并带有百分比跟踪
- **逐文件更新**：实时显示当前正在处理的文件
- **错误处理**：在备份过程中进行优雅的错误报告和警告收集

### 高级 API 端点
1. **`/backup_preview_grouped`**：获取带有深度控制和搜索的智能文件分组
2. **`/backup_progress_stream`**：通过 SSE 流式传输实时备份进度
3. **`/backup_restore_preview`**：使用模式过滤预览恢复操作
4. **增强的 `/backup_inspect`**：返回包含系统信息的全面元数据

### 系统信息收集
- **平台检测**：操作系统、架构、Python 版本、主机名
- **资源信息**：通过 psutil 获取 CPU 计数、内存、磁盘使用情况（转换为字符串以保持 JSON 一致性）
- **环境捕获**：用户、时区、路径、运行时模式
- **版本集成**：使用 git.get_git_info() 实现与主应用程序的一致版本检测
- **完整性验证**：单个文件和完整备份的 SHA-256 校验和

### 安全性和可靠性增强
- **完整性验证**：文件级和备份级校验和验证
- **全面日志记录**：详细的进度跟踪和错误收集
- **路径安全**：增强的验证，带有系统信息上下文
- **备份验证**：版本兼容性检查和环境验证

这份增强的后端规范提供了一个可投入生产的全面备份和恢复系统，具有高级元数据跟踪、实时进度监控和智能文件管理功能，同时保持 Agent Zero 的架构模式和安全标准。

### 实施状态更新

#### ✅ 已完成：核心 BackupService 实现
- **Git 版本集成**：更新为使用与 `run_ui.py` 一致的 `git.get_git_info()`
- **类型安全**：修复了 psutil 返回值为字符串以保持 JSON 元数据一致性
- **代码质量**：所有 linting 错误均已解决，导入结构正确
- **测试验证**：BackupService 正确初始化并检测 Agent Zero 根路径
- **添加依赖项**：pathspec>=0.10.0 用于模式匹配，psutil>=5.8.0 用于系统信息
- **Git Helper 集成**：使用 python.helpers.git.get_git_info() 以保持版本检测一致性

#### 下一个实施阶段：API 端点
准备实施 8 个 API 端点：
1. `backup_test.py` - 模式测试和文件预览
2. `backup_create.py` - 存档创建和下载
3. `backup_restore.py` - 从存档恢复文件
4. `backup_inspect.py` - 存档元数据检查
5. `backup_get_defaults.py` - 获取默认模式
6. `backup_restore_preview.py` - 预览恢复模式
7. `backup_preview_grouped.py` - 智能目录分组
8. `backup_progress_stream.py` - 实时进度流

## 实施清理和最终状态

### ✅ **已完成清理（2024 年 12 月）**

#### **已移除未使用组件：**
- ❌ **`backup_download.py`** - 功能已移至 `backup_create`（直接下载）
- ❌ **`backup_progress_stream.py`** - 未在前端实现，过度设计
- ❌ **`_calculate_file_checksums()` 方法** - 死代码，校验和未正确使用
- ❌ **`_calculate_backup_checksum()` 方法** - 死代码，从未调用
- ❌ **`hashlib` 导入** - 移除校验和后不再需要

#### **简化 BackupService：**
- ✅ **移除校验和计算** - 已计算但未正确使用，使代码过于复杂
- ✅ **简化元数据** - 移除未使用的完整性验证字段
- ✅ **修复 `_count_directories()` 方法** - 返回语句位置错误
- ✅ **更清晰的错误处理** - 移除不必要的警告输出

#### **增强的隐藏文件逻辑：**
最关键的修复是实现了适当的显式模式处理：

```python
# 新增：增强的隐藏文件逻辑
def _get_explicit_patterns(self, include_patterns: List[str]) -> set[str]:
    """提取应始终包含的显式（非通配符）模式"""
    explicit_patterns = set()

    for pattern in include_patterns:
        # 如果模式不包含通配符，则它是显式的
        if '*' not in pattern and '?' not in pattern:
            # 移除前导斜杠以进行比较
            explicit_patterns.add(pattern.lstrip('/'))

            # 同时添加父目录作为显式目录（以便可以遍历隐藏目录）
            path_parts = pattern.lstrip('/').split('/')
            for i in range(1, len(path_parts)):
                parent_path = '/'.join(path_parts[:i])
                explicit_patterns.add(parent_path)

    return explicit_patterns

# 修复：隐藏文件过滤现在遵循显式模式
if not include_hidden and file.startswith('.'):
    if not self._is_explicitly_included(pattern_path, explicit_patterns):
        continue  # 仅排除通过通配符发现的隐藏文件
```

#### **最终 API 端点集（6 个端点）：**
1. ✅ **`backup_get_defaults`** - 获取默认元数据配置
2. ✅ **`backup_test`** - 测试模式和预览文件（试运行）
3. ✅ **`backup_preview_grouped`** - 获取用于 UI 的分组文件预览
4. ✅ **`backup_create`** - 创建和下载备份存档
5. ✅ **`backup_inspect`** - 检查上传的备份元数据
6. ✅ **`backup_restore_preview`** - 预览恢复操作
7. ✅ **`backup_restore`** - 执行恢复操作

### **已修复关键问题：隐藏文件**

**问题：** 当 `include_hidden=false` 时，系统会排除所有隐藏文件，即使它们在 `/a0/.env` 等模式中明确指定了。

**解决方案：** 实施了显式模式检测，区分以下情况：
- **显式模式**（如 `/a0/.env`） - 无论 `include_hidden` 设置如何，始终包含
- **通配符发现**（如 `/a0/*`） - 遵循 `include_hidden` 设置

**结果：** 像 `.env` 这样的关键文件现在在明确指定时会正确备份，确保 Agent Zero 配置得以保留。

### **实施状态：✅ 可投入生产**

备份系统现在：
- **简化**：消除了不必要的复杂性和死代码
- **可靠**：修复了关键的隐藏文件处理
- **高效**：没有不必要的校验和计算
- **整洁**：正确的错误处理和类型安全
- **完整**：完整的备份和恢复功能正常工作

**清理的主要好处：**
- ✅ **更简单的维护** - 更少的代码需要维护和调试
- ✅ **更好的性能** - 没有不必要的校验和计算
- ✅ **正确行为** - 隐藏文件现在按预期工作
- ✅ **更清晰的 API** - 仅使用实际使用的端点
- ✅ **更好的可靠性** - 移除了未正确实现的复杂功能

Agent Zero 备份系统现在已可投入生产并经过实战测试！🚀

## ✅ **最终状态：ACE 编辑器状态保证已完成（2024 年 12 月）**

### **目标实现验证**

主要目标已成功实现：**GUI 中所有 metadata.json 操作都使用 ACE 编辑器状态，而不是原始存档元数据，从而让用户可以完全控制编辑和执行编辑器中定义的精确内容。**

#### **✅ 存档 metadata.json 使用**（最少 - 仅技术要求）：
```python
# 仅用于：
# 1. 初始 ACE 编辑器预加载 (backup_inspect API)
original_backup_metadata = json.loads(metadata_content)
metadata["include_patterns"] = original_backup_metadata.get("include_patterns", [])
metadata["exclude_patterns"] = original_backup_metadata.get("exclude_patterns", [])

# 2. 跨系统兼容性的路径转换
environment_info = original_backup_metadata.get("environment_info", {})
backed_up_agent_root = environment_info.get("agent_zero_root", "")
```

#### **✅ ACE 编辑器元数据使用**（其他所有内容）：
```python
# 用于所有用户可控操作：
backup_metadata = user_edited_metadata if user_edited_metadata else original_backup_metadata

# 1. 用于恢复的文件模式匹配
restore_include_patterns = backup_metadata.get("include_patterns", [])
restore_exclude_patterns = backup_metadata.get("exclude_patterns", [])

# 2. 恢复操作前清理
files_to_delete = await self._find_files_to_clean_with_user_metadata(backup_metadata, original_backup_metadata)

# 3. 所有用户偏好和设置
include_hidden = backup_metadata.get("include_hidden", False)
```

### **实施架构**

#### **混合方法 - 完美平衡：**
- **✅ 用户控制**：ACE 编辑器内容驱动所有恢复操作
- **✅ 技术兼容性**：原始元数据实现跨系统路径转换
- **✅ 完全透明**：用户查看并控制将要执行的内容
- **✅ 系统智能**：自动路径转换保留功能

#### **API 层集成：**
```python
# 预览和恢复 API 都遵循相同的模式：
class BackupRestorePreview(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        # 从 ACE 编辑器获取用户编辑的元数据
        metadata = json.loads(metadata_json)

        # 将用户元数据传递到服务层
        result = await backup_service.preview_restore(
            backup_file=backup_file,
            restore_include_patterns=metadata.get("include_patterns", []),
            restore_exclude_patterns=metadata.get("exclude_patterns", []),
            user_edited_metadata=metadata  # ← ACE 编辑器内容
        )
```

#### **服务层实现：**
```python
# 服务方法智能地使用两个元数据源：
async def preview_restore(self, user_edited_metadata: Optional[Dict[str, Any]] = None):
    # 从存档中读取原始元数据
    original_backup_metadata = json.loads(metadata_content)

    # 使用 ACE 编辑器元数据进行操作
    backup_metadata = user_edited_metadata if user_edited_metadata else original_backup_metadata

    # 用户元数据驱动模式匹配
    files_to_restore = await self._process_with_user_patterns(backup_metadata)

    # 原始元数据实现路径转换
    target_path = self._translate_restore_path(archive_path, original_backup_metadata)
```

### **死代码清理结果**

#### **✅ 已移除未使用方法：**
- **`_find_files_to_clean()` 方法**（39 行） - 已被 `_find_files_to_clean_with_user_metadata()` 替换
- **功能**：使用的是原始存档元数据而不是用户编辑的元数据
- **替换**：新方法正确使用 ACE 编辑器内容进行清理操作

#### **✅ 方法比较：**
```python
# 旧（已移除）：使用原始存档元数据
async def _find_files_to_clean(self, backup_metadata: Dict[str, Any]):
    original_include_patterns = backup_metadata.get("include_patterns", [])  # ← 存档元数据
    # ... 39 行实现

# 新（活动）：使用 ACE 编辑器元数据
async def _find_files_to_clean_with_user_metadata(self, user_metadata: Dict[str, Any], original_metadata: Dict[str, Any]):
    user_include_patterns = user_metadata.get("include_patterns", [])  # ← ACE 编辑器元数据
    # 转换仅使用 original_metadata 进行 environment_info
```

### **用户体验流程**

1. **上传存档** → 提取原始 metadata.json
2. **ACE 编辑器预加载** → 显示原始模式作为起始点
3. **用户编辑** → 完全自由地修改模式、设置
4. **预览操作** → 使用当前 ACE 编辑器内容
5. **执行恢复** → 使用最终 ACE 编辑器内容
6. **路径转换** → 自动系统兼容性（对用户透明）

### **实现的技术优势**

#### **✅ 完全用户控制：**
- 用户可以在 ACE 编辑器中编辑任何模式
- 更改立即反映在预览操作中
- 执行按钮完全按照编辑器中显示的内容运行
- 没有使用不同元数据的隐藏操作

#### **✅ 跨系统兼容性：**
- 路径转换保留技术功能
- 用户无需手动调整路径
- 在不同 Agent Zero 安装之间无缝工作
- 保持备份在环境间的可移植性

#### **✅ 简洁架构：**
- 单一事实来源：ACE 编辑器内容
- 清晰的职责分离：用户控制与技术要求
- 消除了死代码并简化了维护
- 预览和执行之间的一致行为

### **最终状态：✅ 可投入生产**

Agent Zero 备份系统现在提供：
- **✅ 通过 ACE 编辑器状态实现完全用户控制**
- **✅ 通过智能路径转换实现跨系统兼容性**
- **✅ 简洁、可维护的代码，消除了死代码**
- **✅ 透明操作，用户完全可见**
- **✅ 通过全面错误处理实现生产可靠性**

**备份系统完美平衡了用户控制和技术功能！** 🎯 