# 印酱 PrintAI — Android WebView App

A thin native Android wrapper around the PrintAI web app (`https://tw.printaii.com/`).
It is **not** a clone of the site — it loads the real SPA in a hardened `WebView`
and adds the native glue a browser tab can't provide:

- **Photo upload from camera or gallery** — `<input type="file">` opens a chooser
  with both the system camera (via `FileProvider`) and the gallery/file picker,
  including multi-select. This is the critical piece for a print app.
- **In-page live camera** (`getUserMedia`) — `onPermissionRequest` is wired to the
  Android runtime camera permission.
- **`device_id` deep linking** — scanning the printer's QR code (a `tw.printaii.com`
  URL carrying `device_id`) opens the app straight to that device via Android App
  Links. See [App Links setup](#app-links-setup).
- **Pull-to-refresh**, top progress bar, and WebView-aware **back navigation**.
- **External links** (`tel:`, `mailto:`, `intent:`, other hosts) open in the right
  external app instead of trapping inside the WebView.
- **Downloads** routed through Android's `DownloadManager`.
- **Cookies / DOM storage / state** persisted so the SPA session survives rotation
  and backgrounding.

## Project layout

```
android/
├── app/
│   ├── build.gradle.kts            # module config; BASE_URL lives here
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/printaii/app/MainActivity.kt
│       └── res/                    # layout, theme, strings, adaptive icon
├── build.gradle.kts                # plugin versions (AGP 8.6.1 / Kotlin 2.0.21)
├── settings.gradle.kts
└── gradlew                         # Gradle 8.14.3 wrapper
```

## Build

Requires the Android SDK (API 34) — easiest via **Android Studio**:

1. Open the `android/` folder in Android Studio and let it sync.
2. Run on a device/emulator, or build an APK:

```bash
cd android
./gradlew assembleDebug      # output: app/build/outputs/apk/debug/app-debug.apk
```

For a release build, create `app/build/outputs/.../app-release.aab` with
`./gradlew bundleRelease` after configuring signing in `app/build.gradle.kts`.

> A `local.properties` with `sdk.dir=/path/to/Android/sdk` is created automatically
> by Android Studio. If building purely from CLI, create it yourself.

## Configuration

- **Target URL** — `BASE_URL` in `app/build.gradle.kts` (`defaultConfig`).
  Defaults to `https://tw.printaii.com/#/`. Override per build type for staging.
- **In-app hosts** — `allowedHosts` in `MainActivity.kt`. URLs on these hosts stay
  in the WebView; everything else is handed to the OS. Add subdomains here.
- **App name / icon / colors** — `res/values/strings.xml`, `res/values/colors.xml`,
  `res/drawable/ic_launcher_foreground.xml`.

## App Links setup

The manifest declares `android:autoVerify="true"` for `tw.printaii.com`. For
Android to verify it (and open QR/printer links directly in the app instead of a
browser), host this file at **`https://tw.printaii.com/.well-known/assetlinks.json`**:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.printaii.app",
    "sha256_cert_fingerprints": ["REPLACE_WITH_YOUR_SIGNING_CERT_SHA256"]
  }
}]
```

Get the fingerprint from your signing key:

```bash
keytool -list -v -keystore my-release.keystore -alias my-alias \
  | grep SHA256
# Play App Signing: copy the SHA-256 from Play Console → Setup → App signing.
```

Until that file is published, the deep-link still works if the user explicitly
chooses the app; only automatic verification needs `assetlinks.json`.

A starter copy lives at [`.well-known/assetlinks.json`](.well-known/assetlinks.json).
