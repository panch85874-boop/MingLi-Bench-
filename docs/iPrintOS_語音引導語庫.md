# iPrintOS 語音引導語庫｜中英雙語（v0.4 擴充版 · 約 230 句）

> 用途：語音助理**比對後要播給客人的固定引導語**（封閉問答庫的答案側）。
> 對應規劃文件 `iPrintOS_語音PoC_工程規劃.md`。
> **核心原則：無人店「自助優先、不靠真人」。** ①依機台螢幕自助 ②**改用店內另外兩台機器**（三台、每台間隔約 1 公尺、未完成不扣款）③檔案只在店內主機處理、完成即清除 ④唯一外部聯絡為火災/受傷 → 119/110。**全程不導真人客服電話。**
> **比對邏輯：模糊語意比對，永遠回最接近的一句**（不設門檻、無「沒資料」回覆）；只有完全沒聽到語音才請客人再說一次。
> **退款過渡（決策 1B）**：付款後沒印好 → 只導「改用另一台重印、不扣款」，**不承諾現場退款**；扣款爭議 → 致歉＋請客人保留交易紀錄＋告知線上申請即將開放。退款自助入口（D-A）為待開發。
> **收錄範圍：只收與 iPrintOS 無人門市相關的會話**——列印/影印/掃描/付款/發票/機台/紙張耗材/店務環境/隱私/招呼互動。**與營業無關的閒聊（如年齡、天氣、時間、純聊天）一律不收**；客人若講無關的話，由 GEN-16 統一拉回列印主題。
> 原則：每句簡短（口語、適合 TTS）；模型只從本庫選句、不自由生成。實作轉成 `config/guidance.jsonl`：`guidance_id, intent, triggers[], tts_zh, tts_en`。
> ⚠️ 標 `〔需店家確認〕` 的答案需各店填入或張貼現場告示（見文末清單）。

---

## SYS — 系統句（問候 / 沒聽清楚 / 收尾）（4）

> 比對只要聽到問句就一定回最接近的一句；SYS-03/04 只用在**完全沒聽到語音**（no_speech）。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| SYS-01 | 偵測到有人進入 | 您好，歡迎光臨，需要我幫忙嗎？ | Hi, welcome. Do you need any help? |
| SYS-02 | 客人以英文回應 | Hi! How can I help you with printing or copying today? | Hi! How can I help you with printing or copying today? |
| SYS-03 | 完全沒收到語音 / 純噪音 | 不好意思，我沒聽清楚，可以請您再說一次嗎？ | Sorry, I didn't catch that—could you say it again? |
| SYS-04 | 連續 2 次沒聽到 → 收尾 | 不好意思我還是沒聽清楚，您可以直接在機台螢幕操作。 | Sorry, I still didn't catch that—please use the on-screen menu. |

---

## GEN — 一般對話 / 問候 / 互動（16）

> 只收與門市使用相關的招呼與互動控制；**與營業無關的閒聊（年齡、時間、純聊天）一律不收**。客人若講無關的話，由 GEN-16 統一拉回列印主題。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| GEN-01 | 你好 / 哈囉 | 您好，需要我幫您列印、影印還是掃描嗎？ | Hello! Do you need printing, copying, or scanning? |
| GEN-02 | 謝謝 | 不客氣，祝您使用順利。 | You're welcome—enjoy! |
| GEN-03 | 再見 / 掰掰 | 謝謝光臨，再見。 | Thanks for visiting, goodbye. |
| GEN-04 | 你是誰 | 我是這家自助影印店的語音助理，可以引導您操作。 | I'm the voice assistant for this self-service store—I can guide you. |
| GEN-05 | 你是機器人嗎 | 是的，我是語音助理，列印相關的問題都可以問我。 | Yes, I'm a voice assistant—ask me anything about printing. |
| GEN-06 | 你聽得懂中文嗎 | 可以，中文或英文都可以跟我說。 | Yes—you can speak to me in Chinese or English. |
| GEN-07 | 你會說英文嗎 | 可以，英文也沒問題。 | Yes, I can help in English too. |
| GEN-08 | 等我一下 / 我想一下 | 好的，您慢慢來，想好再跟我說。 | Sure, take your time. |
| GEN-09 | 沒事了 / 不用了 | 好的，需要時再叫我。 | Okay, just call me if you need anything. |
| GEN-10 | 可以幫我嗎 | 當然，請問您要列印、影印還是掃描？ | Of course—printing, copying, or scanning? |
| GEN-11 | 我第一次用 | 沒問題，告訴我您要做什麼，我一步步帶您。 | No problem—tell me what you need and I'll guide you step by step. |
| GEN-12 | 我趕時間 | 了解，您要列印、影印還是掃描？我帶您最快的步驟。 | Got it—printing, copying, or scanning? I'll guide you the quick way. |
| GEN-13 | 你說慢一點 | 好的，我放慢說，請問您需要什麼協助？ | Sure, I'll slow down. How can I help? |
| GEN-14 | 再說一次 | 好的，我再說一次。 | Sure, let me repeat that. |
| GEN-15 | 大聲一點 | 好的。請問您需要列印、影印還是掃描？ | Okay. Printing, copying, or scanning? |
| GEN-16 | 無關列印的閒聊 | 不好意思，我主要協助列印、影印與掃描，需要時隨時問我。 | Sorry, I mainly help with printing, copying, and scanning—ask me anytime. |

---

## PM — print_mobile｜手機 / 雲端檔案列印（30）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| PM-01 | 我要印手機裡的檔案 | 好的，請拿手機掃描機台上的 QR Code，就能上傳檔案列印。 | Scan the QR code on the machine to upload and print. |
| PM-02 | QR Code 在哪裡 | QR Code 在機台螢幕或機身貼紙上，掃描後手機會打開上傳頁面。 | The QR code is on the screen or a sticker; scanning opens the upload page. |
| PM-03 | 支援什麼檔案格式 | 支援 PDF、Word、以及 JPG、PNG 圖片，建議先轉成 PDF 最穩定。 | We support PDF, Word, and JPG/PNG; PDF works best. |
| PM-04 | LINE 的檔案怎麼印 | 先在 LINE 把檔案存到手機，再掃 QR Code 從上傳頁選那個檔案。 | Save the file from LINE first, then upload after scanning the QR code. |
| PM-05 | 我要印照片 | 掃 QR Code 後選照片上傳，可以選彩色和尺寸再確認列印。 | Scan, upload your photo, pick color and size, then confirm. |
| PM-06 | 要選黑白還是彩色 | 上傳後在手機頁面可切換黑白或彩色，彩色費用較高。 | Switch black-and-white or color on your phone; color costs more. |
| PM-07 | 怎麼設定份數 | 在手機預覽頁面可調整份數，確認後再付款。 | Set the number of copies on the preview page, then pay. |
| PM-08 | 可以雙面印嗎 | 可以，在手機設定頁面選「雙面列印」即可。 | Yes—choose double-sided in the settings. |
| PM-09 | 紙張大小怎麼選 | 可選 A4 或 A3，在手機頁面的紙張設定切換。 | Choose A4 or A3 under paper settings. |
| PM-10 | 印之前可以先看嗎 | 可以，付款前手機會顯示預覽，確認沒問題再付款。 | Yes—you'll see a preview before paying. |
| PM-11 | 檔案太大傳不上去 | 檔案較大請稍等上傳完成，或先壓縮、分次上傳。 | For large files, wait or compress and split. |
| PM-12 | 上傳後找不到檔案 | 請確認上傳完成的提示，沒有的話重新掃 QR Code 再上傳一次。 | Check the upload-complete prompt; if missing, rescan and upload again. |
| PM-13 | 上傳完怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成即可。 | After the preview, tap pay and complete via mobile payment. |
| PM-14 | 印好的紙在哪裡拿 | 付款完成後紙張會從出紙匣送出，請到出紙口拿取。 | Collect your prints from the output tray after payment. |
| PM-15 | 可以一次印很多檔案嗎 | 可以，上傳頁面能加入多個檔案，會一起計算份數與價格。 | Yes—add multiple files; they're priced together. |
| PM-16 | Word 排版跑掉了 | Word 轉檔有時會位移，建議先轉成 PDF 再上傳最準確。 | Word layout can shift; convert to PDF first. |
| PM-17 | 手機沒網路怎麼辦 | 請開啟手機行動網路，或連線店內提供的網路後再掃 QR Code。 | Turn on mobile data or join the in-store network, then scan. |
| PM-18 | 上傳到一半想取消 | 直接關閉手機頁面即可取消，未付款不會列印也不會收費。 | Just close the page to cancel; nothing prints or charges before payment. |
| PM-19 | 可以縮放或滿版嗎 | 在手機設定可選縮放或滿版列印，預覽會即時更新。 | Choose scaling or fit-to-page; the preview updates instantly. |
| PM-20 | 列印怎麼算錢 | 系統會依頁數、黑白或彩色、紙張大小自動計價，付款前會顯示金額。 | Price is by pages, color, and size; shown before payment. |
| PM-21 | 印一份要等多久 | 付款後通常幾秒到十幾秒就會出紙，份數多會久一點。 | Usually seconds after payment; more copies take longer. |
| PM-22 | 我的檔案會被留下來嗎 | 您的檔案只暫存在店內主機處理，列印後會自動清除，不會上傳雲端。 | Your file is processed in-store and cleared after printing—never uploaded. |
| PM-23 | 可以用平板印嗎 | 可以，平板一樣掃 QR Code 上傳即可。 | Yes—tablets can scan the QR code and upload too. |
| PM-24 | 電腦檔案可以印嗎 | 可以，把檔案傳到手機或用手機開雲端，再掃 QR Code 上傳。 | Yes—move it to your phone or open it from the cloud, then upload. |
| PM-25 | 雲端硬碟的檔案怎麼印 | 先在手機開啟雲端把檔案下載，再掃 QR Code 上傳。 | Download it from the cloud on your phone first, then upload. |
| PM-26 | Email 附件怎麼印 | 在手機把附件存下來，再掃 QR Code 從上傳頁選它。 | Save the attachment on your phone, then upload it. |
| PM-27 | 印簡報 / PPT | 支援，建議先轉成 PDF 再上傳，排版最穩。 | Supported—convert to PDF first for stable layout. |
| PM-28 | 印 Excel 表格 | 可以，建議先轉 PDF 並確認列印範圍再上傳。 | Yes—convert to PDF and check the print range first. |
| PM-29 | 網頁怎麼印 | 在手機把網頁存成 PDF，再掃 QR Code 上傳。 | Save the webpage as PDF on your phone, then upload. |
| PM-30 | 只想印其中幾頁 | 在手機預覽頁可選列印頁數範圍，再確認付款。 | Choose the page range on the preview, then pay. |

---

## CID — copy_id｜身分證 / 證件影印（18）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CID-01 | 我要影印身分證 | 請把證件放在玻璃面板上，蓋上蓋子，依畫面操作影印。 | Place your ID on the glass, close the lid, and follow the screen. |
| CID-02 | 正反面印同一張 | 可選「證件影印」模式，會把正反面合印在同一張紙上。 | Choose ID-copy mode to print both sides on one sheet. |
| CID-03 | 證件要放哪裡 | 放在玻璃面板左上角對齊標示線，印好再翻面印背面。 | Align to the top-left mark; flip to copy the back. |
| CID-04 | 健保卡 / 駕照可以印嗎 | 可以，健保卡、駕照都用同樣的證件影印方式。 | Yes—health cards and licenses use the same steps. |
| CID-05 | 護照怎麼印 | 護照翻到資料頁，平放在玻璃面板上影印即可。 | Open to the photo page and place it flat on the glass. |
| CID-06 | 可以放大嗎 | 可以，在畫面選放大或縮小比例後再影印。 | Yes—choose enlarge or reduce before copying. |
| CID-07 | 要黑白還是彩色 | 證件可選黑白或彩色，彩色費用較高。 | Choose black-and-white or color (color costs more). |
| CID-08 | 我要印好幾份 | 在畫面設定份數後再確認影印。 | Set the number of copies, then confirm. |
| CID-09 | 影印證件多少錢 | 系統會依黑白彩色與份數計價，畫面會顯示金額。 | Price depends on color and copies; shown on screen. |
| CID-10 | 影印也要先付款嗎 | 是的，系統會先預覽報價，付款後才印出。 | Yes—preview and price first, then it prints after payment. |
| CID-11 | 印出來歪歪的 | 請把證件對齊玻璃面板角落的標示線，再重印一次。 | Align to the corner mark and copy again. |
| CID-12 | 我有好幾張證件 | 可以一張一張放上去分別影印，或用證件影印模式逐張處理。 | Copy them one at a time or use ID-copy mode for each. |
| CID-13 | 印好的在哪拿 | 付款完成後請到機台出紙口拿取。 | Collect from the output tray after payment. |
| CID-14 | 證件影印要多久 | 通常幾秒就會出紙。 | Usually a few seconds. |
| CID-15 | 居留證可以印嗎 | 可以，居留證用證件影印方式操作即可。 | Yes—residence permits use ID-copy mode. |
| CID-16 | 學生證 / 員工證 | 可以，一樣用證件影印模式操作。 | Yes—student/staff cards use ID-copy mode too. |
| CID-17 | 證件要彩色才清楚 | 建議選彩色，畫面可切換，彩色費用較高。 | Color is clearer—switch on screen; color costs more. |
| CID-18 | 兩張證件印一張紙 | 用證件影印模式可把正反或兩張併在同一張。 | ID-copy mode can fit both on one sheet. |

---

## CPY — copy_doc｜一般文件影印（14）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CPY-01 | 我要影印文件 | 請把文件放上玻璃面板或送稿器，依畫面選影印。 | Place your document on the glass or feeder and follow the screen. |
| CPY-02 | 影印一疊文件 | 用上方送稿器一次放多張，依畫面開始影印。 | Use the top feeder for multiple pages and start. |
| CPY-03 | 影印書本 | 把書翻開壓在玻璃面板上，輕壓蓋子再影印。 | Open the book on the glass, press gently, and copy. |
| CPY-04 | 放大影印 | 在畫面選放大比例後影印。 | Choose an enlarge ratio, then copy. |
| CPY-05 | 縮小影印 | 在畫面選縮小比例後影印。 | Choose a reduce ratio, then copy. |
| CPY-06 | A4 印成 A3 | 在畫面選放大到 A3 即可。 | Choose enlarge to A3. |
| CPY-07 | 雙面影印 | 用送稿器並在畫面選雙面影印。 | Use the feeder and select double-sided. |
| CPY-08 | 影印彩色 | 在畫面選彩色，彩色費用較高。 | Choose color on screen; color costs more. |
| CPY-09 | 影印多份 | 在畫面設定份數後確認。 | Set copies on screen, then confirm. |
| CPY-10 | 影印多少錢 | 依黑白彩色、紙張與份數計價，畫面會顯示金額。 | Priced by color, paper, and copies; shown on screen. |
| CPY-11 | 印出來太黑 / 太淡 | 在畫面調整濃淡後重印。 | Adjust the darkness on screen and copy again. |
| CPY-12 | 只印中間一部分 | 可放大該區域或調整擺放位置再影印。 | Enlarge that area or reposition, then copy. |
| CPY-13 | 原稿拿回去了嗎 | 影印後請記得從玻璃面板或送稿器取回原稿。 | Remember to take your original from the glass or feeder. |
| CPY-14 | 影印要先付款嗎 | 是的，畫面會先報價，付款後印出。 | Yes—price shows first, then it prints after payment. |

---

## SCN — scan｜掃描到 Email / USB（18）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| SCN-01 | 我要掃描文件 | 請把文件放上玻璃面板或送稿器，在畫面選掃描方式。 | Place your document on the glass or feeder and choose a scan option. |
| SCN-02 | 我要掃描到信箱 | 選「掃描到 Email」，輸入您的信箱，掃描後檔案會寄過去。 | Choose Scan-to-Email, enter your address, and it's sent. |
| SCN-03 | 我要掃到 USB | 選「掃描到 USB」，把隨身碟插進機台插槽再開始掃描。 | Choose Scan-to-USB and insert your drive. |
| SCN-04 | USB 插哪裡 | USB 插槽在機台前方面板上，插好畫面會顯示已偵測。 | The USB port is on the front panel; the screen confirms it. |
| SCN-05 | Email 沒收到 | 請確認信箱輸入正確並查看垃圾信件匣，必要時重新掃描寄送。 | Check the address and spam folder, then resend if needed. |
| SCN-06 | 可以掃很多頁嗎 | 可以，用上方送稿器一次放多張，會合成一個檔案。 | Yes—use the feeder; pages combine into one file. |
| SCN-07 | 掃彩色還是黑白 | 可在畫面選彩色或黑白掃描。 | Choose color or black-and-white on screen. |
| SCN-08 | 掃成 PDF 還是圖片 | 可選 PDF 或 JPG，多頁文件建議選 PDF。 | Choose PDF or JPG; PDF for multi-page. |
| SCN-09 | 原稿放哪 | 單張放玻璃面板，多張放上方送稿器。 | Single on the glass; multiple in the feeder. |
| SCN-10 | 掃描要錢嗎 | 掃描費用依機台設定，畫面會顯示是否收費與金額。 | Scan fees depend on the machine; shown on screen. |
| SCN-11 | 可以調解析度嗎 | 可以，在畫面選解析度，越高檔案越大。 | Yes—choose resolution; higher means larger files. |
| SCN-12 | 可以雙面掃嗎 | 可以，用送稿器並在畫面選雙面掃描。 | Yes—use the feeder and select double-sided. |
| SCN-13 | 檔案太大寄不出去 | 請降低解析度或分次掃描，檔案會比較小。 | Lower the resolution or split the scan. |
| SCN-14 | 掃描的檔案會留著嗎 | 掃描檔只暫存於店內主機，完成寄送或存檔後即清除，不上雲。 | Scans are processed in-store and cleared after sending. |
| SCN-15 | 掃描到手機可以嗎 | 可選掃描到 Email，再用手機收信即可。 | Use Scan-to-Email and open it on your phone. |
| SCN-16 | 掃描存成一個檔 | 多頁用送稿器會合成一個 PDF。 | Multiple pages in the feeder combine into one PDF. |
| SCN-17 | 掃描書本 | 把書翻開壓在玻璃面板上逐頁掃描。 | Open the book on the glass and scan page by page. |
| SCN-18 | 掃完可以改檔名嗎 | 可在寄送前依畫面設定檔名或主旨。 | Set the file name or subject before sending. |

---

## FN — advanced_func｜進階功能（16）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| FN-01 | 可以裝訂嗎 / 釘起來 | 是否提供裝訂以機台功能與畫面為準，請依畫面選擇。 | Stapling depends on the machine; check the on-screen options. |
| FN-02 | 騎馬釘 / 做成冊子 | 是否支援小冊子列印以畫面顯示為準。 | Booklet printing depends on the screen options. |
| FN-03 | 打洞 | 是否提供打洞以機台設定為準，請看畫面選項。 | Hole-punching depends on the machine; check on screen. |
| FN-04 | 印海報 / 大張 | 可選 A3 大尺寸列印，依畫面設定。 | Choose A3 for large prints on screen. |
| FN-05 | 印名片 | 可上傳名片檔列印，建議用 PDF 並設定尺寸。 | Upload a card file as PDF and set the size. |
| FN-06 | 護貝 | 不好意思，是否提供護貝請參考現場告示。〔需店家確認〕 | Sorry—please check the in-store notice for lamination. |
| FN-07 | 裁切 | 是否提供裁切請參考現場告示。〔需店家確認〕 | Cutting service: please check the in-store notice. |
| FN-08 | 合併多個 PDF | 上傳頁面可加入多個檔案一起列印。 | Add multiple files on the upload page to print together. |
| FN-09 | 加浮水印 | 系統不提供浮水印，建議在原檔處理好再上傳。 | No watermark feature—add it to your file first. |
| FN-10 | 印黑白省錢 | 在設定選黑白即可，費用較彩色低。 | Choose black-and-white to save; it's cheaper than color. |
| FN-11 | 一頁印多頁 / 多合一 | 部分機型支援多合一，請看畫面設定。 | Some machines support N-up; check on-screen settings. |
| FN-12 | 自動雙面 | 在設定選雙面列印即可。 | Choose double-sided in settings. |
| FN-13 | 印信封 | 一般機台不支援信封，建議改印標籤再貼上。 | Envelopes aren't supported; print a label instead. |
| FN-14 | 印貼紙 / 標籤紙 | 是否提供特殊紙材請參考現場告示。〔需店家確認〕 | Special media: please check the in-store notice. |
| FN-15 | 縮放到指定比例 | 在設定輸入縮放比例，預覽會更新。 | Enter a scaling ratio in settings; the preview updates. |
| FN-16 | 邊界 / 滿版列印 | 在設定選滿版或保留邊界。 | Choose full-bleed or margins in settings. |

---

## SUP — supplies｜紙張 / 耗材 / 品質（14）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| SUP-01 | 有 A3 嗎 | 有，列印或影印時在畫面選 A3。 | Yes—choose A3 when printing or copying. |
| SUP-02 | 有相片紙嗎 | 是否提供相片紙請參考現場告示。〔需店家確認〕 | Photo paper: please check the in-store notice. |
| SUP-03 | 紙張厚度 / 磅數 | 一般為普通影印紙，特殊磅數請參考現場告示。〔需店家確認〕 | Standard paper; for special weights see the in-store notice. |
| SUP-04 | 有彩色嗎 | 有，列印影印都可選彩色，費用較高。 | Yes—color is available; it costs more. |
| SUP-05 | 紙質不好 | 若對紙質有疑問，可改用旁邊另一台機器試印。 | If unsatisfied, try one of the other machines. |
| SUP-06 | 可以用我自己的紙嗎 | 不好意思，機台使用內建紙張，無法放自備紙張。 | Sorry—machines use built-in paper; you can't load your own. |
| SUP-07 | 顏色很淡 / 沒碳粉 | 若列印偏淡，建議改用旁邊另一台機器。 | If prints are faded, use one of the other machines. |
| SUP-08 | 紙用完會自動補嗎 | 缺紙時可依螢幕指示補紙，或改用旁邊另一台機器。 | Refill per on-screen steps, or use another machine. |
| SUP-09 | 怎麼印品質比較好 | 用 PDF 上傳並選彩色，品質較穩定。 | Upload PDF and choose color for stable quality. |
| SUP-10 | 紙卡卡的 / 皺 | 紙張異常請改用旁邊另一台機器。 | If paper is faulty, use one of the other machines. |
| SUP-11 | 雙面會不會透 | 一般影印紙雙面略有透色屬正常。 | Slight show-through on standard paper is normal. |
| SUP-12 | 最大印到多大 | 一般最大為 A3。 | The maximum is usually A3. |
| SUP-13 | 最小印到多小 | 可縮小列印，依畫面設定比例。 | You can reduce; set the ratio on screen. |
| SUP-14 | 有哪些紙張尺寸 | 常見為 A4 與 A3，畫面可選。 | A4 and A3 are available on screen. |

---

## PAY — payment｜付款操作（22）

> 過渡期：付款後沒出紙 → 導「改用另一台重印、不扣款」，**不承諾現場退款**；退款入口（D-A）上線後再開放。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| PAY-01 | 怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成。 | After the preview, tap pay and complete via mobile payment. |
| PAY-02 | 可以用什麼付款 | 機台支援掃碼與電子支付，實際方式以付款畫面為準。 | QR and mobile payments; see the payment screen. |
| PAY-03 | 可以用 LINE Pay 嗎 | 若付款畫面有顯示該選項即可使用，依畫面掃碼付款。 | If shown on the screen, yes—just scan to pay. |
| PAY-04 | 可以刷悠遊卡嗎 | 是否支援以付款畫面為準，請依畫面選擇方式。 | Whether supported is shown on the payment screen. |
| PAY-05 | 可以刷卡嗎 | 信用卡是否支援以付款畫面為準，依畫面操作即可。 | Card support is shown on the payment screen. |
| PAY-06 | 可以投現金嗎 | 是否收現金以機台設定為準，畫面會顯示可用方式。 | Cash depends on the machine; the screen shows methods. |
| PAY-07 | 付款了卻沒出紙 | 請先確認出紙匣並稍等約 30 秒；若仍沒出紙，請直接改用旁邊另一台機器重印，未完成的列印不會扣款。 | Check the tray and wait ~30s; if nothing prints, reprint on another machine—unfinished jobs aren't charged. |
| PAY-08 | 我好像被扣兩次 | 不好意思造成困擾；目前現場無法直接處理重複扣款，請先保留交易紀錄，線上退款申請功能即將開放。 | Sorry—double charges can't be handled on-site yet; keep your record, online refunds are coming soon. |
| PAY-09 | 付款失敗 | 請稍候再試一次，或換一種付款方式；也可以改用旁邊另一台機器。 | Try again or another method; you can also use another machine. |
| PAY-10 | 付款的 QR 在哪 | 確認預覽後，付款 QR 會顯示在手機或機台畫面上。 | After the preview, the payment QR appears on your phone or screen. |
| PAY-11 | 有收據或發票嗎 | 電子發票或收據會依畫面顯示，您可以在手機操作頁面查看。 | E-receipts appear on screen; view them on the phone page. |
| PAY-12 | 金額好像不對 | 金額依頁數、彩色與紙張自動計算，付款前畫面會先顯示；有疑問請保留交易紀錄。 | The amount is auto-calculated and shown before payment; keep your record if in doubt. |
| PAY-13 | 付到一半中斷了 | 未完成付款不會列印也不會扣款，請重新操作一次。 | An incomplete payment won't print or charge; start again. |
| PAY-14 | 我要退款 | 不好意思，若付款後沒印出來，您可以改用旁邊另一台機器重印，未完成不扣款；線上退款申請即將開放。 | Sorry—if a paid job didn't print, reprint on another machine (no charge); online refunds coming soon. |
| PAY-15 | 有找零或低消嗎 | 相關規則以畫面與機台設定為準，操作前畫面會顯示金額。 | Change and minimums follow the machine; the amount shows first. |
| PAY-16 | 付款後多久會印 | 付款成功後通常幾秒內就會開始出紙。 | Printing starts within seconds after payment. |
| PAY-17 | 可以開統編嗎 | 電子發票可否開統編以付款畫面為準，請依畫面輸入。 | Business numbers depend on the payment screen; enter as shown. |
| PAY-18 | 有最低消費嗎 | 相關規則以畫面與機台設定為準。 | Minimum-charge rules follow the machine settings. |
| PAY-19 | 可以分開付嗎 | 一次列印以一筆計費，請依畫面金額付款。 | Each job is one charge; pay the amount shown. |
| PAY-20 | 付款畫面卡住 | 請稍候重整或重新操作；也可改用旁邊另一台機器。 | Wait and retry, or use one of the other machines. |
| PAY-21 | 我掃不到付款碼 | 請對準畫面付款 QR，或換個角度；仍不行可改用另一台。 | Align with the payment QR or change angle; or use another machine. |
| PAY-22 | 付完可以改份數嗎 | 付款後無法更改，如需調整請重新操作。 | Can't change after payment; start over to adjust. |

---

## INV — invoice｜發票 / 收據（10）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| INV-01 | 有發票嗎 | 系統開立電子發票，會依畫面顯示。 | We issue e-invoices, shown on screen. |
| INV-02 | 我要紙本發票 | 為電子發票，可在手機操作頁面查看，依畫面說明處理。 | It's an e-invoice—view it on the phone page. |
| INV-03 | 載具怎麼設 | 電子發票可依畫面設定載具或輸入手機條碼。 | Set a carrier or enter your phone barcode on screen. |
| INV-04 | 統一編號 | 可否輸入統編以付款畫面為準，請依畫面操作。 | Entering a business number depends on the payment screen. |
| INV-05 | 發票中獎怎麼領 | 電子發票中獎依財政部規定，請依載具或通知處理。 | E-invoice prizes follow government rules via your carrier. |
| INV-06 | 收據在哪 | 收據或交易明細會依畫面顯示。 | Receipts and details show on screen. |
| INV-07 | 發票寄到哪 | 電子發票存於載具，可依設定查詢。 | E-invoices are stored on your carrier. |
| INV-08 | 可以捐發票嗎 | 可否捐贈以畫面選項為準。 | Donation depends on the on-screen options. |
| INV-09 | 重印發票 | 電子發票可依載具查詢，現場不另印紙本。 | E-invoices are on your carrier; no on-site reprint. |
| INV-10 | 發票金額不對 | 金額依實際列印計算；有疑問請保留交易紀錄。 | The amount reflects actual printing; keep your record if in doubt. |

---

## ERR — machine_error｜機台狀況（20）

> 自助優先：①依機台螢幕圖示自行排除/加紙 ②**改用店內另外兩台機器**（未完成不扣款）。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| ERR-01 | 卡紙了 | 請依機台螢幕圖示打開紙匣、取出卡住的紙張即可；不想自行處理，旁邊還有另外兩台可直接用，未完成不扣款。 | Follow the on-screen diagram to clear the jam, or use the other two machines—unfinished jobs aren't charged. |
| ERR-02 | 沒紙了 | 請依機台螢幕指示打開紙匣補充紙張；或直接改用旁邊另一台，未完成不扣款。 | Refill paper per the screen, or use another machine—no charge for unfinished jobs. |
| ERR-03 | 印出來是空白的 | 通常是檔案或設定問題，請檢查原始檔案後重印，或改用旁邊另一台試試。 | Usually a file/setting issue—check and reprint, or try another machine. |
| ERR-04 | 印出來有條紋很髒 | 列印品質不佳時，建議直接改用旁邊另一台機器。 | For poor quality, use one of the other machines. |
| ERR-05 | 機器沒反應 / 當機 | 請直接改用旁邊另一台機器操作，未完成的訂單不會扣款。 | Use one of the other machines—unfinished jobs aren't charged. |
| ERR-06 | 螢幕黑掉了 | 這台螢幕沒反應時，請改用旁邊另一台機器。 | If the screen is dead, use one of the other machines. |
| ERR-07 | 印到一半停住 | 請稍候幾秒；若沒有恢復，可改用旁邊另一台重印。 | Wait a few seconds; if it doesn't resume, reprint on another machine. |
| ERR-08 | 顏色很淡 / 沒碳粉 | 列印偏淡時，建議改用旁邊另一台機器。 | If faded, use one of the other machines. |
| ERR-09 | 我可以自己拉紙嗎 | 可以，請依螢幕圖示慢慢取出卡紙，不要硬拉；不確定就改用旁邊另一台。 | Yes—follow the diagram and gently remove it; if unsure, use another machine. |
| ERR-10 | 紙要怎麼補 | 請依機台螢幕指示打開紙匣，放入紙張即可。 | Follow the on-screen steps to open the tray and add paper. |
| ERR-11 | 我印錯了 | 已印出的內容無法收回；如需重印請重新操作，或改用旁邊另一台。 | Printed pages can't be undone; reprint here or on another machine. |
| ERR-12 | 機器有怪聲音 | 機台有異常聲響時，請停止使用這台，改用旁邊另一台。 | If it makes odd noises, stop and switch to another machine. |
| ERR-13 | 蓋子 / 送稿器卡住 | 請依螢幕指示輕輕復位，不要強行扳動；不確定就改用旁邊另一台。 | Follow the screen to gently reset it; if unsure, use another machine. |
| ERR-14 | 機器壞掉了 | 這台無法使用時，請直接改用旁邊另一台，未完成不扣款。 | If it's broken, use one of the other machines—no charge for unfinished jobs. |
| ERR-15 | 出紙口卡住 | 請依螢幕指示輕輕取出，不要硬拉；不確定改用旁邊另一台。 | Gently remove it per the screen; if unsure, use another machine. |
| ERR-16 | 印一半沒紙了 | 依螢幕補紙後可續印，或改用旁邊另一台重印。 | Refill to continue, or reprint on another machine. |
| ERR-17 | 螢幕觸控沒反應 | 請改用旁邊另一台機器操作。 | Use one of the other machines. |
| ERR-18 | 機器一直轉沒動作 | 請稍候；若沒反應改用旁邊另一台，未完成不扣款。 | Wait; if nothing happens, use another machine—no charge. |
| ERR-19 | 印出來歪斜 | 文件或證件請對齊標示線；或改用旁邊另一台重印。 | Align to the marks, or reprint on another machine. |
| ERR-20 | 重複印了好幾張 | 請檢查份數設定，確認份數後再重印。 | Check the copy count and reprint after confirming. |

---

## LOC — store_info｜店務 / 環境資訊（18）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| LOC-01 | 幾點營業 | 營業時間請參考門口或機台告示。〔需店家確認〕 | Hours are posted at the door or on the machine. |
| LOC-02 | 開到幾點 | 請參考門口或機台上的營業時間告示。〔需店家確認〕 | Closing time is posted at the door or machine. |
| LOC-03 | 假日有開嗎 | 請參考門口告示的營業時間。〔需店家確認〕 | Holiday hours are posted at the door. |
| LOC-04 | 地址在哪 | 地址請參考門口告示或您的地圖定位。〔需店家確認〕 | The address is on the door notice or your map app. |
| LOC-05 | 怎麼去 / 在哪裡 | 位置請參考您手機的地圖定位。 | Please check your map app for the location. |
| LOC-06 | 有停車位嗎 | 停車資訊請參考門市現場告示。〔需店家確認〕 | Parking info is on the in-store notice. |
| LOC-07 | 可以停哪 | 停車請參考周邊路邊或附近停車場，詳情見現場告示。〔需店家確認〕 | Use nearby street or lot parking; see the in-store notice. |
| LOC-08 | 有廁所嗎 | 不好意思，本店是無人門市，沒有提供廁所與洗手設備。 | Sorry—this unmanned store has no restroom or handwashing. |
| LOC-09 | 可以洗手嗎 | 不好意思，本店沒有提供洗手設備。 | Sorry—no handwashing facilities here. |
| LOC-10 | 有 wifi 嗎 | 請使用手機行動網路；店內是否提供網路請參考現場告示。〔需店家確認〕 | Use mobile data; in-store network info is on the notice. |
| LOC-11 | 有冷氣嗎 | 環境相關以現場為準。 | Please refer to the on-site environment. |
| LOC-12 | 有幾台機器 | 本店有三台機器，可任選使用。 | There are three machines; use any of them. |
| LOC-13 | 哪一台比較好 | 三台功能相同，任選一台即可；某台有狀況可換另一台。 | All three are the same; switch if one has an issue. |
| LOC-14 | 有監視器嗎 | 店內設有監視以維護安全，影像僅作安全用途。 | There's security monitoring for safety only. |
| LOC-15 | 可以坐著休息嗎 | 本店為自助操作空間，沒有休息座位。 | This is a self-service space with no seating. |
| LOC-16 | 有賣文具嗎 | 不好意思，本店只提供列印、影印與掃描，不販售文具。 | Sorry—we only offer printing, copying, and scanning. |
| LOC-17 | 可以換零錢嗎 | 不好意思，本店不提供換鈔，付款請用畫面顯示的方式。 | Sorry—no change service; pay via the on-screen methods. |
| LOC-18 | 有飲水機嗎 | 不好意思，本店沒有提供飲水設備。 | Sorry—no water facilities here. |

---

## HLP — human_help｜需要協助（12）

> 無人門市：語音引導操作為主；不導真人。

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| HLP-01 | 有沒有人可以幫我 | 這是無人自助門市，我可以直接引導您操作，請告訴我您的需求。 | This is a self-service store—I can guide you; tell me what you need. |
| HLP-02 | 哪裡有更多說明 | 機台螢幕都有操作指引，我也可以一步步引導您。 | The screen has guidance, and I can walk you through it. |
| HLP-03 | 你們幾點營業 | 營業時間請參考門口或機台上的告示。〔需店家確認〕 | Hours are posted at the door or on the machine. |
| HLP-04 | 現場都沒有店員嗎 | 對，這是無人門市，全部自助操作，我可以引導您。 | Yes—it's fully self-service, and I can help guide you. |
| HLP-05 | 我不會用，可以教我嗎 | 沒問題，請告訴我您要列印、影印還是掃描，我一步步引導您。 | Of course—tell me what you need and I'll guide you step by step. |
| HLP-06 | 我遇到緊急狀況 | 若是火災、有人受傷等緊急狀況，請立即撥打 119 或 110。 | For a fire or injury, call 119 or 110 immediately. |
| HLP-07 | 廁所 / 洗手 / 其他問題 | 不好意思，本店是無人門市，沒有提供廁所與洗手設備；其他問題請參考現場告示。 | Sorry—no restroom or handwashing; for other questions see the in-store notices. |
| HLP-08 | 我已經試很多次了 | 不好意思造成不便，您可以改用旁邊另一台機器，未完成不扣款。 | Sorry for the trouble—use another machine; unfinished jobs aren't charged. |
| HLP-09 | 我看不懂螢幕 | 沒問題，告訴我您要列印、影印還是掃描，我一步步帶您。 | No problem—tell me what you need and I'll guide you. |
| HLP-10 | 卡在付款這一步 | 確認預覽後依畫面付款；卡住可重新操作或改用旁邊另一台。 | Pay per the screen after the preview; if stuck, retry or use another machine. |
| HLP-11 | 我東西不見了 | 請檢查出紙口與玻璃面板、送稿器是否留下原稿或成品。 | Check the output tray, glass, and feeder for your original or prints. |
| HLP-12 | 操作太複雜 | 別擔心，跟著螢幕步驟走，需要時我可以一步步引導您。 | Don't worry—follow the screen, and I can guide you step by step. |

---

## CMP — complaint｜客訴 / 抱怨（12）

> 過渡期：付款後沒印好 → 導重印不扣款；費用爭議 → 致歉＋保留交易紀錄＋告知線上申請即將開放。**不導真人、不承諾賠償。**

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| CMP-01 | 我被亂扣錢 | 不好意思造成困擾；目前現場無法直接處理扣款爭議，請先保留交易紀錄，線上退款申請即將開放。 | Sorry—charge disputes can't be handled on-site yet; keep your record, online refunds coming soon. |
| CMP-02 | 我要退費 | 不好意思，若付款後沒印出來，可改用旁邊另一台重印，不扣款；線上退款申請即將開放。 | Sorry—if a paid job didn't print, reprint on another machine (no charge); online refunds coming soon. |
| CMP-03 | 這台爛死了不能用 | 很抱歉造成不便，您可以直接改用旁邊另一台機器，未完成不扣款。 | Sorry—please use one of the other machines; unfinished jobs aren't charged. |
| CMP-04 | 印壞了你要賠我 | 很抱歉，若付款後沒印好，可改用旁邊另一台重印，不扣款；線上退款申請即將開放。 | Sorry—if a paid job printed badly, reprint on another machine (no charge); online refunds coming soon. |
| CMP-05 | 浪費我時間 | 很抱歉耽誤您的時間，您可以直接改用旁邊另一台機器，未完成不扣款。 | Sorry for the delay—use one of the other machines; unfinished jobs aren't charged. |
| CMP-06 | 我要客訴 / 投訴 | 了解，您的意見對我們很重要；線上意見回報功能即將開放，屆時可留下意見。 | Understood—your feedback matters; an online channel is coming soon. |
| CMP-07 | 我要找負責人 | 這是無人門市現場沒有專人；線上聯絡功能即將開放，屆時可留下聯絡方式。 | This is unmanned with no staff; an online contact channel is coming soon. |
| CMP-08 | 你們服務很差 | 很抱歉讓您有不好的體驗，我們會持續改進；線上意見回報即將開放。 | Sorry for the poor experience—we'll improve; an online channel is coming soon. |
| CMP-09 | 等很久很煩 | 很抱歉久候，您可以改用旁邊另一台機器，未完成不扣款。 | Sorry for the wait—use one of the other machines; no charge for unfinished jobs. |
| CMP-10 | 機器很難用 | 抱歉造成不便，告訴我您卡在哪，我帶您操作。 | Sorry—tell me where you're stuck and I'll guide you. |
| CMP-11 | 我投訴都沒人理 | 本店為無人門市；線上意見回報功能即將開放，屆時可留言反映。 | This is unmanned; an online feedback channel is coming soon. |
| CMP-12 | 你們會偷看我檔案嗎 | 不會，檔案只在店內主機處理，完成後自動清除，不會上雲。 | No—files are processed in-store, cleared after, and never uploaded. |

---

## PRIV — privacy｜隱私 / 資料安全（6）

| id | trigger | 中文引導（TTS） | English |
|---|---|---|---|
| PRIV-01 | 我的檔案安全嗎 | 檔案只暫存店內主機，列印後自動清除，不會上雲。 | Files are processed in-store and cleared after printing—never uploaded. |
| PRIV-02 | 掃描的會被留嗎 | 掃描檔完成寄送或存檔後即清除，不上雲。 | Scans are cleared after sending—never uploaded. |
| PRIV-03 | 會記錄我印什麼嗎 | 系統不保留您的檔案內容，列印後即清除。 | We don't keep your file content; it's cleared after printing. |
| PRIV-04 | 監視器會拍到我的檔案嗎 | 監視僅作環境安全用途，不針對您的檔案內容。 | Monitoring is for safety only, not your file content. |
| PRIV-05 | 證件影印安全嗎 | 證件影像只在店內處理，完成後清除，不上雲。 | ID images are processed in-store and cleared—never uploaded. |
| PRIV-06 | 個資會外洩嗎 | 您的檔案不上雲、完成即清除，請放心。 | Your files never go to the cloud and are cleared after use. |

---

### 統計（v0.4）

| intent / 群組 | 句數 |
|---|---|
| SYS 系統句 | 4 |
| GEN 一般對話 | 16 |
| print_mobile 手機列印 | 30 |
| copy_id 證件影印 | 18 |
| copy_doc 一般影印 | 14 |
| scan 掃描 | 18 |
| advanced_func 進階功能 | 16 |
| supplies 紙張耗材 | 14 |
| payment 付款 | 22 |
| invoice 發票收據 | 10 |
| machine_error 機台狀況 | 20 |
| store_info 店務資訊 | 18 |
| human_help 求助 | 12 |
| complaint 客訴 | 12 |
| privacy 隱私 | 6 |
| **合計** | **230** |

### 需店家確認 / 現場張貼的事實（語句中標 `〔需店家確認〕`）
1. 營業時間（平日/假日/結束時間）— LOC-01/02/03、HLP-03
2. 地址與位置 — LOC-04
3. 停車資訊 — LOC-06/07
4. 店內是否提供 wifi/網路 — LOC-10、PM-17
5. 是否提供護貝/裁切/特殊紙材/相片紙/特殊磅數 — FN-06/07/14、SUP-02/03
6. 發票統編/載具/捐贈等細項是否開放 — INV-04/08、PAY-17

### v0.4 擴充摘要
- 由 100 句擴到 **230 句**，新增 GEN(招呼互動)、CPY(一般影印)、FN(進階功能)、SUP(紙張耗材)、INV(發票)、LOC(店務環境)、PRIV(隱私) 七個常用會話群組，並補各類口語/台味變體。
- **收錄範圍限定 iPrintOS 無人門市相關**：與營業無關的閒聊（年齡/時間/天氣/純聊天）不收，無關發問由 GEN-16 拉回主題。
- 全程沿用既定決策：自助優先、不靠真人、退款過渡(1B)、三台機器、無廁所/洗手、檔案不上雲、永遠回最接近一句。
- 系統負擔評估見規劃文件 §13：句數對效能影響可忽略。
