import { useCallback, useEffect, useRef, useState } from "react";

export type VideoRecorderState =
  | "idle"
  | "requesting-permission"
  | "previewing"
  | "denied"
  | "countdown"
  | "recording"
  | "stopped"
  | "uploading"
  | "error";

const COUNTDOWN_SECONDS = 5;

/** Video-recording counterpart to useAudioRecorder (Round-3 Task 21): camera+mic capture with
 * a live preview, a 5-second countdown before recording starts, and an auto-stop once
 * `durationSeconds` (HR-set, per question) elapses — the candidate never has to click "stop"
 * themselves, matching the requested "automatically stop during the targeted time" behavior. */
export function useVideoRecorder(durationSeconds: number) {
  const [state, setState] = useState<VideoRecorderState>("idle");
  const [countdown, setCountdown] = useState(COUNTDOWN_SECONDS);
  const [remainingSeconds, setRemainingSeconds] = useState(durationSeconds);
  const [videoBlob, setVideoBlob] = useState<Blob | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  // Round-3 follow-up #17 (2026-07-19): live microphone level (0-100), so a candidate can SEE
  // their voice register — a static camera preview alone gives no confirmation the mic actually
  // picks up sound. Driven by a Web Audio AnalyserNode reading the same stream used for preview.
  const [audioLevel, setAudioLevel] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const previewVideoRef = useRef<HTMLVideoElement | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const meterRafRef = useRef<number | null>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const stopAudioMeter = useCallback(() => {
    if (meterRafRef.current !== null) {
      cancelAnimationFrame(meterRafRef.current);
      meterRafRef.current = null;
    }
    audioContextRef.current?.close().catch(() => undefined);
    audioContextRef.current = null;
    analyserRef.current = null;
    setAudioLevel(0);
  }, []);

  const startAudioMeter = useCallback((stream: MediaStream) => {
    if (stream.getAudioTracks().length === 0) return;
    const AudioContextCtor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const audioContext = new AudioContextCtor();
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 512;
    audioContext.createMediaStreamSource(stream).connect(analyser);
    audioContextRef.current = audioContext;
    analyserRef.current = analyser;

    const data = new Uint8Array(analyser.frequencyBinCount);
    const tick = () => {
      analyser.getByteTimeDomainData(data);
      // RMS of the time-domain waveform around its 128 (silence) midpoint -> 0-100 level.
      let sumSquares = 0;
      for (let i = 0; i < data.length; i++) {
        const centered = (data[i] - 128) / 128;
        sumSquares += centered * centered;
      }
      const rms = Math.sqrt(sumSquares / data.length);
      setAudioLevel(Math.min(100, Math.round(rms * 400)));
      meterRafRef.current = requestAnimationFrame(tick);
    };
    meterRafRef.current = requestAnimationFrame(tick);
  }, []);

  const cleanupStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    clearTimer();
    stopAudioMeter();
  }, [clearTimer, stopAudioMeter]);

  useEffect(() => cleanupStream, [cleanupStream]);

  // Round-3 follow-up #14 (2026-07-19, real bug found via live testing — camera stayed black):
  // the <video> preview element is conditionally rendered (only mounted once `state` is
  // "previewing"/"countdown"/"recording") — assigning `.srcObject` INSIDE startPreview()/
  // startRecording() ran too early, while the element was still unmounted (state was still
  // "requesting-permission" at that point), so the assignment silently landed on a null ref and
  // the stream was never actually attached once the element finally mounted. Re-attaching here,
  // keyed on `state`, runs AFTER React has committed the newly-mounted <video> element, so the
  // ref is guaranteed to be populated by the time this fires.
  useEffect(() => {
    if (
      (state === "previewing" || state === "countdown" || state === "recording") &&
      previewVideoRef.current &&
      streamRef.current
    ) {
      previewVideoRef.current.srcObject = streamRef.current;
    }
  }, [state]);

  const stopRecording = useCallback(() => {
    mediaRecorderRef.current?.stop();
  }, []);

  const beginCapture = useCallback(
    async (stream: MediaStream) => {
      const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "video/webm" });
        setVideoBlob(blob);
        setVideoUrl(URL.createObjectURL(blob));
        setState("stopped");
        cleanupStream();
      };

      recorder.start();
      setRemainingSeconds(durationSeconds);
      timerRef.current = setInterval(() => {
        setRemainingSeconds((s) => {
          if (s <= 1) {
            clearTimer();
            recorder.stop();
            return 0;
          }
          return s - 1;
        });
      }, 1000);
      setState("recording");
    },
    [cleanupStream, clearTimer, durationSeconds]
  );

  // Round-3 follow-up #13 (2026-07-19): "Uji Kamera & Mikrofon" — requests getUserMedia and shows
  // a live preview WITHOUT starting the countdown/recording/timer, so a candidate can confirm
  // their camera/mic actually work before committing to a timed answer. Reuses the SAME stream
  // for the real recording afterward (no second permission prompt).
  const startPreview = useCallback(async () => {
    setState("requesting-permission");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamRef.current = stream;
      startAudioMeter(stream);
      setState("previewing");
    } catch {
      setState("denied");
    }
  }, [startAudioMeter]);

  const startRecording = useCallback(async () => {
    let stream = streamRef.current;
    if (!stream) {
      setState("requesting-permission");
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        streamRef.current = stream;
        startAudioMeter(stream);
      } catch {
        setState("denied");
        return;
      }
    }

    setState("countdown");
    setCountdown(COUNTDOWN_SECONDS);
    let remaining = COUNTDOWN_SECONDS;
    const capturedStream = stream;
    timerRef.current = setInterval(() => {
      remaining -= 1;
      setCountdown(remaining);
      if (remaining <= 0) {
        clearTimer();
        beginCapture(capturedStream);
      }
    }, 1000);
  }, [beginCapture, clearTimer, startAudioMeter]);

  const reRecord = useCallback(() => {
    if (videoUrl) URL.revokeObjectURL(videoUrl);
    setVideoBlob(null);
    setVideoUrl(null);
    setRemainingSeconds(durationSeconds);
    setState("idle");
  }, [videoUrl, durationSeconds]);

  const reset = useCallback(() => {
    if (videoUrl) URL.revokeObjectURL(videoUrl);
    setVideoBlob(null);
    setVideoUrl(null);
    setRemainingSeconds(durationSeconds);
    setState("idle");
  }, [videoUrl, durationSeconds]);

  return {
    state,
    setState,
    countdown,
    remainingSeconds,
    videoBlob,
    videoUrl,
    audioLevel,
    previewVideoRef,
    startPreview,
    startRecording,
    stopRecording,
    reRecord,
    reset,
  };
}
