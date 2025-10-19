"""
系统音频监控器
"""

import numpy as np
import time
from threading import Thread
from .core import AudioMonitor, AudioLevel
from datetime import datetime


class SystemAudioMonitor(AudioMonitor):
    """系统音频（扬声器输出）监控器 - 使用Windows Core Audio API"""

    def __init__(self, **kwargs):
        """初始化系统音频监控器"""
        super().__init__(**kwargs)
        self._audio_meter = None
        self._initialize_pycaw()

    def _initialize_pycaw(self):
        """初始化Pycaw（Windows Core Audio API）"""
        try:
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

            # 获取默认音频输出设备
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioMeterInformation._iid_, CLSCTX_ALL, None)
            self._audio_meter = interface.QueryInterface(IAudioMeterInformation)

        except Exception as e:
            print(f"初始化Pycaw失败: {e}")
            print("提示: 系统音频监控需要pycaw库，请运行: pip install pycaw comtypes")
            self._audio_meter = None

    def start(self):
        """启动系统音频监控"""
        if self.is_running:
            return

        if self._audio_meter is None:
            print("错误: 无法初始化系统音频监控。")
            return

        self.is_running = True
        self._stop_event.clear()
        self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def _monitor_loop(self):
        """监控循环 - 使用Pycaw获取系统音量"""
        try:
            while self.is_running and not self._stop_event.is_set():
                # 获取当前峰值音量 (0.0 - 1.0)
                peak = self._audio_meter.GetPeakValue()

                # 计算RMS（近似为峰值的70%）
                rms = peak * 0.7

                # 计算分贝
                if rms > 0:
                    db = 20 * np.log10(rms)
                else:
                    db = -np.inf

                # 创建AudioLevel对象
                level = AudioLevel(
                    timestamp=datetime.now(),
                    rms=float(rms),
                    db=float(db),
                    peak=float(peak)
                )

                # 更新当前数据
                self.current_level = level

                # 通知回调
                self._notify_callbacks(level)

                # 控制更新频率
                time.sleep(0.05)  # 20Hz更新率

        except Exception as e:
            print(f"系统音频监控错误: {e}")
            self.is_running = False