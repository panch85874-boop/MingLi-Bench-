# WebView with JS. Keep any @JavascriptInterface methods if added later.
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep WebView client/chrome callbacks invoked reflectively by the framework.
-keep class android.webkit.** { *; }
