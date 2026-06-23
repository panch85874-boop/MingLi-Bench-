# iPrintOS 語音引導語庫（100 句）｜中英雙語

> 用途：語音助理**命中意圖後要播給客人的固定引導語**（封閉問答庫的答案側）。
> 對應規劃文件 `iPrintOS_語音PoC_工程規劃.md` v0.2，§8 第 2 份語料。
> 原則：**每句簡短（口語、1~2 句、適合 TTS）**；模型不自由生成，只從本庫選。
> 定位：簡易問答型語音助理（封閉領域，類似 AI 客服但只播固定答案、不自由閒聊）。
> 電話佔位：`〔店家行動電話〕` 為店家提供的行動電話號碼（靜態資訊，非真人轉接），由各店填入。
> 實作時轉成 `config/guidance.jsonl`，欄位：`guidance_id, intent, triggers[], tts_zh, tts_en`。

---

## SYS — 系統句（問候 / 無資料 / 收尾）

| id | trigger（情境） | 中文引導（TTS） | English |
|---|---|---|---|
| SYS-01 | 偵測到有人進入 | 您好，歡迎光臨，需要我幫忙嗎？ | Hi, welcome. Do you need any help? |
| SYS-02 | 客人以英文回應 | Hi! How can I help you with printing or copying today? | Hi! How can I help you with printing or copying today? |
| SYS-03 | 比對不到 / 低信心 | 抱歉，這個問題我這邊沒有資料，沒辦法幫您處理。 | Sorry, I don't have information about that, so I can't help with it. |
| SYS-04 | 連續 2 次聽不懂 | 不好意思我沒聽清楚，建議您撥打機台上的店家服務電話，由人員協助您。 | Sorry, I couldn't catch that. Please call the store number on the machine for assistance. |

---

## PM — print_mobile｜手機 / 雲端檔案列印（22）

| id | trigger（客人會講） | 中文引導（TTS） | English |
|---|---|---|---|
| PM-01 | 我要印手機裡的檔案 | 好的，請拿手機掃描機台上的 QR Code，就能上傳檔案列印。 | Sure—scan the QR code on the machine with your phone to upload and print. |
| PM-02 | QR Code 在哪裡 | QR Code 在機台螢幕或機身貼紙上，掃描後手機會打開上傳頁面。 | The QR code is on the screen or a sticker on the machine; scanning opens the upload page. |
| PM-03 | 支援什麼檔案格式 | 支援 PDF、Word、以及 JPG、PNG 圖片，建議先轉成 PDF 最穩定。 | We support PDF, Word, and JPG/PNG images; PDF works best. |
| PM-04 | LINE 的檔案怎麼印 | 先在 LINE 把檔案存到手機，再掃 QR Code 從上傳頁選那個檔案。 | Save the file from LINE to your phone first, then upload it on the page after scanning the QR code. |
| PM-05 | 我要印照片 | 掃 QR Code 後選照片上傳，可以選彩色和尺寸再確認列印。 | Scan the QR code, upload your photo, choose color and size, then confirm. |
| PM-06 | 要選黑白還是彩色 | 上傳後在手機頁面可以切換黑白或彩色，彩色費用較高。 | After uploading, switch between black-and-white and color on your phone; color costs more. |
| PM-07 | 怎麼設定份數 | 在手機預覽頁面可以調整份數，確認後再付款。 | Set the number of copies on the preview page, then pay. |
| PM-08 | 可以雙面印嗎 | 可以，在手機設定頁面選「雙面列印」即可。 | Yes—choose double-sided in the settings on your phone. |
| PM-09 | 紙張大小怎麼選 | 可選 A4 或 A3，在手機頁面的紙張設定切換。 | Choose A4 or A3 under paper settings on your phone. |
| PM-10 | 印之前可以先看嗎 | 可以，付款前手機會顯示預覽，確認沒問題再付款。 | Yes—you'll see a preview before paying, so check it first. |
| PM-11 | 檔案太大傳不上去 | 檔案較大請稍等上傳完成，或先壓縮、分次上傳。 | For large files, wait for the upload to finish, or compress and split it. |
| PM-12 | 上傳後找不到檔案 | 請確認上傳完成的綠色提示，沒有的話重新掃 QR Code 再上傳一次。 | Check for the upload-complete confirmation; if it's missing, rescan the QR code and upload again. |
| PM-13 | 上傳完怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成即可。 | After the preview, tap pay and complete it via mobile payment as shown. |
| PM-14 | 印好的紙在哪裡拿 | 付款完成後紙張會從機台出紙匣送出，請到出紙口拿取。 | After payment, your prints come out of the output tray—collect them there. |
| PM-15 | 可以一次印很多檔案嗎 | 可以，上傳頁面能加入多個檔案，會一起計算份數與價格。 | Yes—add multiple files on the upload page; they're counted and priced together. |
| PM-16 | Word 排版跑掉了 | Word 轉檔有時會位移，建議先在手機轉成 PDF 再上傳最準確。 | Word layout can shift; converting to PDF on your phone before uploading is most accurate. |
| PM-17 | 手機沒網路怎麼辦 | 機台附近有提供的網路可連線，或開手機行動網路再掃 QR Code。 | Connect to the provided in-store network, or use mobile data, then scan the QR code. |
| PM-18 | 上傳到一半想取消 | 直接關閉手機頁面即可取消，未付款不會列印也不收費。 | Just close the page to cancel; nothing prints or is charged before payment. |
| PM-19 | 可以縮放或滿版嗎 | 在手機設定可選縮放或滿版列印，預覽會即時更新。 | Choose scaling or fit-to-page in settings; the preview updates instantly. |
| PM-20 | 列印怎麼算錢 | 系統會依頁數、黑白或彩色、紙張大小自動計價，付款前會顯示金額。 | Price is by pages, color, and paper size; the amount shows before payment. |
| PM-21 | 印一份要等多久 | 付款後通常幾秒到十幾秒就會出紙，份數多會久一點。 | Prints usually come out within seconds after payment; more copies take a bit longer. |
| PM-22 | 我的檔案會被留下來嗎 | 您的檔案只暫存在店內主機處理，列印後會自動清除，不會上傳雲端。 | Your file is processed only on the in-store machine and cleared after printing—never uploaded to the cloud. |

---

## CID — copy_id｜身分證 / 證件影印（14）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CID-01 | 我要影印身分證 | 好的，請把證件放在影印機玻璃面板上，蓋上蓋子，依畫面操作影印。 | Sure—place your ID on the scanner glass, close the lid, and follow the screen. |
| CID-02 | 正反面要印同一張 | 可以選「證件影印」模式，會把正反面合印在同一張紙上。 | Choose ID-copy mode to print both sides on one sheet. |
| CID-03 | 證件要放哪裡 | 放在玻璃面板左上角對齊標示線，印好再翻面印背面。 | Align it to the top-left mark on the glass; flip it to copy the back. |
| CID-04 | 健保卡 / 駕照可以印嗎 | 可以，健保卡、駕照都用同樣的證件影印方式操作。 | Yes—health cards and driver's licenses use the same ID-copy steps. |
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
| SCN-05 | Email 沒收到 | 請確認信箱輸入正確並查看垃圾信件匣，必要時重新掃描寄送。 | Check the address is correct and your spam folder, then resend if needed. |
| SCN-06 | 可以掃很多頁嗎 | 可以，用上方送稿器一次放多張，會合成一個檔案。 | Yes—use the top feeder for multiple pages combined into one file. |
| SCN-07 | 掃彩色還是黑白 | 可在畫面選彩色或黑白掃描。 | Choose color or black-and-white scanning on the screen. |
| SCN-08 | 掃成 PDF 還是圖片 | 可選 PDF 或 JPG，多頁文件建議選 PDF。 | Choose PDF or JPG; PDF is best for multi-page documents. |
| SCN-09 | 原稿放哪 | 單張放玻璃面板，多張放上方送稿器。 | Single sheets on the glass; multiple sheets in the top feeder. |
| SCN-10 | 掃描要錢嗎 | 掃描費用依機台設定，操作畫面會顯示是否收費與金額。 | Scan fees depend on the machine; the screen shows any charge. |
| SCN-11 | 可以調解析度嗎 | 可以，在畫面選解析度，越高檔案越大。 | Yes—choose resolution on the screen; higher means larger files. |
| SCN-12 | 可以雙面掃嗎 | 可以，用送稿器並在畫面選雙面掃描。 | Yes—use the feeder and select double-sided scanning. |
| SCN-13 | 檔案太大寄不出去 | 請降低解析度或分次掃描，檔案會比較小。 | Lower the resolution or split the scan to reduce file size. |
| SCN-14 | 掃描的檔案會留著嗎 | 掃描檔只暫存於店內主機完成寄送或存檔後即清除，不上雲。 | Scans are processed on the in-store machine and cleared after sending—never uploaded to the cloud. |

---

## PAY — payment｜付款操作（16）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| PAY-01 | 怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成。 | After the preview, tap pay and complete it via mobile payment as shown. |
| PAY-02 | 可以用什麼付款 | 機台支援掃碼與電子支付，實際方式以付款畫面顯示為準。 | The machine supports QR and mobile payments; see the payment screen for options. |
| PAY-03 | 可以用 LINE Pay 嗎 | 若付款畫面有顯示該選項即可使用，依畫面掃碼付款。 | If it appears on the payment screen, yes—just scan to pay. |
| PAY-04 | 可以刷悠遊卡嗎 | 是否支援以付款畫面顯示為準，請依畫面選擇方式。 | Whether it's supported is shown on the payment screen; choose as displayed. |
| PAY-05 | 可以刷卡嗎 | 信用卡是否支援以付款畫面為準，依畫面操作即可。 | Card support is shown on the payment screen; follow the on-screen steps. |
| PAY-06 | 可以投現金嗎 | 是否收現金以機台設定為準，畫面會顯示可用的付款方式。 | Cash acceptance depends on the machine; the screen shows available methods. |
| PAY-07 | 付款了卻沒出紙 | 請先確認出紙匣並稍等約 30 秒；若仍未出紙，請撥打機台上的店家服務電話確認這筆交易。 | Check the output tray and wait ~30 seconds; if nothing prints, call the store number on the machine to verify the transaction. |
| PAY-08 | 我好像被扣兩次 | 若擔心重複扣款，請撥打機台上的店家服務電話，由人員為您查證。 | If you're worried about a double charge, please call the store number to have it checked. |
| PAY-09 | 付款失敗 | 請稍候再試一次，或換一種付款方式；多次失敗請撥打店家服務電話。 | Try again shortly or use another method; if it keeps failing, call the store number. |
| PAY-10 | 付款的 QR 在哪 | 確認預覽後，付款 QR 會顯示在手機或機台畫面上。 | After the preview, the payment QR appears on your phone or the screen. |
| PAY-11 | 有收據或發票嗎 | 收據或發票方式以畫面顯示為準，需要協助請撥打店家服務電話。 | Receipt options are shown on screen; call the store number if you need help. |
| PAY-12 | 金額好像不對 | 金額依頁數、彩色與紙張自動計算；有疑問請撥打店家服務電話。 | The amount is based on pages, color, and paper; call the store number if it seems wrong. |
| PAY-13 | 付到一半中斷了 | 未完成付款不會列印也不會扣款，請重新操作一次。 | An incomplete payment won't print or charge; please start again. |
| PAY-14 | 我要退款 | 退款需由人員處理，請撥打機台上的店家服務電話協助您。 | Refunds are handled by staff—please call the store number on the machine. |
| PAY-15 | 有找零或低消嗎 | 相關規則以畫面與機台設定為準，需要協助請撥打店家服務電話。 | Change and minimum-charge rules follow the machine settings; call the store number for help. |
| PAY-16 | 付款後多久會印 | 付款成功後通常幾秒內就會開始出紙。 | Printing usually starts within seconds after a successful payment. |

---

## ERR — machine_error｜機台狀況（14）

> v1 不判斷故障原因、不操作機台；只給安全指引與店家聯絡方式。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| ERR-01 | 卡紙了 | 機台卡紙請不要自行用力拉紙，請撥打機台上的店家服務電話協助處理。 | If paper is jammed, don't pull it out by force—call the store number on the machine for help. |
| ERR-02 | 沒紙了 | 機台缺紙需要補紙，請撥打機台上的店家服務電話。 | The machine is out of paper—please call the store number to have it refilled. |
| ERR-03 | 印出來是空白的 | 印出空白可能是檔案或碳粉問題，請撥打店家服務電話，必要時不會重複扣款。 | A blank print may be a file or toner issue—call the store number for assistance. |
| ERR-04 | 印出來有條紋很髒 | 列印品質異常請撥打機台上的店家服務電話，由人員檢查機器。 | For streaky or dirty prints, call the store number so staff can check the machine. |
| ERR-05 | 機器沒反應 / 當機 | 請稍等約一分鐘看是否恢復，仍無反應請撥打店家服務電話。 | Wait about a minute to see if it recovers; if not, call the store number. |
| ERR-06 | 螢幕黑掉了 | 螢幕無顯示請撥打機台上的店家服務電話通知處理。 | If the screen is blank, call the store number to report it. |
| ERR-07 | 印到一半停住 | 列印中斷請稍候，若沒有恢復請撥打店家服務電話。 | If printing stalls, wait a moment; if it doesn't resume, call the store number. |
| ERR-08 | 顏色很淡 / 沒碳粉 | 列印偏淡可能碳粉不足，請撥打機台上的店家服務電話。 | Faded prints may mean low toner—call the store number. |
| ERR-09 | 我可以自己把紙拉出來嗎 | 為了安全請不要自行拆機台或硬拉卡紙，交由人員處理較安全。 | For safety, don't open the machine or force out jammed paper—let staff handle it. |
| ERR-10 | 紙要怎麼補 | 補紙需由人員處理，請撥打機台上的店家服務電話。 | Refilling paper is done by staff—please call the store number. |
| ERR-11 | 我印錯了 | 已印出的內容無法收回，若需協助請撥打店家服務電話。 | Printed pages can't be undone; call the store number if you need help. |
| ERR-12 | 機器有怪聲音 | 機台有異常聲響請停止使用並撥打店家服務電話。 | If the machine makes unusual noises, stop using it and call the store number. |
| ERR-13 | 蓋子 / 送稿器卡住 | 請勿強行扳動，撥打機台上的店家服務電話由人員處理。 | Don't force the lid or feeder—call the store number for help. |
| ERR-14 | 機器壞掉了 | 機台故障請撥打機台上的店家服務電話，會盡快為您處理。 | If the machine is faulty, call the store number and we'll help as soon as possible. |

---

## HLP — human_help｜想找人（8）

> v1 不轉接真人，提供店家聯絡方式與操作總覽。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| HLP-01 | 有沒有人可以幫我 | 這是無人自助門市，需要真人協助請撥打機台上的店家服務電話。 | This is a self-service store; for staff help, please call the store number on the machine. |
| HLP-02 | 店家電話幾號 | 店家服務電話貼在機台上，您也可以記下〔店家行動電話〕。 | The store number is posted on the machine: 〔店家行動電話〕. |
| HLP-03 | 你們幾點營業 | 營業時間請參考門口或機台上的告示。 | Please see the opening hours posted at the door or on the machine. |
| HLP-04 | 現場都沒有店員嗎 | 這是無人門市，現場以自助操作為主，需要時可電話聯絡店家。 | Yes, it's unmanned—everything is self-service; call the store if you need help. |
| HLP-05 | 我不會用，可以教我嗎 | 沒問題，請告訴我您要列印、影印還是掃描，我一步步引導您。 | Of course—tell me if you want to print, copy, or scan, and I'll guide you step by step. |
| HLP-06 | 我遇到緊急狀況 | 緊急狀況請立即撥打機台上的店家服務電話或相關緊急電話。 | In an emergency, call the store number on the machine or emergency services immediately. |
| HLP-07 | 廁所在哪 / 其他問題 | 這部分我這邊沒有資料，建議您撥打店家服務電話詢問。 | I don't have that information—please call the store number to ask. |
| HLP-08 | 我已經試很多次了 | 不好意思造成不便，建議直接撥打機台上的店家服務電話由人員協助。 | Sorry for the trouble—please call the store number for direct assistance. |

---

## CMP — complaint｜客訴 / 抱怨（8）

> v1 不處理爭議、不承諾賠償，只給固定致歉 + 店家聯絡方式。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CMP-01 | 我被亂扣錢 | 不好意思造成困擾，扣款問題需由人員查證，請撥打機台上的店家服務電話。 | Sorry for the trouble—charge issues are verified by staff; please call the store number. |
| CMP-02 | 我要退費 | 退費需由人員處理，請撥打機台上的店家服務電話為您辦理。 | Refunds are handled by staff—please call the store number. |
| CMP-03 | 這台爛死了不能用 | 很抱歉造成您的不便，請撥打機台上的店家服務電話，會盡快為您處理。 | I'm sorry for the inconvenience—please call the store number and we'll help quickly. |
| CMP-04 | 印壞了你要賠我 | 不好意思，賠償相關事宜需由人員處理，請撥打店家服務電話。 | I'm sorry; compensation matters are handled by staff—please call the store number. |
| CMP-05 | 浪費我時間 | 很抱歉耽誤您的時間，需要協助請撥打機台上的店家服務電話。 | I'm sorry for the delay—please call the store number if you need help. |
| CMP-06 | 我要客訴 / 投訴 | 了解，您的意見很重要，請撥打機台上的店家服務電話反映，會有人員處理。 | Understood—your feedback matters; please call the store number to report it. |
| CMP-07 | 我要找負責人 | 需要與負責人聯繫，請撥打機台上的店家服務電話。 | To reach the manager, please call the store number on the machine. |
| CMP-08 | 你們服務很差 | 很抱歉讓您有不好的體驗，請撥打店家服務電話，我們會改進。 | I'm sorry for the poor experience—please call the store number and we'll improve. |

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
