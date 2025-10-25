"""
Command handlers for ClassTop application.
"""

import sys
import numpy as np
from typing import Optional, List, Dict

from pydantic import BaseModel
from pytauri import Commands
from pytauri.ipc import Channel, JavaScriptChannelId, WebviewWindow

from . import logger as _logger
from . import db as _db


# Command registration
commands: Commands = Commands()

# 全局存储 audio channel 以避免重复创建
_audio_channel = None


# Request/Response models
class Person(BaseModel):
    name: str


class Greeting(BaseModel):
    message: str


class LogRequest(BaseModel):
    level: Optional[str] = "info"
    message: str


class LogResponse(BaseModel):
    ok: bool


class LogsResponse(BaseModel):
    lines: List[str]


class SetConfigRequest(BaseModel):
    key: str
    value: str


class ConfigResponse(BaseModel):
    key: str
    value: Optional[str]


class GetLogsRequest(BaseModel):
    max_lines: Optional[int] = 200


class GetConfigRequest(BaseModel):
    key: str


# Command handlers
@commands.command()
async def greet(body: Person) -> Greeting:
    return Greeting(
        message=f"Hello, {body.name}! You've been greeted from Python {sys.version}!"
    )


@commands.command()
async def log_message(body: LogRequest) -> LogResponse:
    lvl = body.level or "info"
    _logger.log_message(lvl, body.message)
    return LogResponse(ok=True)


@commands.command()
async def get_logs(body: GetLogsRequest) -> LogsResponse:
    lines = _logger.tail_logs(int(body.max_lines or 200))
    return LogsResponse(lines=lines)


@commands.command()
async def set_config(body: SetConfigRequest) -> ConfigResponse:
    _db.set_config(body.key, body.value)
    return ConfigResponse(key=body.key, value=body.value)


@commands.command()
async def get_config(body: GetConfigRequest) -> ConfigResponse:
    val = _db.get_config(body.key)
    return ConfigResponse(key=body.key, value=val)


@commands.command()
async def list_configs() -> Dict[str, str]:
    return _db.list_configs()


# Schedule commands
class CourseRequest(BaseModel):
    name: str
    teacher: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    teacher: Optional[str]
    location: Optional[str]
    color: Optional[str]


class ScheduleEntryRequest(BaseModel):
    course_id: int
    day_of_week: int
    start_time: str
    end_time: str
    weeks: Optional[List[int]] = None
    note: Optional[str] = None


class ScheduleEntryResponse(BaseModel):
    id: int
    course_id: int
    course_name: str
    teacher: Optional[str]
    location: Optional[str]
    color: Optional[str]
    day_of_week: int
    start_time: str
    end_time: str
    weeks: List[int]
    note: Optional[str]


class CurrentClassResponse(BaseModel):
    id: int
    name: str
    teacher: Optional[str]
    location: Optional[str]
    start_time: str
    end_time: str
    color: Optional[str]


class NextClassResponse(BaseModel):
    id: int
    name: str
    teacher: Optional[str]
    location: Optional[str]
    day_of_week: int
    start_time: str
    end_time: str
    color: Optional[str]


class WeekRequest(BaseModel):
    week: Optional[int] = None


@commands.command()
async def add_course(body: CourseRequest) -> CourseResponse:
    course_id = _db.add_course(body.name, body.teacher, body.location, body.color)
    return CourseResponse(
        id=course_id,
        name=body.name,
        teacher=body.teacher,
        location=body.location,
        color=body.color
    )


@commands.command()
async def get_courses() -> List[CourseResponse]:
    courses = _db.get_courses()
    return [CourseResponse(**course) for course in courses]


@commands.command()
async def update_course(body: Dict) -> Dict:
    course_id = body.pop("id")
    success = _db.update_course(course_id, **body)
    return {"success": success}


@commands.command()
async def delete_course(body: Dict) -> Dict:
    success = _db.delete_course(body["id"])
    return {"success": success}


@commands.command()
async def add_schedule_entry(body: ScheduleEntryRequest) -> Dict:
    entry_id = _db.add_schedule_entry(
        body.course_id,
        body.day_of_week,
        body.start_time,
        body.end_time,
        body.weeks,
        body.note
    )
    return {"id": entry_id, "success": entry_id > 0}


class ConflictCheckRequest(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    weeks: Optional[List[int]] = None
    exclude_entry_id: Optional[int] = None  # 编辑时排除当前课程


class ConflictEntry(BaseModel):
    id: int
    course_name: str
    teacher: Optional[str]
    location: Optional[str]
    start_time: str
    end_time: str
    day_of_week: int
    weeks: List[int]
    conflict_weeks: List[int]  # 实际冲突的周数


class ConflictCheckResponse(BaseModel):
    has_conflict: bool
    conflicts: List[ConflictEntry]


@commands.command()
async def check_schedule_conflict(body: ConflictCheckRequest) -> ConflictCheckResponse:
    """Check if a schedule entry conflicts with existing entries."""
    if not _db.schedule_manager:
        return ConflictCheckResponse(has_conflict=False, conflicts=[])

    conflicts = _db.schedule_manager.check_conflicts(
        body.day_of_week,
        body.start_time,
        body.end_time,
        body.weeks,
        body.exclude_entry_id
    )

    conflict_entries = [ConflictEntry(**conflict) for conflict in conflicts]

    return ConflictCheckResponse(
        has_conflict=len(conflict_entries) > 0,
        conflicts=conflict_entries
    )


@commands.command()
async def get_schedule(body: WeekRequest) -> List[ScheduleEntryResponse]:
    schedule = _db.get_schedule(body.week)
    return [ScheduleEntryResponse(**entry) for entry in schedule]


@commands.command()
async def delete_schedule_entry(body: Dict) -> Dict:
    success = _db.delete_schedule_entry(body["id"])
    return {"success": success}


@commands.command()
async def get_current_class() -> Optional[CurrentClassResponse]:
    """DEPRECATED: Use get_schedule_by_day and calculate on frontend."""
    current = _db.get_current_class()
    if current:
        return CurrentClassResponse(**current)
    return None


@commands.command()
async def get_next_class() -> Optional[NextClassResponse]:
    """DEPRECATED: Use get_schedule_by_day and calculate on frontend."""
    next_class = _db.get_next_class()
    if next_class:
        return NextClassResponse(**next_class)
    return None


@commands.command()
async def get_last_class() -> Optional[NextClassResponse]:
    """DEPRECATED: Use get_schedule_by_day and calculate on frontend."""
    last_class = _db.get_last_class()
    if last_class:
        return NextClassResponse(**last_class)
    return None


class ScheduleByDayRequest(BaseModel):
    day_of_week: int
    week: Optional[int] = None


@commands.command()
async def get_schedule_by_day(body: ScheduleByDayRequest) -> List[NextClassResponse]:
    """Get all classes for a specific day, optionally filtered by week."""
    classes = _db.get_schedule_by_day(body.day_of_week, body.week)
    return [NextClassResponse(**cls) for cls in classes]


@commands.command()
async def get_schedule_for_week(body: WeekRequest) -> List[NextClassResponse]:
    """Get all classes for the entire week."""
    classes = _db.get_schedule_for_week(body.week)
    return [NextClassResponse(**cls) for cls in classes]


@commands.command()
async def get_current_week() -> Dict:
    """Get the current week number, either calculated or manually set."""
    week = _db.get_calculated_week_number()
    semester_start = _db.get_config("semester_start_date")
    return {
        "week": week,
        "semester_start_date": semester_start,
        "is_calculated": bool(semester_start and semester_start.strip())
    }


@commands.command()
async def get_calculated_week_number() -> int:
    """Get current week number (calculated from semester start date or fallback to manual)."""
    return _db.get_calculated_week_number()


@commands.command()
async def set_semester_start_date(body: Dict) -> Dict:
    """Set the semester start date for automatic week calculation."""
    start_date = body.get("date", "")
    _db.set_config("semester_start_date", start_date)

    # Calculate and return the current week
    if start_date:
        week = _db.get_calculated_week_number()
        return {"success": True, "semester_start_date": start_date, "calculated_week": week}
    else:
        return {"success": True, "semester_start_date": "", "calculated_week": 1}


# ========== Settings Management Commands ==========

@commands.command()
async def get_all_settings() -> Dict[str, str]:
    """Get all application settings."""
    return _db.list_configs()


@commands.command()
async def update_settings(body: Dict) -> Dict:
    """Update multiple settings at once."""
    settings = body.get("settings", {})

    if not settings:
        return {"success": False, "message": "No settings provided"}

    # Update through settings manager if available
    if _db.settings_manager:
        success = _db.settings_manager.update_multiple(settings)
        return {"success": success}
    else:
        # Fallback to individual updates
        for key, value in settings.items():
            _db.set_config(key, str(value))
        return {"success": True}


@commands.command()
async def regenerate_uuid() -> Dict:
    """Regenerate client UUID."""
    if _db.settings_manager:
        new_uuid = _db.settings_manager.regenerate_uuid()
        return {"success": True, "uuid": new_uuid}
    else:
        import uuid
        new_uuid = str(uuid.uuid4())
        _db.set_config('client_uuid', new_uuid)
        return {"success": True, "uuid": new_uuid}


@commands.command()
async def reset_settings(body: Dict) -> Dict:
    """Reset settings to default values."""
    exclude_keys = body.get("exclude", [])

    if _db.settings_manager:
        success = _db.settings_manager.reset_to_defaults(exclude_keys)
        return {"success": success}
    else:
        return {"success": False, "message": "Settings manager not available"}


# Camera commands
class CameraInitResponse(BaseModel):
    success: bool
    camera_count: int
    message: str


class CameraListResponse(BaseModel):
    cameras: List[Dict]


class CameraEncodersResponse(BaseModel):
    h264: Dict
    h265: Dict


class StartRecordingRequest(BaseModel):
    camera_index: int
    filename: Optional[str] = None
    codec_type: Optional[str] = None  # 'H.264' or 'H.265'
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[int] = None
    preset: Optional[str] = None
    bitrate: Optional[str] = None


class RecordingResponse(BaseModel):
    success: bool
    message: str


class StopRecordingRequest(BaseModel):
    camera_index: int


class CameraStatusRequest(BaseModel):
    camera_index: Optional[int] = None


class CameraStatusResponse(BaseModel):
    status: Dict


@commands.command()
async def initialize_camera() -> CameraInitResponse:
    """Initialize camera monitoring system."""
    if not _db.camera_manager:
        return CameraInitResponse(
            success=False,
            camera_count=0,
            message="Camera manager not available"
        )

    success = _db.camera_manager.initialize()
    if success:
        cameras = _db.camera_manager.get_cameras()
        return CameraInitResponse(
            success=True,
            camera_count=len(cameras),
            message=f"Camera system initialized with {len(cameras)} cameras"
        )
    else:
        return CameraInitResponse(
            success=False,
            camera_count=0,
            message="Failed to initialize camera system"
        )


@commands.command()
async def get_cameras() -> CameraListResponse:
    """Get list of available cameras."""
    if not _db.camera_manager:
        return CameraListResponse(cameras=[])

    cameras = _db.camera_manager.get_cameras()
    return CameraListResponse(cameras=cameras)


@commands.command()
async def get_camera_encoders() -> CameraEncodersResponse:
    """Get available video encoders."""
    if not _db.camera_manager:
        return CameraEncodersResponse(
            h264={"available": 0, "encoders": [], "preferred": "libx264"},
            h265={"available": 0, "encoders": [], "preferred": "libx265"}
        )

    encoders = _db.camera_manager.get_encoders()
    return CameraEncodersResponse(**encoders)


@commands.command()
async def start_camera_recording(body: StartRecordingRequest) -> RecordingResponse:
    """Start recording from camera."""
    if not _db.camera_manager:
        return RecordingResponse(
            success=False,
            message="Camera manager not available"
        )

    success = _db.camera_manager.start_recording(
        camera_index=body.camera_index,
        filename=body.filename,
        codec_type=body.codec_type,
        width=body.width,
        height=body.height,
        fps=body.fps,
        preset=body.preset,
        bitrate=body.bitrate
    )

    if success:
        return RecordingResponse(
            success=True,
            message=f"Recording started on camera {body.camera_index}"
        )
    else:
        return RecordingResponse(
            success=False,
            message=f"Failed to start recording on camera {body.camera_index}"
        )


@commands.command()
async def stop_camera_recording(body: StopRecordingRequest) -> RecordingResponse:
    """Stop recording from camera."""
    if not _db.camera_manager:
        return RecordingResponse(
            success=False,
            message="Camera manager not available"
        )

    success = _db.camera_manager.stop_recording(body.camera_index)

    if success:
        return RecordingResponse(
            success=True,
            message=f"Recording stopped on camera {body.camera_index}"
        )
    else:
        return RecordingResponse(
            success=False,
            message=f"Failed to stop recording on camera {body.camera_index}"
        )


@commands.command()
async def get_camera_status(body: CameraStatusRequest) -> CameraStatusResponse:
    """Get camera status."""
    if not _db.camera_manager:
        return CameraStatusResponse(status={"active_cameras": 0, "streamers": {}})

    status = _db.camera_manager.get_status(body.camera_index)
    return CameraStatusResponse(status=status)


# ========== Audio Monitoring Commands ==========

class AudioLevelData(BaseModel):
    """音频响度数据 - 用于 Channel 传输"""
    timestamp: str  # ISO format datetime string
    rms: float      # 均方根值 (0-1)
    db: float       # 分贝值
    peak: float     # 峰值 (0-1)
    source: str     # 数据源: "microphone" or "system"


class StartAudioMonitoringRequest(BaseModel):
    """启动音频监控请求"""
    monitor_type: str  # "microphone" or "system" or "both"
    channel_id: JavaScriptChannelId[AudioLevelData]  # Channel ID from frontend


class StopAudioMonitoringRequest(BaseModel):
    """停止音频监控请求"""
    monitor_type: str  # "microphone" or "system" or "all"


class AudioMonitoringResponse(BaseModel):
    """音频监控响应"""
    success: bool
    message: str


class AudioDevicesResponse(BaseModel):
    """音频设备列表响应"""
    input_devices: List[Dict]
    output_devices: List[Dict]


@commands.command()
async def start_audio_monitoring(
    body: StartAudioMonitoringRequest,
    webview_window: WebviewWindow
) -> AudioMonitoringResponse:
    """启动音频监控并通过 Channel 实时传输数据"""
    global _audio_channel

    if not _db.audio_manager:
        return AudioMonitoringResponse(
            success=False,
            message="Audio manager not available"
        )

    try:
        # 复用或创建 Channel 对象
        if _audio_channel is None:
            _audio_channel = body.channel_id.channel_on(webview_window.as_ref_webview())

        channel = _audio_channel

        if body.monitor_type == "microphone":
            def mic_callback(level):
                try:
                    # 确保 db 值是有限数值，避免 JSON 序列化问题
                    db_value = level.db if np.isfinite(level.db) else -100.0

                    data = AudioLevelData(
                        timestamp=level.timestamp.isoformat(),
                        rms=level.rms,
                        db=db_value,
                        peak=level.peak,
                        source="microphone"
                    )
                    channel.send_model(data)
                except Exception as e:
                    _logger.log_message("error", f"Failed to send mic audio data: {e}")

            _db.audio_manager.start_microphone_monitoring(callback=mic_callback)
            return AudioMonitoringResponse(
                success=True,
                message="Microphone monitoring started"
            )
        elif body.monitor_type == "system":
            def sys_callback(level):
                try:
                    # 确保 db 值是有限数值，避免 JSON 序列化问题
                    db_value = level.db if np.isfinite(level.db) else -100.0

                    data = AudioLevelData(
                        timestamp=level.timestamp.isoformat(),
                        rms=level.rms,
                        db=db_value,
                        peak=level.peak,
                        source="system"
                    )
                    channel.send_model(data)
                except Exception as e:
                    _logger.log_message("error", f"Failed to send sys audio data: {e}")

            _db.audio_manager.start_system_monitoring(callback=sys_callback)
            return AudioMonitoringResponse(
                success=True,
                message="System audio monitoring started"
            )
        elif body.monitor_type == "both":
            # 为 both 模式创建两个不同的 callback
            def mic_callback(level):
                try:
                    # 确保 db 值是有限数值，避免 JSON 序列化问题
                    db_value = level.db if np.isfinite(level.db) else -100.0

                    data = AudioLevelData(
                        timestamp=level.timestamp.isoformat(),
                        rms=level.rms,
                        db=db_value,
                        peak=level.peak,
                        source="microphone"
                    )
                    channel.send_model(data)
                except Exception as e:
                    _logger.log_message("error", f"Failed to send mic audio data: {e}")

            def sys_callback(level):
                try:
                    # 确保 db 值是有限数值，避免 JSON 序列化问题
                    db_value = level.db if np.isfinite(level.db) else -100.0

                    data = AudioLevelData(
                        timestamp=level.timestamp.isoformat(),
                        rms=level.rms,
                        db=db_value,
                        peak=level.peak,
                        source="system"
                    )
                    channel.send_model(data)
                except Exception as e:
                    _logger.log_message("error", f"Failed to send sys audio data: {e}")

            _db.audio_manager.start_all(
                mic_callback=mic_callback,
                sys_callback=sys_callback
            )
            return AudioMonitoringResponse(
                success=True,
                message="Both microphone and system monitoring started"
            )
        else:
            return AudioMonitoringResponse(
                success=False,
                message=f"Invalid monitor_type: {body.monitor_type}"
            )
    except Exception as e:
        _logger.log_message("error", f"Failed to start audio monitoring: {e}")
        return AudioMonitoringResponse(
            success=False,
            message=str(e)
        )


@commands.command()
async def stop_audio_monitoring(body: StopAudioMonitoringRequest) -> AudioMonitoringResponse:
    """停止音频监控"""
    global _audio_channel

    if not _db.audio_manager:
        return AudioMonitoringResponse(
            success=False,
            message="Audio manager not available"
        )

    try:
        if body.monitor_type == "microphone":
            _db.audio_manager.stop_microphone_monitoring()
            return AudioMonitoringResponse(
                success=True,
                message="Microphone monitoring stopped"
            )
        elif body.monitor_type == "system":
            _db.audio_manager.stop_system_monitoring()
            return AudioMonitoringResponse(
                success=True,
                message="System audio monitoring stopped"
            )
        elif body.monitor_type == "all":
            _db.audio_manager.stop_all()
            # 当停止所有监控时，清理 channel
            _audio_channel = None
            return AudioMonitoringResponse(
                success=True,
                message="All audio monitoring stopped"
            )
        else:
            return AudioMonitoringResponse(
                success=False,
                message=f"Invalid monitor_type: {body.monitor_type}"
            )
    except Exception as e:
        _logger.log_message("error", f"Failed to stop audio monitoring: {e}")
        return AudioMonitoringResponse(
            success=False,
            message=str(e)
        )


@commands.command()
async def get_audio_devices() -> AudioDevicesResponse:
    """获取所有可用的音频设备"""
    try:
        from .audio_manager import AudioManager
        devices = AudioManager.list_devices()
        return AudioDevicesResponse(
            input_devices=devices.get("input", []),
            output_devices=devices.get("output", [])
        )
    except Exception as e:
        _logger.log_message("error", f"Failed to list audio devices: {e}")
        return AudioDevicesResponse(
            input_devices=[],
            output_devices=[]
        )


# ========== Data Import/Export Commands ==========

class ExportDataRequest(BaseModel):
    format: str  # "json" or "csv"
    include_courses: bool = True
    include_schedule: bool = True
    include_settings: bool = False


class ExportDataResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    message: str


class ImportDataRequest(BaseModel):
    format: str  # "json" or "csv"
    data: str
    replace_existing: bool = False  # 是否替换现有数据


class ImportDataResponse(BaseModel):
    success: bool
    message: str
    courses_imported: int = 0
    schedule_imported: int = 0


@commands.command()
async def export_schedule_data(body: ExportDataRequest) -> ExportDataResponse:
    """Export schedule data to JSON or CSV format."""
    try:
        import json
        import csv
        import io

        data_dict = {}

        # Export courses
        if body.include_courses:
            courses = _db.get_courses()
            data_dict['courses'] = courses

        # Export schedule
        if body.include_schedule:
            schedule = _db.get_schedule(week=None)
            data_dict['schedule'] = schedule

        # Export settings (optional)
        if body.include_settings:
            settings = _db.list_configs()
            # Exclude sensitive settings
            safe_settings = {k: v for k, v in settings.items()
                           if k not in ['client_uuid', 'server_url', 'api_server_enabled']}
            data_dict['settings'] = safe_settings

        if body.format == 'json':
            # Export as JSON
            json_data = json.dumps(data_dict, ensure_ascii=False, indent=2)
            return ExportDataResponse(
                success=True,
                data=json_data,
                message="数据已导出为 JSON 格式"
            )

        elif body.format == 'csv':
            # Export as CSV (schedule entries only)
            output = io.StringIO()
            writer = csv.writer(output)

            # Write CSV header
            writer.writerow([
                'course_id', 'course_name', 'teacher', 'location', 'color',
                'day_of_week', 'start_time', 'end_time', 'weeks', 'note'
            ])

            # Write schedule entries
            for entry in data_dict.get('schedule', []):
                writer.writerow([
                    entry.get('course_id', ''),
                    entry.get('course_name', ''),
                    entry.get('teacher', ''),
                    entry.get('location', ''),
                    entry.get('color', ''),
                    entry.get('day_of_week', ''),
                    entry.get('start_time', ''),
                    entry.get('end_time', ''),
                    json.dumps(entry.get('weeks', [])),
                    entry.get('note', '')
                ])

            csv_data = output.getvalue()
            return ExportDataResponse(
                success=True,
                data=csv_data,
                message="数据已导出为 CSV 格式"
            )

        else:
            return ExportDataResponse(
                success=False,
                message=f"不支持的导出格式: {body.format}"
            )

    except Exception as e:
        _logger.log_message("error", f"Failed to export data: {e}")
        return ExportDataResponse(
            success=False,
            message=f"导出失败: {str(e)}"
        )


@commands.command()
async def import_schedule_data(body: ImportDataRequest) -> ImportDataResponse:
    """Import schedule data from JSON or CSV format."""
    try:
        import json
        import csv
        import io

        courses_imported = 0
        schedule_imported = 0

        if body.format == 'json':
            # Parse JSON data
            data_dict = json.loads(body.data)

            # Clear existing data if requested
            if body.replace_existing:
                # Delete all schedule entries and courses
                all_courses = _db.get_courses()
                for course in all_courses:
                    _db.delete_course(course['id'])

            # Import courses
            if 'courses' in data_dict:
                course_id_map = {}  # Map old IDs to new IDs
                for course_data in data_dict['courses']:
                    # Remove ID to create new course
                    course_name = course_data.get('name')
                    teacher = course_data.get('teacher')
                    location = course_data.get('location')
                    color = course_data.get('color')

                    new_id = _db.add_course(course_name, teacher, location, color)
                    if new_id > 0:
                        old_id = course_data.get('id')
                        course_id_map[old_id] = new_id
                        courses_imported += 1

            # Import schedule entries
            if 'schedule' in data_dict:
                for entry_data in data_dict['schedule']:
                    old_course_id = entry_data.get('course_id')
                    new_course_id = course_id_map.get(old_course_id)

                    if new_course_id:
                        entry_id = _db.add_schedule_entry(
                            course_id=new_course_id,
                            day_of_week=entry_data.get('day_of_week'),
                            start_time=entry_data.get('start_time'),
                            end_time=entry_data.get('end_time'),
                            weeks=entry_data.get('weeks'),
                            note=entry_data.get('note')
                        )
                        if entry_id > 0:
                            schedule_imported += 1

            return ImportDataResponse(
                success=True,
                message=f"成功导入 {courses_imported} 门课程和 {schedule_imported} 条课程表",
                courses_imported=courses_imported,
                schedule_imported=schedule_imported
            )

        elif body.format == 'csv':
            # Parse CSV data
            reader = csv.DictReader(io.StringIO(body.data))

            # Clear existing data if requested
            if body.replace_existing:
                all_courses = _db.get_courses()
                for course in all_courses:
                    _db.delete_course(course['id'])

            # Map to track created courses
            course_map = {}  # name -> course_id

            for row in reader:
                course_name = row.get('course_name', '').strip()
                if not course_name:
                    continue

                # Create or get course
                if course_name not in course_map:
                    course_id = _db.add_course(
                        name=course_name,
                        teacher=row.get('teacher'),
                        location=row.get('location'),
                        color=row.get('color')
                    )
                    if course_id > 0:
                        course_map[course_name] = course_id
                        courses_imported += 1
                else:
                    course_id = course_map[course_name]

                # Add schedule entry
                try:
                    weeks_str = row.get('weeks', '[]')
                    weeks = json.loads(weeks_str) if weeks_str else None
                except:
                    weeks = None

                entry_id = _db.add_schedule_entry(
                    course_id=course_id,
                    day_of_week=int(row.get('day_of_week', 1)),
                    start_time=row.get('start_time'),
                    end_time=row.get('end_time'),
                    weeks=weeks,
                    note=row.get('note')
                )
                if entry_id > 0:
                    schedule_imported += 1

            return ImportDataResponse(
                success=True,
                message=f"成功导入 {courses_imported} 门课程和 {schedule_imported} 条课程表",
                courses_imported=courses_imported,
                schedule_imported=schedule_imported
            )

        else:
            return ImportDataResponse(
                success=False,
                message=f"不支持的导入格式: {body.format}"
            )

    except Exception as e:
        _logger.log_message("error", f"Failed to import data: {e}")
        return ImportDataResponse(
            success=False,
            message=f"导入失败: {str(e)}"
        )


