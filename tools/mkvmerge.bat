@echo off
"%~dp0ffmpeg.exe" -i "%1" -i "%2" -c copy "%3"