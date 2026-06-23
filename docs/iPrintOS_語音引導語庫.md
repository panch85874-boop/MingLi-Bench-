# iPrintOS 語音引導語庫（100 句）｜中英雙語

> 用途：語音助理**命中意圖後要播給客人的固定引導語**（封閉問答庫的答案側）。
> 對應規劃文件 `iPrintOS_語音PoC_工程規劃.md` v0.2，§8 第 2 份語料。
> **核心設計原則（v0.3 重做）：無人店「自助優先、不靠真人」。** 每句都要把客人導向自己解決——
> ①依機台螢幕指示自行處理 ②**改用店內另外兩台機器**（一店三台）③在手機操作頁面填聯絡資料自助申請退款/處理 ④參考線上常見問題頁面。**真人聯絡不是選項；只有火災/受傷才導緊急電話。**
> 原則：每句簡短（口語、1~2 句、適合 TTS）；模型不自由生成，只從本庫選。
> 佔位：`〔線上FAQ〕`＝線上常見問題頁面網址/QR；「手機操作頁面」＝客人掃 QR 進入的 iPrintOS 操作介面（可填聯絡資料申請退款/處理）。
> ⚠️ **前置相依（已採過渡措辭）**：兩個出口尚未建置——①退款/聯絡自助入口（規劃文件 D-A，**P0**）②線上FAQ頁面（D-B）。本庫 PAY/CMP 已改為**過渡期措辭：付款後沒印好→只導「改用另一台重印、不扣款」，不承諾現場退款**（決策 1B）；扣款爭議→致歉＋保留交易紀錄＋告知線上申請即將開放。HLP 類以「語音引導＋機台螢幕」為主，FAQ 連結待 D-B 上線再播。〔D-A 上線後〕標註處為目標措辭。
> 場域：**一店三台、每台間隔約 1 公尺**，故「改用旁邊另一台機器」對客人移動成本極低，為硬體問題首選自助解。
> 實作時轉成 `config/guidance.jsonl`，欄位：`guidance_id, intent, triggers[], tts_zh, tts_en`。

---

## SYS — 系統句（問候 / 沒聽清楚 / 收尾）（4）

> 比對邏輯：**只要聽到問句就一定回最接近的一句**，沒有「無資料」回覆。SYS-03/04 只用在**完全沒聽到語音**（no_speech）的情況。

| id | trigger（情境） | 中文引導（TTS） | English |
|---|---|---|---|
| SYS-01 | 偵測到有人進入 | 您好，歡迎光臨，需要我幫忙嗎？ | Hi, welcome. Do you need any help? |
| SYS-02 | 客人以英文回應 | Hi! How can I help you with printing or copying today? | Hi! How can I help you with printing or copying today? |
| SYS-03 | 完全沒收到語音 / 純噪音（no_speech） | 不好意思，我沒聽清楚，可以請您再說一次嗎？ | Sorry, I didn't catch that—could you say it again? |
| SYS-04 | 連續 2 次沒聽到 → 收尾 | 不好意思我還是沒聽清楚，您可以直接在機台螢幕操作。 | Sorry, I still didn't catch that—please use the on-screen menu. |

---

## PM — print_mobile｜手機 / 雲端檔案列印（22）

| id | trigger（客人會講） | 中文引導（TTS） | English |
|---|---|---|---|
| PM-01 | 我要印手機裡的檔案 | 好的，請拿手機掃描機台上的 QR Code，就能上傳檔案列印。 | Sure—scan the QR code on the machine with your phone to upload and print. |
| PM-02 | QR Code 在哪裡 | QR Code 在機台螢幕或機身貼紙上，掃描後手機會打開上傳頁面。 | The QR code is on the screen or a sticker on the machine; scanning opens the upload page. |
| PM-03 | 支援什麼檔案格式 | 支援 PDF、Word、以及 JPG、PNG 圖片，建議先轉成 PDF 最穩定。 | We support PDF, Word, and JPG/PNG images; PDF works best. |
| PM-04 | LINE 的檔案怎麼印 | 先在 LINE 把檔案存到手機，再掃 QR Code 從上傳頁選那個檔案。 | Save the file from LINE to your phone first, then upload it after scanning the QR code. |
| PM-05 | 我要印照片 | 掃 QR Code 後選照片上傳，可以選彩色和尺寸再確認列印。 | Scan the QR code, upload your photo, choose color and size, then confirm. |
| PM-06 | 要選黑白還是彩色 | 上傳後在手機頁面可以切換黑白或彩色，彩色費用較高。 | After uploading, switch between black-and-white and color on your phone; color costs more. |
| PM-07 | 怎麼設定份數 | 在手機預覽頁面可以調整份數，確認後再付款。 | Set the number of copies on the preview page, then pay. |
| PM-08 | 可以雙面印嗎 | 可以，在手機設定頁面選「雙面列印」即可。 | Yes—choose double-sided in the settings on your phone. |
| PM-09 | 紙張大小怎麼選 | 可選 A4 或 A3，在手機頁面的紙張設定切換。 | Choose A4 or A3 under paper settings on your phone. |
| PM-10 | 印之前可以先看嗎 | 可以，付款前手機會顯示預覽，確認沒問題再付款。 | Yes—you'll see a preview before paying, so check it first. |
| PM-11 | 檔案太大傳不上去 | 檔案較大請稍等上傳完成，或先壓縮、分次上傳。 | For large files, wait for the upload to finish, or compress and split it. |
| PM-12 | 上傳後找不到檔案 | 請確認上傳完成的提示，沒有的話重新掃 QR Code 再上傳一次。 | Check for the upload-complete confirmation; if missing, rescan and upload again. |
| PM-13 | 上傳完怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成即可。 | After the preview, tap pay and complete it via mobile payment as shown. |
| PM-14 | 印好的紙在哪裡拿 | 付款完成後紙張會從機台出紙匣送出，請到出紙口拿取。 | After payment, your prints come out of the output tray—collect them there. |
| PM-15 | 可以一次印很多檔案嗎 | 可以，上傳頁面能加入多個檔案，會一起計算份數與價格。 | Yes—add multiple files on the upload page; they're counted and priced together. |
| PM-16 | Word 排版跑掉了 | Word 轉檔有時會位移，建議先在手機轉成 PDF 再上傳最準確。 | Word layout can shift; convert to PDF before uploading for best accuracy. |
| PM-17 | 手機沒網路怎麼辦 | 請開啟手機行動網路，或連線店內提供的網路後再掃 QR Code。 | Turn on mobile data, or join the in-store network, then scan the QR code. |
| PM-18 | 上傳到一半想取消 | 直接關閉手機頁面即可取消，未付款不會列印也不會收費。 | Just close the page to cancel; nothing prints or is charged before payment. |
| PM-19 | 可以縮放或滿版嗎 | 在手機設定可選縮放或滿版列印，預覽會即時更新。 | Choose scaling or fit-to-page in settings; the preview updates instantly. |
| PM-20 | 列印怎麼算錢 | 系統會依頁數、黑白或彩色、紙張大小自動計價，付款前會顯示金額。 | Price is by pages, color, and paper size; the amount shows before payment. |
| PM-21 | 印一份要等多久 | 付款後通常幾秒到十幾秒就會出紙，份數多會久一點。 | Prints usually come out within seconds after payment; more copies take longer. |
| PM-22 | 我的檔案會被留下來嗎 | 您的檔案只暫存在店內主機處理，列印後會自動清除，不會上傳雲端。 | Your file is processed only on the in-store machine and cleared after printing—never uploaded. |

---

## CID — copy_id｜身分證 / 證件影印（14）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CID-01 | 我要影印身分證 | 好的，請把證件放在影印機玻璃面板上，蓋上蓋子，依畫面操作影印。 | Sure—place your ID on the scanner glass, close the lid, and follow the screen. |
| CID-02 | 正反面要印同一張 | 可以選「證件影印」模式，會把正反面合印在同一張紙上。 | Choose ID-copy mode to print both sides on one sheet. |
| CID-03 | 證件要放哪裡 | 放在玻璃面板左上角對齊標示線，印好再翻面印背面。 | Align it to the top-left mark on the glass; flip it to copy the back. |
| CID-04 | 健保卡 / 駕照可以印嗎 | 可以，健保卡、駕照都用同樣的證件影印方式操作。 | Yes—health cards and licenses use the same ID-copy steps. |
| CID-05 | 護照怎麼印 | 護照翻到資料頁，平放在玻璃面板上影印即可。 | Open the passport to the photo page and place it flat on the glass. |
| CID-06 | 可以放大嗎 | 可以，在畫面選放大或縮小比例後再影印。 | Yes—choose enlarge or reduce on the screen before copying. |
| CID-07 | 要黑白還是彩色 | 證件可選黑白或彩色，彩色費用較高，依畫面切換。 | Choose black-and-white or color (color costs more) on the screen. |
| CID-08 | 我要印好幾份 | 在畫面設定份數後再確認影印。 | Set the number of copies on the screen, then confirm. |
| CID-09 | 影印證件多少錢 | 系統會依黑白彩色與份數計價，操作畫面會顯示金額。 | Price depends on color and copies; the amount shows on screen. |
| CID-10 | 影印也要先付款嗎 | 是的，系統會先預覽報價，付款後才會印出來。 | Yes—you'll see a preview and price, and it prints after payment. |
| CID-11 | 印出來歪歪的 | 請把證件對齊玻璃面板角落的標示線，再重印一次。 | Align the ID to the corner mark on the glass and copy again. |
| CID-12 | 我有好幾張證件 | 可以一張一張放上去分別影印，或用證件影印模式逐張處理。 | Copy them one at a time, or use ID-copy mode for each. |
| CID-13 | 印好的在哪拿 | 付款完成後請到機台出紙口拿取。 | Collect your copies from the output tray after payment. |
| CID-14 | 證件影印要多久 | 通常幾秒就會出紙。 | It usually prints within a few seconds. |

---

## SCN — scan｜掃描到 Email / USB（14）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| SCN-01 | 我要掃描文件 | 好的，請把文件放上玻璃面板或送稿器，在畫面選掃描方式。 | Sure—place your document on the glass or feeder and choose a scan option. |
| SCN-02 | 我要掃描到信箱 | 選「掃描到 Email」，輸入您的信箱，掃描後檔案會寄過去。 | Choose Scan-to-Email, enter your address, and the file is sent there. |
| SCN-03 | 我要掃到 USB | 選「掃描到 USB」，把隨身碟插進機台插槽再開始掃描。 | Choose Scan-to-USB and insert your drive into the machine's port. |
| SCN-04 | USB 插哪裡 | USB 插槽在機台前方面板上，插好畫面會顯示已偵測。 | The USB port is on the front panel; the screen confirms when detected. |
| SCN-05 | Email 沒收到 | 請確認信箱輸入正確並查看垃圾信件匣，必要時重新掃描寄送。 | Check the address and your spam folder, then resend if needed. |
| SCN-06 | 可以掃很多頁嗎 | 可以，用上方送稿器一次放多張，會合成一個檔案。 | Yes—use the top feeder for multiple pages combined into one file. |
| SCN-07 | 掃彩色還是黑白 | 可在畫面選彩色或黑白掃描。 | Choose color or black-and-white scanning on the screen. |
| SCN-08 | 掃成 PDF 還是圖片 | 可選 PDF 或 JPG，多頁文件建議選 PDF。 | Choose PDF or JPG; PDF is best for multi-page documents. |
| SCN-09 | 原稿放哪 | 單張放玻璃面板，多張放上方送稿器。 | Single sheets on the glass; multiple sheets in the top feeder. |
| SCN-10 | 掃描要錢嗎 | 掃描費用依機台設定，操作畫面會顯示是否收費與金額。 | Scan fees depend on the machine; the screen shows any charge. |
| SCN-11 | 可以調解析度嗎 | 可以，在畫面選解析度，越高檔案越大。 | Yes—choose resolution on the screen; higher means larger files. |
| SCN-12 | 可以雙面掃嗎 | 可以，用送稿器並在畫面選雙面掃描。 | Yes—use the feeder and select double-sided scanning. |
| SCN-13 | 檔案太大寄不出去 | 請降低解析度或分次掃描，檔案會比較小。 | Lower the resolution or split the scan to reduce file size. |
| SCN-14 | 掃描的檔案會留著嗎 | 掃描檔只暫存於店內主機，完成寄送或存檔後即清除，不上雲。 | Scans are processed on the in-store machine and cleared after sending—never uploaded. |

---

## PAY — payment｜付款操作（16）

> 過渡期：付款後沒出紙 → 導「改用另一台重印、不扣款」，**不承諾現場退款**；退款/查證入口（D-A）上線後再開放。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| PAY-01 | 怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成。 | After the preview, tap pay and complete it via mobile payment as shown. |
| PAY-02 | 可以用什麼付款 | 機台支援掃碼與電子支付，實際方式以付款畫面顯示為準。 | The machine supports QR and mobile payments; see the payment screen for options. |
| PAY-03 | 可以用 LINE Pay 嗎 | 若付款畫面有顯示該選項即可使用，依畫面掃碼付款。 | If it appears on the payment screen, yes—just scan to pay. |
| PAY-04 | 可以刷悠遊卡嗎 | 是否支援以付款畫面顯示為準，請依畫面選擇方式。 | Whether it's supported is shown on the payment screen; choose as displayed. |
| PAY-05 | 可以刷卡嗎 | 信用卡是否支援以付款畫面為準，依畫面操作即可。 | Card support is shown on the payment screen; follow the on-screen steps. |
| PAY-06 | 可以投現金嗎 | 是否收現金以機台設定為準，畫面會顯示可用的付款方式。 | Cash acceptance depends on the machine; the screen shows available methods. |
| PAY-07 | 付款了卻沒出紙 | 請先確認出紙匣並稍等約 30 秒；若仍沒出紙，請直接改用旁邊另一台機器重印，未完成的列印不會扣款。〔D-A 上線後加：或在手機操作頁面填聯絡資料申請退款〕 | Check the output tray and wait ~30s; if nothing prints, just reprint on one of the other machines—unfinished jobs aren't charged. |
| PAY-08 | 我好像被扣兩次 | 不好意思造成困擾；目前現場無法直接處理重複扣款，請先保留您的交易紀錄，線上退款申請功能即將開放，屆時可提出查證。 | Sorry for the trouble—double charges can't be handled on-site yet; please keep your transaction record, online refund requests are coming soon. |
| PAY-09 | 付款失敗 | 請稍候再試一次，或換一種付款方式；也可以直接改用旁邊另一台機器。 | Try again shortly or use another payment method; you can also use one of the other machines. |
| PAY-10 | 付款的 QR 在哪 | 確認預覽後，付款 QR 會顯示在手機或機台畫面上。 | After the preview, the payment QR appears on your phone or the screen. |
| PAY-11 | 有收據或發票嗎 | 電子發票或收據會依畫面顯示，您可以在手機操作頁面查看。 | E-receipts appear on screen; you can view them on the phone page. |
| PAY-12 | 金額好像不對 | 金額會依頁數、彩色與紙張大小自動計算，付款前畫面都會先顯示金額；若仍有疑問，請先保留交易紀錄，線上查證功能即將開放。 | The amount is based on pages, color, and paper, and shows before you pay; if in doubt, keep your record—online checks are coming soon. |
| PAY-13 | 付到一半中斷了 | 未完成付款不會列印也不會扣款，請重新操作一次。 | An incomplete payment won't print or charge; please start again. |
| PAY-14 | 我要退款 | 不好意思，若是付款後沒印出來，您可以直接改用旁邊另一台機器重印，未完成的列印不會扣款；線上退款申請功能即將開放。 | Sorry—if a paid job didn't print, just reprint on one of the other machines (unfinished jobs aren't charged); online refund requests are coming soon. |
| PAY-15 | 有找零或低消嗎 | 相關規則以畫面與機台設定為準，操作前畫面會顯示金額。 | Change and minimum-charge rules follow the machine settings; the amount shows before you pay. |
| PAY-16 | 付款後多久會印 | 付款成功後通常幾秒內就會開始出紙。 | Printing usually starts within seconds after a successful payment. |

---

## ERR — machine_error｜機台狀況（14）

> 自助優先：①依機台螢幕圖示自行排除/加紙 ②**改用店內另外兩台機器**（未完成訂單不扣款）。v1 不導真人。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| ERR-01 | 卡紙了 | 請依機台螢幕的圖示指示打開紙匣、取出卡住的紙張即可；若不想自行處理，旁邊還有另外兩台機器可以直接使用，未完成的列印不會扣款。 | Follow the on-screen diagram to open the tray and remove the jammed paper; or just use one of the other two machines—unfinished jobs aren't charged. |
| ERR-02 | 沒紙了 | 請依機台螢幕指示打開紙匣補充紙張；或直接改用旁邊另一台機器，未完成的列印不會扣款。 | Follow the on-screen steps to refill paper, or use one of the other machines—unfinished jobs aren't charged. |
| ERR-03 | 印出來是空白的 | 印出空白通常是檔案或設定問題，請檢查原始檔案後重新列印，或改用旁邊另一台機器試試。 | A blank page is usually a file or setting issue—check the file and reprint, or try one of the other machines. |
| ERR-04 | 印出來有條紋很髒 | 列印品質不佳時，建議直接改用旁邊另一台機器列印。 | For poor print quality, use one of the other machines. |
| ERR-05 | 機器沒反應 / 當機 | 請直接改用旁邊另一台機器操作，未完成的訂單不會扣款。 | Please use one of the other machines—unfinished jobs aren't charged. |
| ERR-06 | 螢幕黑掉了 | 這台螢幕沒反應時，請改用旁邊另一台機器。 | If this screen is unresponsive, please use one of the other machines. |
| ERR-07 | 印到一半停住 | 請稍候幾秒；若沒有恢復，可改用旁邊另一台機器重印。 | Wait a few seconds; if it doesn't resume, reprint on one of the other machines. |
| ERR-08 | 顏色很淡 / 沒碳粉 | 列印偏淡時，建議改用旁邊另一台機器列印。 | If prints look faded, use one of the other machines. |
| ERR-09 | 我可以自己把紙拉出來嗎 | 可以，請依機台螢幕的圖示指示，慢慢取出卡住的紙張，不要硬拉；不確定的話直接改用旁邊另一台機器。 | Yes—follow the on-screen diagram and gently remove the paper (don't yank it); if unsure, just use another machine. |
| ERR-10 | 紙要怎麼補 | 請依機台螢幕指示打開紙匣，放入紙張即可。 | Follow the on-screen steps to open the tray and add paper. |
| ERR-11 | 我印錯了 | 已印出的內容無法收回；如需重印請重新操作，或改用旁邊另一台機器。 | Printed pages can't be undone; reprint here or on one of the other machines. |
| ERR-12 | 機器有怪聲音 | 機台有異常聲響時，請停止使用這台，改用旁邊另一台機器。 | If the machine makes unusual noises, stop using it and switch to another machine. |
| ERR-13 | 蓋子 / 送稿器卡住 | 請依機台螢幕指示輕輕復位，不要強行扳動；不確定就改用旁邊另一台機器。 | Follow the on-screen steps to gently reset it—don't force it; if unsure, use another machine. |
| ERR-14 | 機器壞掉了 | 這台無法使用時，請直接改用旁邊另一台機器，未完成的訂單不會扣款。 | If this machine isn't working, please use one of the other machines—unfinished jobs aren't charged. |

---

## HLP — human_help｜想找人（8）

> 無人門市：我直接語音引導操作 + 線上常見問題頁面；不導真人。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| HLP-01 | 有沒有人可以幫我 | 這是無人自助門市，我可以直接引導您操作；更詳細的說明也可以參考線上常見問題頁面。 | This is a self-service store—I can guide you directly, or you can check our online FAQ. |
| HLP-02 | 哪裡有更多說明 | 詳細操作說明在線上常見問題頁面〔線上FAQ〕，我也可以一步步引導您。 | Detailed steps are on our online FAQ 〔線上FAQ〕, and I can guide you step by step. |
| HLP-03 | 你們幾點營業 | 營業時間請參考門口或機台上的告示。 | Please see the opening hours posted at the door or on the machine. |
| HLP-04 | 現場都沒有店員嗎 | 對，這是無人門市，全部自助操作；需要時可參考線上常見問題頁面，我也能引導您。 | Yes, it's fully self-service; check the online FAQ anytime, and I can help guide you. |
| HLP-05 | 我不會用，可以教我嗎 | 沒問題，請告訴我您要列印、影印還是掃描，我一步步引導您。 | Of course—tell me if you want to print, copy, or scan, and I'll guide you step by step. |
| HLP-06 | 我遇到緊急狀況 | 若是火災、有人受傷等緊急狀況，請立即撥打 119 或 110。 | For a fire or injury emergency, call 119 or 110 immediately. |
| HLP-07 | 廁所在哪 / 洗手 / 其他問題 | 不好意思，本店是無人自助門市，沒有提供廁所與洗手設備；其他問題請參考門市現場告示。 | Sorry, this unmanned store has no restroom or handwashing facilities; for other questions, please see the in-store notices. |
| HLP-08 | 我已經試很多次了 | 不好意思造成不便，您可以改用旁邊另一台機器，或參考線上常見問題頁面的詳細步驟。 | Sorry for the trouble—try one of the other machines, or see the detailed steps in our online FAQ. |

---

## CMP — complaint｜客訴 / 抱怨（8）

> 過渡期（退款入口未上線）：付款後沒印好 → 導「改用另一台重印、不扣款」；其餘費用爭議 → 致歉 + 保留交易紀錄 + 告知線上申請即將開放。**不導真人、不承諾賠償。**

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CMP-01 | 我被亂扣錢 | 不好意思造成困擾；目前現場無法直接處理扣款爭議，請先保留您的交易紀錄，線上退款申請功能即將開放，屆時可提出查證。 | Sorry for the trouble—charge disputes can't be handled on-site yet; please keep your transaction record, online refund requests are coming soon. |
| CMP-02 | 我要退費 | 不好意思，若是付款後沒印出來，您可以直接改用旁邊另一台機器重印，未完成的列印不會扣款；線上退款申請功能即將開放。 | Sorry—if a paid job didn't print, just reprint on one of the other machines (unfinished jobs aren't charged); online refund requests are coming soon. |
| CMP-03 | 這台爛死了不能用 | 很抱歉造成不便，您可以直接改用旁邊另一台機器，未完成的訂單不會扣款。 | Sorry for the inconvenience—please use one of the other machines; unfinished jobs aren't charged. |
| CMP-04 | 印壞了你要賠我 | 很抱歉，若是付款後沒印好，您可以直接改用旁邊另一台機器重印，未完成的列印不會扣款；線上退款申請功能即將開放。 | I'm sorry—if a paid job didn't print well, reprint on one of the other machines (unfinished jobs aren't charged); online refund requests are coming soon. |
| CMP-05 | 浪費我時間 | 很抱歉耽誤您的時間，您可以直接改用旁邊另一台機器，未完成的列印不會扣款。 | Sorry for the delay—please use one of the other machines; unfinished jobs aren't charged. |
| CMP-06 | 我要客訴 / 投訴 | 了解，您的意見對我們很重要；線上意見回報功能即將開放，屆時可留下您的意見，我們會處理。 | Understood—your feedback matters; an online feedback channel is coming soon and we'll follow up. |
| CMP-07 | 我要找負責人 | 這是無人門市現場沒有專人；線上聯絡功能即將開放，屆時可留下聯絡方式由我們與您聯繫。 | This is an unmanned store with no staff on-site; an online contact channel is coming soon for us to reach you. |
| CMP-08 | 你們服務很差 | 很抱歉讓您有不好的體驗，我們會持續改進；線上意見回報功能即將開放。 | Sorry for the poor experience—we'll keep improving; an online feedback channel is coming soon. |

---

### 統計

| intent | 句數 |
|---|---|
| SYS | 4 |
| print_mobile | 22 |
| copy_id | 14 |
| scan | 14 |
| payment | 16 |
| machine_error | 14 |
| human_help | 8 |
| complaint | 8 |
| **合計** | **100** |

### v0.3 重做摘要（依無人店「不靠真人」原則）
- 清除幾乎所有「撥打店家電話」。
- 硬體問題（卡紙/缺紙/當機/印壞）→ **依螢幕自助 + 改用店內另外兩台機器**。
- 付款/退款爭議 → **手機操作頁面填聯絡資料自助申請**（對應 iPrintOS 手機介面）。
- 想找人/雜項 → **線上常見問題頁面 + 語音引導**。
- 唯一真人/外部聯絡：火災、受傷等緊急 → 119 / 110。
