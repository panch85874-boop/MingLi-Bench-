# iPrintOS 語音引導語庫｜中英越印四語（v0.5 · 237 句 · 中／英／越南文／印尼文）

> 用途：語音助理**比對後要播給客人的固定引導語**（封閉問答庫的答案側）。
> 對應規劃文件 `iPrintOS_語音PoC_工程規劃.md`。
> **核心原則：無人店「自助優先、不靠真人」。** ①依機台螢幕自助 ②**改用店內另外兩台機器**（三台、每台間隔約 1 公尺、未完成不扣款）③檔案只在店內主機處理、完成即清除 ④唯一外部聯絡為火災/受傷 → 119/110。**全程不導真人客服電話。**
> **比對邏輯：模糊語意比對，永遠回最接近的一句**（不設門檻、無「沒資料」回覆）；只有完全沒聽到語音才請客人再說一次。
> **退款過渡（決策 1B）**：付款後沒印好 → 只導「改用另一台重印、不扣款」，**不承諾現場退款**；扣款爭議 → 致歉＋請客人保留交易紀錄＋告知線上申請即將開放。退款自助入口（D-A）為待開發。
> **收錄範圍：只收與 iPrintOS 無人門市相關的會話**——列印/影印/掃描/付款/發票/機台/紙張耗材/店務環境/隱私/招呼互動。**與營業無關的閒聊（如年齡、天氣、時間、純聊天）一律不收**；客人若講無關的話，由 GEN-16 統一拉回列印主題。
> 原則：每句簡短（口語、適合 TTS）；模型只從本庫選句、不自由生成。實作轉成 `config/guidance.jsonl`：`guidance_id, intent, triggers[], tts_zh, tts_en, tts_vi, tts_id`。
> **多語（v0.5）**：新增 **Tiếng Việt（越南文）/ Bahasa Indonesia（印尼文）** 兩欄；其中 169 句沿用對外 FAQ 翻譯（`data/faq_content.json`）以保持用詞一致，68 句（SYS/GEN 及措辭略異者）另行翻譯。
> **關聯**：對外 FAQ 同源四語資料於 `data/faq_content.json`；網頁由 `scripts/build_faq.py` 生成、Obsidian 對照筆記由 `scripts/build_faq_md.py` 生成。

---

## SYS — 系統句（問候 / 沒聽清楚 / 收尾）（4）

> 比對只要聽到問句就一定回最接近的一句；SYS-03/04 只用在**完全沒聽到語音**（no_speech）。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| SYS-01 | 偵測到有人進入 | 您好，歡迎光臨，需要我幫忙嗎？ | Hi, welcome. Do you need any help? | Xin chào, hoan nghênh quý khách. Quý khách cần tôi giúp gì không? | Halo, selamat datang. Ada yang bisa saya bantu? |
| SYS-02 | 客人以英文回應 | Hi! How can I help you with printing or copying today? | Hi! How can I help you with printing or copying today? | Xin chào! Hôm nay tôi có thể giúp bạn in hay sao chép gì không? | Halo! Hari ini saya bisa membantu Anda mencetak atau memfotokopi apa? |
| SYS-03 | 完全沒收到語音 / 純噪音 | 不好意思，我沒聽清楚，可以請您再說一次嗎？ | Sorry, I didn't catch that—could you say it again? | Xin lỗi, tôi nghe chưa rõ, bạn có thể nói lại một lần nữa không? | Maaf, saya kurang jelas mendengar, bisa diulang sekali lagi? |
| SYS-04 | 連續 2 次沒聽到 → 收尾 | 不好意思我還是沒聽清楚，您可以直接在機台螢幕操作。 | Sorry, I still didn't catch that—please use the on-screen menu. | Xin lỗi, tôi vẫn chưa nghe rõ. Quý khách có thể thao tác trực tiếp trên màn hình máy. | Maaf, saya masih kurang jelas mendengarnya. Silakan gunakan menu di layar mesin. |

---

## GEN — 一般對話 / 問候 / 互動（16）

> 只收與門市使用相關的招呼與互動控制；**與營業無關的閒聊（年齡、時間、純聊天）一律不收**。客人若講無關的話，由 GEN-16 統一拉回列印主題。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| GEN-01 | 你好 / 哈囉 | 您好，需要我幫您列印、影印還是掃描嗎？ | Hello! Do you need printing, copying, or scanning? | Xin chào, bạn cần tôi giúp in, sao chép hay quét không? | Halo, apakah Anda perlu saya bantu mencetak, memfotokopi, atau memindai? |
| GEN-02 | 謝謝 | 不客氣，祝您使用順利。 | You're welcome—enjoy! | Không có gì, chúc bạn dùng thuận lợi nhé. | Sama-sama, semoga lancar ya. |
| GEN-03 | 再見 / 掰掰 | 謝謝光臨，再見。 | Thanks for visiting, goodbye. | Cảm ơn quý khách đã ghé, hẹn gặp lại. | Terima kasih sudah berkunjung, sampai jumpa. |
| GEN-04 | 你是誰 | 我是這家自助影印店的語音助理，可以引導您操作。 | I'm the voice assistant for this self-service store—I can guide you. | Tôi là trợ lý giọng nói của tiệm photocopy tự phục vụ này, tôi có thể hướng dẫn bạn thao tác. | Saya asisten suara dari toko fotokopi swalayan ini, saya bisa memandu Anda. |
| GEN-05 | 你是機器人嗎 | 是的，我是語音助理，列印相關的問題都可以問我。 | Yes, I'm a voice assistant—ask me anything about printing. | Vâng, tôi là trợ lý giọng nói, mọi thắc mắc về in ấn cứ hỏi tôi nhé. | Ya, saya asisten suara, soal cetak apa saja boleh tanya saya. |
| GEN-06 | 你聽得懂中文嗎 | 可以，中文或英文都可以跟我說。 | Yes—you can speak to me in Chinese or English. | Được, quý khách có thể nói với tôi bằng tiếng Trung hoặc tiếng Anh. | Bisa, Anda boleh berbicara dengan saya dalam bahasa Mandarin atau Inggris. |
| GEN-07 | 你會說英文嗎 | 可以，英文也沒問題。 | Yes, I can help in English too. | Được chứ, tiếng Anh cũng không vấn đề gì. | Bisa, bahasa Inggris juga tidak masalah. |
| GEN-08 | 等我一下 / 我想一下 | 好的，您慢慢來，想好再跟我說。 | Sure, take your time. | Được, bạn cứ từ từ, nghĩ xong rồi nói với tôi nhé. | Baik, santai saja, kalau sudah siap beri tahu saya ya. |
| GEN-09 | 沒事了 / 不用了 | 好的，需要時再叫我。 | Okay, just call me if you need anything. | Vâng, khi cần thì cứ gọi tôi nhé. | Baik, panggil saya kapan saja Anda membutuhkan. |
| GEN-10 | 可以幫我嗎 | 當然，請問您要列印、影印還是掃描？ | Of course—printing, copying, or scanning? | Tất nhiên rồi, bạn muốn in, sao chép hay quét ạ? | Tentu saja, Anda ingin mencetak, memfotokopi, atau memindai? |
| GEN-11 | 我第一次用 | 沒問題，告訴我您要做什麼，我一步步帶您。 | No problem—tell me what you need and I'll guide you step by step. | Không sao, hãy cho tôi biết bạn cần gì, tôi sẽ hướng dẫn từng bước. | Tidak masalah, beri tahu apa yang Anda butuhkan, saya pandu langkah demi langkah. |
| GEN-12 | 我趕時間 | 了解，您要列印、影印還是掃描？我帶您最快的步驟。 | Got it—printing, copying, or scanning? I'll guide you the quick way. | Hiểu rồi. Quý khách muốn in, sao chép hay quét? Tôi sẽ hướng dẫn cách nhanh nhất. | Baik. Anda mau mencetak, fotokopi, atau memindai? Saya pandu cara tercepat. |
| GEN-13 | 你說慢一點 | 好的，我放慢說，請問您需要什麼協助？ | Sure, I'll slow down. How can I help? | Vâng, tôi sẽ nói chậm lại, bạn cần giúp gì ạ? | Baik, saya akan bicara lebih pelan, ada yang bisa saya bantu? |
| GEN-14 | 再說一次 | 好的，我再說一次。 | Sure, let me repeat that. | Được, tôi xin nói lại một lần nữa. | Baik, saya ulangi sekali lagi. |
| GEN-15 | 大聲一點 | 好的。請問您需要列印、影印還是掃描？ | Okay. Printing, copying, or scanning? | Vâng. Quý khách cần in, sao chép hay quét ạ? | Baik. Anda perlu mencetak, fotokopi, atau memindai? |
| GEN-16 | 無關列印的閒聊 | 不好意思，我主要協助列印、影印與掃描，需要時隨時問我。 | Sorry, I mainly help with printing, copying, and scanning—ask me anytime. | Xin lỗi, tôi chủ yếu giúp in, sao chép và quét, cần gì cứ hỏi tôi nhé. | Maaf, saya terutama membantu mencetak, memfotokopi, dan memindai, tanya saya kapan saja ya. |

---

## PM — print_mobile｜手機 / 雲端檔案列印（30）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| PM-01 | 我要印手機裡的檔案 | 好的，請拿手機掃描機台上的 QR Code，就能上傳檔案列印。 | Scan the QR code on the machine to upload and print. | Vâng, vui lòng dùng điện thoại quét mã QR trên máy để tải tệp lên và in. | Baik, silakan pindai kode QR di mesin dengan ponsel untuk mengunggah file dan mencetak. |
| PM-02 | QR Code 在哪裡 | QR Code 在機台螢幕或機身貼紙上，掃描後手機會打開上傳頁面。 | The QR code is on the screen or a sticker; scanning opens the upload page. | Mã QR ở trên màn hình máy hoặc nhãn dán trên thân máy; quét xong điện thoại sẽ mở trang tải lên. | Kode QR ada di layar mesin atau stiker di badan mesin; setelah dipindai, ponsel akan membuka halaman unggah. |
| PM-03 | 支援什麼檔案格式 | 支援 PDF 與 Word、Excel、PPT 等 Office 檔，免轉檔直接列印；也支援 JPG、PNG 圖片。單檔上限 150MB。 | We support PDF and Office files (Word, Excel, PPT)—no conversion needed—plus JPG/PNG images. Max 150MB per file. | Hỗ trợ PDF và tệp Office như Word, Excel, PPT, in trực tiếp không cần chuyển đổi; cũng hỗ trợ ảnh JPG, PNG. Mỗi tệp tối đa 150MB. | Mendukung PDF dan file Office (Word, Excel, PPT), cetak langsung tanpa konversi; juga mendukung gambar JPG, PNG. Maksimal 150MB per file. |
| PM-04 | LINE 的檔案怎麼印 | 先在 LINE 把檔案存到手機，再掃 QR Code 從上傳頁選那個檔案。 | Save the file from LINE first, then upload after scanning the QR code. | Trước tiên lưu tệp từ LINE vào điện thoại, rồi quét mã QR và chọn tệp đó từ trang tải lên. | Simpan dulu file dari LINE ke ponsel, lalu pindai kode QR dan pilih file itu di halaman unggah. |
| PM-05 | 我要印照片 | 掃 QR Code 後上傳照片，可選彩色與尺寸列印於一般紙張；本店不提供相片紙與照片沖印。 | Scan the QR, upload your photo, pick color and size to print on plain paper; we don't offer photo paper or photo developing. | Quét mã QR rồi tải ảnh lên, có thể chọn in màu và kích thước trên giấy thường; cửa hàng không cung cấp giấy ảnh và rửa ảnh. | Pindai kode QR lalu unggah foto, bisa pilih warna dan ukuran cetak di kertas biasa; toko tidak menyediakan kertas foto dan cetak foto. |
| PM-06 | 要選黑白還是彩色 | 上傳後在手機頁面可切換黑白或彩色，彩色費用較高。 | Switch black-and-white or color on your phone; color costs more. | Sau khi tải lên, trên trang điện thoại có thể chuyển giữa đen trắng hoặc màu; in màu có phí cao hơn. | Setelah diunggah, di halaman ponsel bisa beralih antara hitam-putih atau warna; cetak warna lebih mahal. |
| PM-07 | 怎麼設定份數 | 在手機預覽頁面可調整份數，確認後再付款。 | Set the number of copies on the preview page, then pay. | Trên trang xem trước ở điện thoại có thể điều chỉnh số bản, xác nhận xong rồi thanh toán. | Di halaman pratinjau ponsel bisa atur jumlah salinan, lalu konfirmasi dan bayar. |
| PM-08 | 可以雙面印嗎 | 可以，在手機設定頁面選「雙面列印」即可。 | Yes—choose double-sided in the settings. | Được, chọn "in 2 mặt" trên trang cài đặt ở điện thoại là được. | Bisa, pilih "cetak bolak-balik" di halaman pengaturan ponsel. |
| PM-09 | 紙張大小怎麼選 | 可選 A4 或 A3，在手機頁面的紙張設定切換。 | Choose A4 or A3 under paper settings. | Có thể chọn A4 hoặc A3, chuyển đổi ở phần cài đặt giấy trên trang điện thoại. | Bisa pilih A4 atau A3 di pengaturan kertas pada halaman ponsel. |
| PM-10 | 印之前可以先看嗎 | 可以，付款前手機會顯示預覽，確認沒問題再付款。 | Yes—you'll see a preview before paying. | Được, trước khi thanh toán điện thoại sẽ hiển thị bản xem trước, xác nhận không vấn đề rồi mới thanh toán. | Bisa, sebelum membayar ponsel akan menampilkan pratinjau, konfirmasi tidak ada masalah baru bayar. |
| PM-11 | 檔案太大傳不上去 | 檔案較大請稍等上傳完成，或先壓縮、分次上傳。 | For large files, wait or compress and split. | Tệp lớn vui lòng đợi tải lên xong, hoặc nén lại, tải theo nhiều lần. | Untuk file besar, tunggu hingga selesai diunggah, atau kompres dan unggah secara bertahap. |
| PM-12 | 上傳後找不到檔案 | 請確認上傳完成的提示，沒有的話重新掃 QR Code 再上傳一次。 | Check the upload-complete prompt; if missing, rescan and upload again. | Vui lòng kiểm tra thông báo tải lên hoàn tất; nếu không có, quét lại mã QR và tải lên một lần nữa. | Periksa pemberitahuan unggah selesai; jika tidak ada, pindai ulang kode QR dan unggah sekali lagi. |
| PM-13 | 上傳完怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成即可。 | After the preview, tap pay and complete via mobile payment. | Xác nhận bản xem trước rồi nhấn thanh toán, theo màn hình dùng thanh toán điện tử hoặc quét mã để hoàn tất. | Konfirmasi pratinjau lalu tekan bayar, ikuti layar dengan pembayaran elektronik atau pindai kode untuk menyelesaikan. |
| PM-14 | 印好的紙在哪裡拿 | 付款完成後紙張會從出紙匣送出，請到出紙口拿取。 | Collect your prints from the output tray after payment. | Sau khi thanh toán xong, giấy sẽ ra từ khay giấy, vui lòng lấy ở khe ra giấy. | Setelah pembayaran selesai, kertas akan keluar dari baki keluaran, silakan ambil di lubang keluaran kertas. |
| PM-15 | 可以一次印很多檔案嗎 | 可以，上傳頁面能加入多個檔案，會一起計算份數與價格。 | Yes—add multiple files; they're priced together. | Được, trang tải lên có thể thêm nhiều tệp, sẽ tính chung số bản và giá. | Bisa, halaman unggah dapat menambahkan beberapa file, jumlah salinan dan harga dihitung bersama. |
| PM-16 | Word 排版跑掉了 | Word 可免轉檔直接列印；若要排版完全一致，也可自行先轉成 PDF 再上傳。 | Word prints directly—no conversion needed; for an exact layout you may convert to PDF yourself first. | Word in trực tiếp không cần chuyển đổi; nếu muốn bố cục hoàn toàn khớp, bạn cũng có thể tự chuyển sang PDF rồi tải lên. | Word dicetak langsung tanpa konversi; jika ingin tata letak persis sama, Anda juga bisa mengubahnya ke PDF sendiri dulu lalu unggah. |
| PM-17 | 手機沒網路怎麼辦 | 掃機台 QR Code 上傳檔案時會自動連線傳檔，不需另外上網；其他用途請用手機行動網路。 | Scanning the QR auto-connects just to send your file—no internet needed; use mobile data for anything else. | Khi quét mã QR trên máy để tải tệp lên sẽ tự động kết nối gửi tệp, không cần lên mạng riêng; các nhu cầu khác vui lòng dùng mạng di động của điện thoại. | Saat memindai kode QR mesin untuk mengunggah file, akan otomatis terhubung untuk mengirim file, tidak perlu internet lain; untuk keperluan lain gunakan data seluler ponsel. |
| PM-18 | 上傳到一半想取消 | 直接關閉手機頁面即可取消，未付款不會列印也不會收費。 | Just close the page to cancel; nothing prints or charges before payment. | Chỉ cần đóng trang trên điện thoại là hủy được; chưa thanh toán thì sẽ không in và không thu phí. | Cukup tutup halaman di ponsel untuk membatalkan; sebelum dibayar tidak akan mencetak dan tidak dikenai biaya. |
| PM-19 | 可以縮放或滿版嗎 | 放大縮小提供少數固定倍率，也可選滿版或保留邊界，預覽會更新。 | Enlarge/reduce offers a few fixed ratios; you can also choose fit-to-page or margins—the preview updates. | Phóng to thu nhỏ có một số tỷ lệ cố định, cũng có thể chọn tràn lề hoặc giữ lề, bản xem trước sẽ cập nhật. | Pembesaran/pengecilan tersedia beberapa rasio tetap, juga bisa pilih penuh halaman atau pertahankan margin, pratinjau akan diperbarui. |
| PM-20 | 列印怎麼算錢 | 系統會依頁數、黑白或彩色、紙張大小自動計價，付款前會顯示金額。 | Price is by pages, color, and size; shown before payment. | Hệ thống sẽ tự tính giá theo số trang, đen trắng hay màu, khổ giấy; trước khi thanh toán sẽ hiển thị số tiền. | Sistem akan menghitung harga otomatis berdasarkan jumlah halaman, hitam-putih atau warna, dan ukuran kertas; jumlahnya ditampilkan sebelum pembayaran. |
| PM-21 | 印一份要等多久 | 付款後通常幾秒到十幾秒就會出紙，份數多會久一點。 | Usually seconds after payment; more copies take longer. | Sau khi thanh toán thường vài giây đến hơn chục giây sẽ ra giấy, nhiều bản thì lâu hơn một chút. | Setelah membayar biasanya beberapa detik hingga belasan detik kertas keluar, lebih banyak salinan agak lebih lama. |
| PM-22 | 我的檔案會被留下來嗎 | 您的檔案只暫存在店內主機處理，列印後會自動清除，不會上傳雲端。 | Your file is processed in-store and cleared after printing—never uploaded. | Tệp của bạn chỉ lưu tạm trên máy chủ trong cửa hàng để xử lý, in xong sẽ tự động xóa, không tải lên đám mây. | File Anda hanya disimpan sementara di server dalam toko untuk diproses, setelah dicetak akan otomatis dihapus, tidak diunggah ke cloud. |
| PM-23 | 可以用平板印嗎 | 可以，平板一樣掃 QR Code 上傳即可。 | Yes—tablets can scan the QR code and upload too. | Được, máy tính bảng cũng quét mã QR và tải lên là được. | Bisa, tablet juga cukup pindai kode QR dan unggah. |
| PM-24 | 電腦檔案可以印嗎 | 可以，把檔案傳到手機或用手機開雲端，再掃 QR Code 上傳。 | Yes—move it to your phone or open it from the cloud, then upload. | Được, chuyển tệp sang điện thoại hoặc mở đám mây trên điện thoại, rồi quét mã QR tải lên. | Bisa, pindahkan file ke ponsel atau buka dari cloud di ponsel, lalu pindai kode QR dan unggah. |
| PM-25 | 雲端硬碟的檔案怎麼印 | 先在手機開啟雲端把檔案下載，再掃 QR Code 上傳。 | Download it from the cloud on your phone first, then upload. | Trước tiên mở đám mây trên điện thoại để tải tệp xuống, rồi quét mã QR tải lên. | Buka cloud di ponsel dulu untuk mengunduh file, lalu pindai kode QR dan unggah. |
| PM-26 | Email 附件怎麼印 | 在手機把附件存下來，再掃 QR Code 從上傳頁選它。 | Save the attachment on your phone, then upload it. | Lưu tệp đính kèm vào điện thoại, rồi quét mã QR và chọn nó từ trang tải lên. | Simpan lampiran ke ponsel, lalu pindai kode QR dan pilih dari halaman unggah. |
| PM-27 | 印簡報 / PPT | 支援，PPT 可免轉檔直接列印。 | Supported—PPT prints directly, no conversion needed. | Có hỗ trợ, PPT in trực tiếp không cần chuyển đổi. | Didukung, PPT dicetak langsung tanpa konversi. |
| PM-28 | 印 Excel 表格 | 支援，Excel 可免轉檔直接列印，列印前可在畫面確認範圍。 | Supported—Excel prints directly; check the print range on screen first. | Có hỗ trợ, Excel in trực tiếp không cần chuyển đổi, trước khi in có thể xác nhận phạm vi trên màn hình. | Didukung, Excel dicetak langsung tanpa konversi, sebelum mencetak bisa cek rentang di layar dulu. |
| PM-29 | 網頁怎麼印 | 在手機把網頁存成 PDF，再掃 QR Code 上傳。 | Save the webpage as PDF on your phone, then upload. | Lưu trang web thành PDF trên điện thoại, rồi quét mã QR tải lên. | Simpan halaman web sebagai PDF di ponsel, lalu pindai kode QR dan unggah. |
| PM-30 | 只想印其中幾頁 | 在手機預覽頁可選列印頁數範圍，再確認付款。 | Choose the page range on the preview, then pay. | Trên trang xem trước ở điện thoại có thể chọn phạm vi trang cần in, rồi xác nhận thanh toán. | Di halaman pratinjau ponsel bisa pilih rentang halaman yang akan dicetak, lalu konfirmasi dan bayar. |

---

## CID — copy_id｜身分證 / 證件影印（18）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| CID-01 | 我要影印身分證 | 請把證件放在玻璃面板上，蓋上蓋子，依畫面操作影印。 | Place your ID on the glass, close the lid, and follow the screen. | Đặt giấy tờ lên mặt kính, đóng nắp lại và làm theo màn hình. | Letakkan dokumen di atas kaca, tutup penutupnya, lalu ikuti layar. |
| CID-02 | 正反面印同一張 | 可選「證件影印」模式，會把正反面合印在同一張紙上。 | Choose ID-copy mode to print both sides on one sheet. | Chọn chế độ "sao chép giấy tờ" để in cả hai mặt lên cùng một tờ giấy. | Pilih mode fotokopi dokumen untuk mencetak kedua sisi pada satu lembar. |
| CID-03 | 證件要放哪裡 | 放在玻璃面板左上角對齊標示線，印好再翻面印背面。 | Align to the top-left mark; flip to copy the back. | Đặt vào góc trên bên trái mặt kính theo vạch chỉ dẫn, in xong rồi lật mặt sau. | Sejajarkan dengan tanda kiri atas; balik untuk fotokopi sisi belakang. |
| CID-04 | 健保卡 / 駕照可以印嗎 | 可以，健保卡、駕照都用同樣的證件影印方式。 | Yes—health cards and licenses use the same steps. | Được, thẻ bảo hiểm y tế và bằng lái xe đều dùng cùng cách sao chép giấy tờ. | Bisa—kartu kesehatan dan SIM menggunakan langkah yang sama. |
| CID-05 | 護照怎麼印 | 護照翻到資料頁，平放在玻璃面板上影印即可。 | Open to the photo page and place it flat on the glass. | Mở hộ chiếu đến trang thông tin, đặt phẳng lên mặt kính rồi sao chép. | Buka ke halaman foto dan letakkan rata di atas kaca. |
| CID-06 | 可以放大嗎 | 可以，放大縮小提供少數固定倍率，請依畫面選擇。 | Yes—enlarge/reduce offers a few fixed ratios; pick one on screen. | Được, phóng to/thu nhỏ có một số tỷ lệ cố định, hãy chọn trên màn hình. | Bisa—perbesar/perkecil menyediakan beberapa rasio tetap; pilih di layar. |
| CID-07 | 要黑白還是彩色 | 證件可選黑白或彩色，彩色費用較高。 | Choose black-and-white or color (color costs more). | Giấy tờ có thể chọn đen trắng hoặc màu, in màu phí cao hơn. | Pilih hitam-putih atau berwarna (berwarna lebih mahal). |
| CID-08 | 我要印好幾份 | 在畫面設定份數後再確認影印。 | Set the number of copies, then confirm. | Đặt số bản trên màn hình rồi xác nhận sao chép. | Atur jumlah salinan, lalu konfirmasi. |
| CID-09 | 影印證件多少錢 | 系統會依黑白彩色與份數計價，畫面會顯示金額。 | Price depends on color and copies; shown on screen. | Hệ thống tính giá theo đen trắng/màu và số bản, màn hình sẽ hiển thị số tiền. | Harga tergantung warna dan jumlah salinan; ditampilkan di layar. |
| CID-10 | 影印也要先付款嗎 | 是的，系統會先預覽報價，付款後才印出。 | Yes—preview and price first, then it prints after payment. | Đúng vậy, hệ thống xem trước báo giá, thanh toán xong mới in ra. | Ya—pratinjau dan harga dulu, lalu mencetak setelah pembayaran. |
| CID-11 | 印出來歪歪的 | 請把證件對齊玻璃面板角落的標示線，再重印一次。 | Align to the corner mark and copy again. | Hãy căn giấy tờ theo vạch chỉ dẫn ở góc mặt kính rồi in lại. | Sejajarkan dengan tanda di sudut lalu fotokopi lagi. |
| CID-12 | 我有好幾張證件 | 可以一張一張放上去分別影印，或用證件影印模式逐張處理。 | Copy them one at a time or use ID-copy mode for each. | Có thể đặt từng tờ để sao chép riêng, hoặc dùng chế độ sao chép giấy tờ xử lý từng tờ. | Fotokopi satu per satu atau gunakan mode fotokopi dokumen untuk masing-masing. |
| CID-13 | 印好的在哪拿 | 付款完成後請到機台出紙口拿取。 | Collect from the output tray after payment. | Thanh toán xong hãy lấy ở khe ra giấy của máy. | Ambil dari baki keluaran setelah pembayaran. |
| CID-14 | 證件影印要多久 | 通常幾秒就會出紙。 | Usually a few seconds. | Thường vài giây là ra giấy. | Biasanya beberapa detik. |
| CID-15 | 居留證可以印嗎 | 可以，居留證用證件影印方式操作即可。 | Yes—residence permits use ID-copy mode. | Được, thẻ cư trú dùng cách sao chép giấy tờ để thao tác. | Bisa—kartu izin tinggal menggunakan mode fotokopi dokumen. |
| CID-16 | 學生證 / 員工證 | 可以，一樣用證件影印模式操作。 | Yes—student/staff cards use ID-copy mode too. | Được, cũng dùng chế độ sao chép giấy tờ để thao tác. | Bisa—kartu pelajar/karyawan juga menggunakan mode fotokopi dokumen. |
| CID-17 | 證件要彩色才清楚 | 建議選彩色，畫面可切換，彩色費用較高。 | Color is clearer—switch on screen; color costs more. | Nên chọn màu, màn hình có thể chuyển đổi, in màu phí cao hơn. | Berwarna lebih jelas—ganti di layar; berwarna lebih mahal. |
| CID-18 | 兩張證件印一張紙 | 用證件影印模式可把正反或兩張併在同一張。 | ID-copy mode can fit both on one sheet. | Chế độ sao chép giấy tờ có thể ghép cả hai mặt hoặc hai tờ vào cùng một tờ. | Mode fotokopi dokumen bisa memuat keduanya pada satu lembar. |

---

## CPY — copy_doc｜一般文件影印（14）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| CPY-01 | 我要影印文件 | 請把文件放上玻璃面板或送稿器，依畫面選影印。 | Place your document on the glass or feeder and follow the screen. | Đặt tài liệu lên mặt kính hoặc bộ nạp tài liệu, chọn sao chép theo màn hình. | Letakkan dokumen di atas kaca atau pengumpan dokumen, lalu pilih fotokopi sesuai layar. |
| CPY-02 | 影印一疊文件 | 用上方送稿器一次放多張，依畫面開始影印。 | Use the top feeder for multiple pages and start. | Dùng bộ nạp tài liệu phía trên để đặt nhiều tờ một lúc, bắt đầu sao chép theo màn hình. | Gunakan pengumpan dokumen di atas untuk beberapa lembar sekaligus, lalu mulai fotokopi sesuai layar. |
| CPY-03 | 影印書本 | 不好意思，因著作財產權問題，本店不支援影印書本。 | Sorry—due to copyright, we don't support copying books. | Xin lỗi, vì vấn đề bản quyền, cửa hàng không hỗ trợ sao chép sách. | Maaf, karena masalah hak cipta, kami tidak mendukung fotokopi buku. |
| CPY-04 | 放大影印 | 放大提供少數固定倍率，請在畫面選擇。 | Enlarging offers a few fixed ratios—choose one on screen. | Phóng to chỉ có vài tỷ lệ cố định, vui lòng chọn trên màn hình. | Perbesar hanya tersedia beberapa rasio tetap, silakan pilih di layar. |
| CPY-05 | 縮小影印 | 縮小提供少數固定倍率，請在畫面選擇。 | Reducing offers a few fixed ratios—choose one on screen. | Thu nhỏ chỉ có vài tỷ lệ cố định, vui lòng chọn trên màn hình. | Perkecil hanya tersedia beberapa rasio tetap, silakan pilih di layar. |
| CPY-06 | A4 印成 A3 | 在畫面選放大到 A3 的固定倍率即可。 | Choose the fixed A4-to-A3 enlarge ratio on screen. | Chỉ cần chọn tỷ lệ cố định phóng to lên A3 trên màn hình. | Cukup pilih rasio tetap perbesar ke A3 di layar. |
| CPY-07 | 雙面影印 | 用送稿器並在畫面選雙面影印。 | Use the feeder and select double-sided. | Dùng bộ nạp tài liệu và chọn sao chép 2 mặt trên màn hình. | Gunakan pengumpan dokumen dan pilih fotokopi bolak-balik di layar. |
| CPY-08 | 影印彩色 | 在畫面選彩色，彩色費用較高。 | Choose color on screen; color costs more. | Chọn màu trên màn hình, in màu có phí cao hơn. | Pilih warna di layar, fotokopi warna lebih mahal. |
| CPY-09 | 影印多份 | 在畫面設定份數後確認。 | Set copies on screen, then confirm. | Đặt số bản trên màn hình rồi xác nhận. | Atur jumlah salinan di layar lalu konfirmasi. |
| CPY-10 | 影印多少錢 | 依黑白彩色、紙張與份數計價，畫面會顯示金額。 | Priced by color, paper, and copies; shown on screen. | Tính theo đen trắng/màu, giấy và số bản; màn hình sẽ hiển thị giá. | Dihitung berdasarkan hitam-putih/warna, kertas, dan jumlah salinan; harga tampil di layar. |
| CPY-11 | 印出來太黑 / 太淡 | 在畫面調整濃淡後重印。 | Adjust the darkness on screen and copy again. | Điều chỉnh độ đậm nhạt trên màn hình rồi in lại. | Sesuaikan kegelapan di layar lalu fotokopi lagi. |
| CPY-12 | 只印中間一部分 | 可調整擺放位置或選固定放大倍率，再影印。 | Reposition the page or choose a fixed enlarge ratio, then copy. | Có thể chỉnh vị trí đặt hoặc chọn tỷ lệ phóng to cố định rồi sao chép. | Bisa atur posisi peletakan atau pilih rasio perbesar tetap, lalu fotokopi. |
| CPY-13 | 原稿拿回去了嗎 | 影印後請記得從玻璃面板或送稿器取回原稿。 | Remember to take your original from the glass or feeder. | Sau khi sao chép, nhớ lấy lại bản gốc từ mặt kính hoặc bộ nạp tài liệu. | Setelah fotokopi, ingat ambil kembali dokumen asli dari kaca atau pengumpan dokumen. |
| CPY-14 | 影印要先付款嗎 | 是的，畫面會先報價，付款後印出。 | Yes—price shows first, then it prints after payment. | Đúng vậy, màn hình sẽ báo giá trước, thanh toán xong mới in ra. | Ya, layar menampilkan harga dulu, lalu dicetak setelah pembayaran. |

---

## SCN — scan｜掃描到 Email（不支援 USB）（18）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| SCN-01 | 我要掃描文件 | 請把文件放上玻璃面板或送稿器，在畫面選掃描方式。 | Place your document on the glass or feeder and choose a scan option. | Đặt tài liệu lên mặt kính hoặc khay nạp giấy, rồi chọn cách quét trên màn hình. | Letakkan dokumen di kaca atau pengumpan dokumen, lalu pilih opsi pindai di layar. |
| SCN-02 | 我要掃描到信箱 | 選「掃描到 Email」，輸入您的信箱，掃描後檔案會寄過去；Email 附檔最大 15MB。 | Choose Scan-to-Email and enter your address; email attachments are up to 15MB. | Chọn "quét sang Email", nhập email của bạn, sau khi quét tệp sẽ được gửi tới; tệp đính kèm Email tối đa 15MB. | Pilih "pindai ke Email", masukkan email Anda, setelah dipindai file akan dikirim; lampiran Email maksimal 15MB. |
| SCN-03 | 我要掃到 USB | 不好意思，本店掃描不支援 USB 隨身碟，只能選「掃描到 Email」寄送。 | Sorry—scan-to-USB isn't supported; we can only email the scan. | Xin lỗi, cửa hàng không hỗ trợ quét sang USB, chỉ có thể chọn "quét sang Email" để gửi. | Maaf, toko tidak mendukung pindai ke USB drive, hanya bisa pilih "pindai ke Email" untuk mengirim. |
| SCN-04 | USB 插哪裡 | 不好意思，本店不支援 USB 隨身碟，掃描請改用「掃描到 Email」。 | We don't support USB drives; please use Scan-to-Email instead. | Xin lỗi, cửa hàng không hỗ trợ USB drive, vui lòng quét bằng "quét sang Email". | Maaf, toko tidak mendukung USB drive, untuk memindai silakan gunakan "pindai ke Email". |
| SCN-05 | Email 沒收到 | 請確認信箱輸入正確並查看垃圾信件匣，必要時重新掃描寄送。 | Check the address and spam folder, then resend if needed. | Vui lòng kiểm tra email nhập đúng chưa và xem hộp thư rác, nếu cần thì quét gửi lại. | Periksa apakah alamat email benar dan cek folder spam, jika perlu pindai dan kirim ulang. |
| SCN-06 | 可以掃很多頁嗎 | 可以，用上方送稿器一次放多張，會合成一個檔案。 | Yes—use the feeder; pages combine into one file. | Được, dùng khay nạp giấy phía trên đặt nhiều tờ một lần, sẽ gộp thành một tệp. | Bisa, gunakan pengumpan dokumen di atas untuk banyak lembar sekaligus, akan digabung jadi satu file. |
| SCN-07 | 掃彩色還是黑白 | 可在畫面選彩色或黑白掃描。 | Choose color or black-and-white on screen. | Có thể chọn quét màu hoặc đen trắng trên màn hình. | Pilih pindai warna atau hitam-putih di layar. |
| SCN-08 | 掃成 PDF 還是圖片 | 可選 PDF 或 JPG，多頁文件建議選 PDF。 | Choose PDF or JPG; PDF for multi-page. | Có thể chọn PDF hoặc JPG, tài liệu nhiều trang nên chọn PDF. | Bisa pilih PDF atau JPG, untuk dokumen banyak halaman disarankan PDF. |
| SCN-09 | 原稿放哪 | 單張放玻璃面板，多張放上方送稿器。 | Single on the glass; multiple in the feeder. | Một tờ đặt lên mặt kính, nhiều tờ đặt vào khay nạp giấy phía trên. | Satu lembar di kaca, banyak lembar di pengumpan dokumen di atas. |
| SCN-10 | 掃描要錢嗎 | 掃描費用依機台設定，畫面會顯示是否收費與金額。 | Scan fees depend on the machine; shown on screen. | Phí quét tùy theo cài đặt của máy, màn hình sẽ hiển thị có thu phí và số tiền hay không. | Biaya pindai tergantung pengaturan mesin, layar akan menampilkan apakah berbayar dan jumlahnya. |
| SCN-11 | 可以調解析度嗎 | 可以，在畫面選解析度，越高檔案越大。 | Yes—choose resolution; higher means larger files. | Được, chọn độ phân giải trên màn hình, càng cao thì tệp càng lớn. | Bisa, pilih resolusi di layar, makin tinggi makin besar filenya. |
| SCN-12 | 可以雙面掃嗎 | 可以，用送稿器並在畫面選雙面掃描。 | Yes—use the feeder and select double-sided. | Được, dùng khay nạp giấy và chọn quét hai mặt trên màn hình. | Bisa, gunakan pengumpan dokumen dan pilih pindai dua sisi di layar. |
| SCN-13 | 檔案太大寄不出去 | Email 附檔上限 15MB，請降低解析度或分次掃描讓檔案變小。 | Email attachments are capped at 15MB—lower the resolution or split the scan. | Tệp đính kèm Email tối đa 15MB, vui lòng giảm độ phân giải hoặc quét chia nhiều lần để tệp nhỏ lại. | Lampiran Email maksimal 15MB, turunkan resolusi atau pindai secara terpisah agar filenya lebih kecil. |
| SCN-14 | 掃描的檔案會留著嗎 | 掃描檔只暫存於店內主機，完成寄送或存檔後即清除，不上雲。 | Scans are processed in-store and cleared after sending. | Tệp quét chỉ lưu tạm trên máy chủ trong cửa hàng, sau khi gửi hoặc lưu xong sẽ xóa, không lên đám mây. | File pindai hanya disimpan sementara di server toko, dihapus setelah dikirim atau disimpan, tidak naik ke cloud. |
| SCN-15 | 掃描到手機可以嗎 | 可選掃描到 Email，再用手機收信即可。 | Use Scan-to-Email and open it on your phone. | Có thể chọn quét sang Email, rồi dùng điện thoại nhận thư là được. | Bisa pilih pindai ke Email, lalu buka emailnya di ponsel. |
| SCN-16 | 掃描存成一個檔 | 多頁用送稿器會合成一個 PDF。 | Multiple pages in the feeder combine into one PDF. | Nhiều trang dùng khay nạp giấy sẽ gộp thành một PDF. | Banyak halaman dengan pengumpan dokumen akan digabung jadi satu PDF. |
| SCN-17 | 掃描書本 | 不好意思，因著作財產權問題，本店不支援掃描書本。 | Sorry—due to copyright, we don't support scanning books. | Xin lỗi, vì vấn đề bản quyền, cửa hàng không hỗ trợ quét sách. | Maaf, karena masalah hak cipta, toko tidak mendukung pindai buku. |
| SCN-18 | 掃完可以改檔名嗎 | 可在寄送前依畫面設定檔名或主旨。 | Set the file name or subject before sending. | Có thể đặt tên tệp hoặc tiêu đề theo màn hình trước khi gửi. | Bisa atur nama file atau subjek di layar sebelum mengirim. |

---

## FN — advanced_func｜進階功能（16）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| FN-01 | 可以裝訂嗎 / 釘起來 | 不好意思，本店不提供裝訂、騎馬釘與打孔功能。 | Sorry—we don't offer binding, saddle-stitch, or hole-punching. | Xin lỗi, cửa hàng không cung cấp đóng tập, ghim giữa và đục lỗ. | Maaf, kami tidak menyediakan penjilidan, jahit kawat tengah, dan pelubangan. |
| FN-02 | 騎馬釘 / 做成冊子 | 不好意思，本店不提供騎馬釘與裝訂功能。 | Sorry—saddle-stitch and binding aren't available. | Xin lỗi, cửa hàng không cung cấp ghim giữa và đóng tập. | Maaf, jahit kawat tengah dan penjilidan tidak tersedia. |
| FN-03 | 打洞 | 不好意思，本店不提供打孔功能。 | Sorry—hole-punching isn't available. | Xin lỗi, cửa hàng không cung cấp đục lỗ. | Maaf, pelubangan tidak tersedia. |
| FN-04 | 印海報 / 大張 | 不好意思，本店不提供海報列印，最大列印尺寸為 A3。 | Sorry—poster printing isn't available; the largest size is A3. | Xin lỗi, cửa hàng không in áp phích, khổ in lớn nhất là A3. | Maaf, cetak poster tidak tersedia; ukuran terbesar adalah A3. |
| FN-05 | 印名片 | 可上傳名片檔列印，建議用 PDF 並設定尺寸。 | Upload a card file as PDF and set the size. | Có thể tải tệp danh thiếp lên để in, nên dùng PDF và đặt kích thước. | Unggah file kartu sebagai PDF dan atur ukurannya. |
| FN-06 | 護貝 | 不好意思，本店目前不提供護貝服務。 | Sorry—we don't offer lamination. | Xin lỗi, cửa hàng hiện không có dịch vụ ép plastic. | Maaf, toko ini saat ini tidak menyediakan laminasi. |
| FN-07 | 裁切 | 不好意思，本店目前不提供裁切服務。 | Sorry—we don't offer cutting. | Xin lỗi, hiện cửa hàng không có dịch vụ cắt giấy. | Maaf, saat ini kami tidak menyediakan layanan pemotongan. |
| FN-08 | 合併多個 PDF | 上傳頁面可加入多個檔案一起列印。 | Add multiple files on the upload page to print together. | Trên trang tải lên có thể thêm nhiều tệp để in cùng nhau. | Tambahkan beberapa file di halaman unggah untuk dicetak bersama. |
| FN-09 | 加浮水印 | 系統不提供浮水印，建議在原檔處理好再上傳。 | No watermark feature—add it to your file first. | Hệ thống không có chức năng đóng dấu mờ, bạn nên xử lý sẵn trong tệp gốc rồi tải lên. | Sistem tidak menyediakan tanda air, sebaiknya siapkan dulu di file asli sebelum mengunggah. |
| FN-10 | 印黑白省錢 | 在設定選黑白即可，費用較彩色低。 | Choose black-and-white to save; it's cheaper than color. | Chọn đen trắng trong cài đặt, chi phí thấp hơn in màu. | Pilih hitam-putih untuk hemat; lebih murah dari warna. |
| FN-11 | 一頁印多頁 / 多合一 | 可在畫面選擇多合一（一頁印多頁），依設定會更新預覽。 | Choose N-up (multiple pages per sheet) on screen; the preview updates. | Có thể chọn nhiều trang một tờ trên màn hình, bản xem trước sẽ cập nhật theo cài đặt. | Pilih N-up (beberapa halaman per lembar) di layar; pratinjau diperbarui. |
| FN-12 | 自動雙面 | 在設定選雙面列印即可。 | Choose double-sided in settings. | Chỉ cần chọn in 2 mặt trong cài đặt. | Pilih bolak-balik di pengaturan. |
| FN-13 | 印信封 | 不好意思，本店不支援信封列印功能。 | Sorry—envelope printing isn't supported. | Xin lỗi, cửa hàng không hỗ trợ in phong bì. | Maaf, cetak amplop tidak didukung. |
| FN-14 | 印貼紙 / 標籤紙 | 不好意思，本店目前不提供特殊紙材。 | Sorry—we don't offer special media. | Xin lỗi, cửa hàng hiện không cung cấp loại giấy đặc biệt. | Maaf, toko ini saat ini tidak menyediakan kertas khusus. |
| FN-15 | 縮放到指定比例 | 放大縮小提供少數固定倍率，請在畫面選擇。 | Enlarge/reduce offers a few fixed ratios—choose one on screen. | Phóng to/thu nhỏ chỉ có vài tỷ lệ cố định, vui lòng chọn trên màn hình. | Perbesar/perkecil hanya menawarkan beberapa rasio tetap—pilih di layar. |
| FN-16 | 邊界 / 滿版列印 | 在設定選滿版或保留邊界。 | Choose full-bleed or margins in settings. | Chọn in tràn lề hoặc giữ lề trong cài đặt. | Pilih full-bleed atau margin di pengaturan. |

---

## SUP — supplies｜紙張 / 耗材 / 品質（14）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| SUP-01 | 有 A3 嗎 | 有，列印或影印時在畫面選 A3。 | Yes—choose A3 when printing or copying. | Có—chọn A3 khi in hoặc photocopy. | Ada—pilih A3 saat mencetak atau memfotokopi. |
| SUP-02 | 有相片紙嗎 | 不好意思，本店目前不提供相片紙。 | Sorry—we don't offer photo paper. | Xin lỗi, hiện cửa hàng không có giấy ảnh. | Maaf, saat ini kami tidak menyediakan kertas foto. |
| SUP-03 | 紙張厚度 / 磅數 | 本店提供 A4、A3 的 80 磅優良影印紙；目前不提供其他規格紙材。 | We provide quality 80gsm paper in A4 and A3; no other paper types at this time. | Cửa hàng cung cấp giấy photocopy chất lượng 80gsm khổ A4, A3; hiện không có loại giấy khác. | Kami menyediakan kertas berkualitas 80gsm dalam A4 dan A3; saat ini tidak ada jenis kertas lain. |
| SUP-04 | 有彩色嗎 | 有，列印影印都可選彩色，費用較高。 | Yes—color is available; it costs more. | Có—in và photocopy đều chọn được màu, phí cao hơn. | Ada—warna tersedia; biayanya lebih mahal. |
| SUP-05 | 紙質不好 | 若對紙質有疑問，可改用旁邊另一台機器試印。 | If unsatisfied, try one of the other machines. | Nếu bạn thắc mắc về chất lượng giấy, có thể chuyển sang máy bên cạnh để in thử. | Jika ragu soal kualitas kertas, Anda bisa coba cetak di mesin sebelah. |
| SUP-06 | 可以用我自己的紙嗎 | 不好意思，機台使用內建紙張，無法放自備紙張。 | Sorry—machines use built-in paper; you can't load your own. | Xin lỗi—máy dùng giấy có sẵn, không thể nạp giấy tự mang. | Maaf—mesin memakai kertas bawaan; Anda tidak bisa memasang kertas sendiri. |
| SUP-07 | 顏色很淡 / 沒碳粉 | 若列印偏淡，建議改用旁邊另一台機器。 | If prints are faded, use one of the other machines. | Nếu bản in bị nhạt, bạn nên chuyển sang máy bên cạnh nhé. | Kalau hasil cetak terlihat pudar, sebaiknya gunakan mesin di sebelahnya. |
| SUP-08 | 紙用完會自動補嗎 | 缺紙時可依螢幕指示補紙，或改用旁邊另一台機器。 | Refill per on-screen steps, or use another machine. | Khi hết giấy, quý khách có thể làm theo hướng dẫn trên màn hình để thêm giấy, hoặc dùng máy bên cạnh. | Saat kertas habis, ikuti petunjuk di layar untuk mengisi kertas, atau gunakan mesin di sebelahnya. |
| SUP-09 | 怎麼印品質比較好 | 用 PDF 上傳並選彩色，品質較穩定。 | Upload PDF and choose color for stable quality. | Tải lên PDF và chọn màu để chất lượng ổn định hơn. | Unggah PDF dan pilih warna agar kualitas stabil. |
| SUP-10 | 紙卡卡的 / 皺 | 紙張異常請改用旁邊另一台機器。 | If paper is faulty, use one of the other machines. | Nếu giấy bị lỗi, bạn vui lòng chuyển sang máy bên cạnh nhé. | Jika kertas bermasalah, silakan beralih ke mesin sebelah. |
| SUP-11 | 雙面會不會透 | 一般影印紙雙面略有透色屬正常。 | Slight show-through on standard paper is normal. | Giấy photocopy thường hơi thấu màu hai mặt là bình thường. | Sedikit tembus pandang pada kertas standar adalah normal. |
| SUP-12 | 最大印到多大 | 一般最大為 A3。 | The maximum is usually A3. | Lớn nhất thường là A3. | Maksimum biasanya A3. |
| SUP-13 | 最小印到多小 | 縮小提供少數固定倍率，請依畫面選擇。 | Reducing offers a few fixed ratios—choose one on screen. | Thu nhỏ có vài tỷ lệ cố định, hãy chọn trên màn hình. | Perkecil tersedia beberapa rasio tetap—pilih di layar. |
| SUP-14 | 有哪些紙張尺寸 | 常見為 A4 與 A3，畫面可選。 | A4 and A3 are available on screen. | Thường có A4 và A3, chọn trên màn hình. | A4 dan A3 tersedia di layar. |

---

## PAY — payment｜付款操作（22）

> 過渡期：付款後沒出紙 → 導「改用另一台重印、不扣款」，**不承諾現場退款**；退款入口（D-A）上線後再開放。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| PAY-01 | 怎麼付款 | 確認預覽後點付款，依畫面用電子支付或掃碼完成。 | After the preview, tap pay and complete via mobile payment. | Sau khi xem trước, nhấn thanh toán và hoàn tất bằng thanh toán điện tử hoặc quét mã. | Setelah pratinjau, ketuk bayar dan selesaikan dengan pembayaran elektronik atau scan to pay. |
| PAY-02 | 可以用什麼付款 | 本店為多元電子支付，支援 LINE Pay、信用卡等掃碼/電子支付；不收現金與實體悠遊卡。 | We accept multiple e-payments—LINE Pay, credit card and other scan/e-payments; no cash or physical EasyCard. | Cửa hàng dùng nhiều loại thanh toán điện tử, hỗ trợ LINE Pay, thẻ tín dụng và quét mã; không nhận tiền mặt và thẻ EasyCard vật lý. | Kami menerima beragam pembayaran elektronik—LINE Pay, kartu kredit dan scan to pay; tidak menerima tunai maupun EasyCard fisik. |
| PAY-03 | 可以用 LINE Pay 嗎 | 可以，本店多元支付支援 LINE Pay，依畫面掃碼付款即可。 | Yes—LINE Pay is supported; just scan to pay on screen. | Được, cửa hàng hỗ trợ LINE Pay, chỉ cần quét mã trên màn hình để thanh toán. | Bisa—LINE Pay didukung; cukup scan to pay di layar. |
| PAY-04 | 可以刷悠遊卡嗎 | 不好意思，本店不支援實體悠遊卡，可改用 LINE Pay 或信用卡。 | Sorry—physical EasyCard isn't accepted; use LINE Pay or credit card instead. | Xin lỗi, cửa hàng không hỗ trợ thẻ EasyCard vật lý, vui lòng dùng LINE Pay hoặc thẻ tín dụng. | Maaf—EasyCard fisik tidak diterima; gunakan LINE Pay atau kartu kredit. |
| PAY-05 | 可以刷卡嗎 | 可以，本店多元支付支援信用卡，依畫面操作即可。 | Yes—credit card is supported; just follow the on-screen steps. | Được, cửa hàng hỗ trợ thẻ tín dụng, chỉ cần làm theo màn hình. | Bisa—kartu kredit didukung; cukup ikuti langkah di layar. |
| PAY-06 | 可以投現金嗎 | 不好意思，本店不收現金，僅支援電子支付（如 LINE Pay、信用卡）。 | Sorry—no cash; we accept e-payments only (e.g., LINE Pay, credit card). | Xin lỗi, cửa hàng không nhận tiền mặt, chỉ hỗ trợ thanh toán điện tử (như LINE Pay, thẻ tín dụng). | Maaf—tidak menerima tunai; hanya pembayaran elektronik (mis. LINE Pay, kartu kredit). |
| PAY-07 | 付款了卻沒出紙 | 請先確認出紙匣並稍等約 30 秒；若仍沒出紙，請直接改用旁邊另一台機器重印，未完成的列印不會扣款。 | Check the tray and wait ~30s; if nothing prints, reprint on another machine—unfinished jobs aren't charged. | Vui lòng kiểm tra khay giấy và đợi khoảng 30 giây; nếu vẫn chưa ra giấy, hãy chuyển sang máy bên cạnh để in lại, bản in chưa hoàn thành sẽ không bị trừ tiền. | Mohon periksa baki kertas dan tunggu sekitar 30 detik; jika tetap tidak keluar, langsung gunakan mesin di sebelahnya untuk cetak ulang, cetakan yang belum selesai tidak akan ditagih. |
| PAY-08 | 我好像被扣兩次 | 不好意思造成困擾；目前現場無法直接處理重複扣款，請先保留交易紀錄，線上退款申請功能即將開放。 | Sorry—double charges can't be handled on-site yet; keep your record, online refunds are coming soon. | Xin lỗi đã gây phiền; hiện tại không thể xử lý trừ tiền trùng tại chỗ, vui lòng giữ lại lịch sử giao dịch, chức năng yêu cầu hoàn tiền trực tuyến sắp ra mắt. | Maaf—penagihan ganda belum bisa ditangani di tempat; simpan catatan transaksi Anda, pengajuan refund online segera hadir. |
| PAY-09 | 付款失敗 | 請稍候再試一次，或換一種付款方式；也可以改用旁邊另一台機器。 | Try again or another method; you can also use another machine. | Xin chờ rồi thử lại, hoặc đổi cách thanh toán khác; quý khách cũng có thể dùng máy bên cạnh. | Mohon tunggu lalu coba lagi, atau ganti metode pembayaran lain; Anda juga bisa gunakan mesin di sebelahnya. |
| PAY-10 | 付款的 QR 在哪 | 確認預覽後，付款 QR 會顯示在手機或機台畫面上。 | After the preview, the payment QR appears on your phone or screen. | Sau khi xem trước, mã QR thanh toán sẽ hiện trên điện thoại hoặc màn hình máy. | Setelah pratinjau, QR pembayaran muncul di ponsel atau layar Anda. |
| PAY-11 | 有收據或發票嗎 | 本店所有消費都開立電子發票；付款明細也會顯示在畫面與手機操作頁面。 | Every purchase gets an e-invoice; payment details also show on screen and your phone. | Mọi giao dịch tại cửa hàng đều xuất hóa đơn điện tử; chi tiết thanh toán cũng hiện trên màn hình và trang thao tác điện thoại. | Setiap pembelian mendapat faktur elektronik; detail pembayaran juga tampil di layar dan ponsel Anda. |
| PAY-12 | 金額好像不對 | 金額依頁數、彩色與紙張自動計算，付款前畫面會先顯示；有疑問請保留交易紀錄。 | The amount is auto-calculated and shown before payment; keep your record if in doubt. | Số tiền tự động tính theo số trang, màu sắc và loại giấy, sẽ hiện trên màn hình trước khi thanh toán; nếu thắc mắc vui lòng giữ lại lịch sử giao dịch. | Jumlah dihitung otomatis dan ditampilkan sebelum pembayaran; simpan catatan Anda jika ragu. |
| PAY-13 | 付到一半中斷了 | 未完成付款不會列印也不會扣款，請重新操作一次。 | An incomplete payment won't print or charge; start again. | Thanh toán chưa hoàn tất sẽ không in và không bị trừ tiền, vui lòng thao tác lại. | Pembayaran yang tidak selesai tidak akan mencetak atau menagih; mulai lagi. |
| PAY-14 | 我要退款 | 不好意思，若付款後沒印出來，您可以改用旁邊另一台機器重印，未完成不扣款；線上退款申請即將開放。 | Sorry—if a paid job didn't print, reprint on another machine (no charge); online refunds coming soon. | Xin lỗi, nếu đã thanh toán mà chưa in ra, bạn có thể chuyển sang máy bên cạnh để in lại, chưa hoàn thành thì không bị trừ tiền; đăng ký hoàn tiền trực tuyến sắp mở. | Maaf, jika sudah bayar tetapi belum tercetak, Anda bisa cetak ulang di mesin sebelah, yang belum selesai tidak dikenai biaya; pengajuan refund online segera dibuka. |
| PAY-15 | 有找零或低消嗎 | 本店僅電子支付、無找零；低消為 2 元，付款前畫面會顯示金額。 | E-payment only, no change; the minimum charge is NT$2 and the amount shows before payment. | Cửa hàng chỉ thanh toán điện tử, không thối tiền; mức tiêu tối thiểu là 2 NT$, số tiền sẽ hiện trên màn hình trước khi thanh toán. | Hanya pembayaran elektronik, tanpa kembalian; minimum charge NT$2 dan jumlah tampil sebelum pembayaran. |
| PAY-16 | 付款後多久會印 | 付款成功後通常幾秒內就會開始出紙。 | Printing starts within seconds after payment. | Sau khi thanh toán thành công, thường vài giây sau là bắt đầu ra giấy. | Pencetakan dimulai dalam hitungan detik setelah pembayaran. |
| PAY-17 | 可以開統編嗎 | 不好意思，電子發票目前不支援輸入統一編號。 | Sorry—the e-invoice doesn't support a business tax number. | Xin lỗi—hóa đơn điện tử hiện không hỗ trợ nhập business tax number. | Maaf—faktur elektronik tidak mendukung business tax number. |
| PAY-18 | 有最低消費嗎 | 有，低消為 2 元，付款前畫面會顯示金額。 | Yes—the minimum charge is NT$2; the amount shows before payment. | Có, mức tiêu tối thiểu là 2 NT$, số tiền sẽ hiện trên màn hình trước khi thanh toán. | Ya—minimum charge NT$2; jumlah tampil sebelum pembayaran. |
| PAY-19 | 可以分開付嗎 | 不好意思，無法分開付款，每筆訂單就是一次付款，請依畫面金額付清。 | Sorry—payments can't be split; each order is a single payment for the amount shown. | Xin lỗi, không thể tách thanh toán, mỗi đơn hàng là một lần thanh toán, vui lòng trả đủ theo số tiền trên màn hình. | Maaf—pembayaran tidak bisa dipisah; tiap pesanan satu kali pembayaran sesuai jumlah yang tampil. |
| PAY-20 | 付款畫面卡住 | 請稍候重整或重新操作；也可改用旁邊另一台機器。 | Wait and retry, or use one of the other machines. | Vui lòng đợi rồi làm mới hoặc thao tác lại; bạn cũng có thể chuyển sang máy bên cạnh. | Mohon tunggu lalu segarkan atau ulangi; Anda juga bisa beralih ke mesin di sebelahnya. |
| PAY-21 | 我掃不到付款碼 | 請對準畫面付款 QR，或換個角度；仍不行可改用另一台。 | Align with the payment QR or change angle; or use another machine. | Vui lòng canh đúng mã QR thanh toán trên màn hình, hoặc đổi góc; nếu vẫn không được có thể chuyển sang máy khác. | Sejajarkan dengan QR pembayaran atau ubah sudut; atau <mark>pakai mesin lain</mark>. |
| PAY-22 | 付完可以改份數嗎 | 付款後無法更改，如需調整請重新操作。 | Can't change after payment; start over to adjust. | Sau khi thanh toán không thể thay đổi, nếu cần điều chỉnh vui lòng thao tác lại. | Tidak bisa diubah setelah pembayaran; mulai ulang untuk menyesuaikan. |

---

## PRO — promo｜優惠券 / 優惠碼（7）

> 門市有優惠/折扣，以「優惠碼」(一串代碼)形式；在**手機操作頁面輸入優惠碼**折抵，**機台無掃描功能**。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| PRO-01 | 有優惠券嗎 / 有折扣嗎 | 有的，若您有優惠碼，可在手機操作頁面輸入折抵。 | Yes—if you have a promo code, enter it on the phone page to get the discount. | Có. Nếu bạn có mã khuyến mãi, hãy nhập trên trang điện thoại để được giảm giá. | Ada. Jika punya kode promo, masukkan di halaman ponsel untuk mendapat diskon. |
| PRO-02 | 優惠碼怎麼用 | 在手機付款前的頁面找到優惠碼欄位，輸入那串代碼就會套用折扣。 | On the phone page before payment, enter your promo code to apply the discount. | Trên trang điện thoại trước khi thanh toán, nhập mã khuyến mãi để áp dụng giảm giá. | Di halaman ponsel sebelum pembayaran, masukkan kode promo untuk menerapkan diskon. |
| PRO-03 | 優惠券要在機台掃描嗎 | 不好意思，機台沒有掃描功能，優惠請改在手機頁面輸入優惠碼。 | Sorry—the machine can't scan; enter your promo code on the phone page instead. | Xin lỗi, máy không quét được; hãy nhập mã khuyến mãi trên trang điện thoại. | Maaf, mesin tidak bisa memindai; masukkan kode promo di halaman ponsel saja. |
| PRO-04 | 優惠碼在哪裡輸入 | 在手機操作頁面、付款前會有優惠碼欄位，輸入後金額會更新。 | There's a promo-code field on the phone page before payment; the amount updates after you enter it. | Có ô mã khuyến mãi trên trang điện thoại trước khi thanh toán; số tiền sẽ cập nhật sau khi nhập. | Ada kolom kode promo di halaman ponsel sebelum pembayaran; jumlahnya diperbarui setelah dimasukkan. |
| PRO-05 | 優惠碼無效 / 用不了 | 請確認優惠碼輸入正確且仍在有效期內；若仍無法使用，可能已過期或不符使用條件。 | Check the code is correct and still valid; if it still won't work, it may be expired or not eligible. | Hãy kiểm tra mã nhập đúng và còn trong thời hạn; nếu vẫn không dùng được, có thể đã hết hạn hoặc không đủ điều kiện. | Periksa kode sudah benar dan masih berlaku; jika tetap tidak bisa, mungkin sudah kedaluwarsa atau tidak memenuhi syarat. |
| PRO-06 | 折扣有套用到嗎 | 輸入優惠碼後，付款前畫面會顯示折扣後金額，確認後再付款。 | After entering the code, the discounted total shows before payment—check it, then pay. | Sau khi nhập mã, màn hình trước khi thanh toán sẽ hiển thị số tiền sau giảm giá; kiểm tra rồi thanh toán. | Setelah memasukkan kode, total setelah diskon muncul sebelum pembayaran; periksa lalu bayar. |
| PRO-07 | 優惠券哪裡拿 / 怎麼領 | 優惠活動與優惠碼的取得方式，請參考現場告示或我們的活動公告。 | For promotions and how to get codes, see the in-store notices or our announcements. | Về các chương trình khuyến mãi và cách nhận mã, xin xem thông báo tại cửa hàng hoặc thông báo hoạt động của chúng tôi. | Untuk promosi dan cara mendapatkan kode, lihat pengumuman di toko atau pengumuman acara kami. |

---

## INV — invoice｜發票 / 收據（10）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| INV-01 | 有發票嗎 | 有，本店所有消費都開立電子發票。 | Yes—every purchase gets an e-invoice. | Có—mọi giao dịch đều xuất hóa đơn điện tử. | Ya—setiap pembelian mendapat faktur elektronik. |
| INV-02 | 我要紙本發票 | 不好意思，本店只開電子發票，不提供紙本發票。 | Sorry—we issue e-invoices only, no paper invoices. | Xin lỗi—chúng tôi chỉ xuất hóa đơn điện tử, không có hóa đơn giấy. | Maaf—kami hanya menerbitkan faktur elektronik, tidak ada faktur kertas. |
| INV-03 | 載具怎麼設 | 本店所有消費都開電子發票；載具與發票設定是在付款時由電子支付系統處理。 | Every purchase gets an e-invoice; carrier and invoice settings are handled by the payment system at checkout. | Mọi giao dịch đều xuất hóa đơn điện tử; invoice carrier và cài đặt hóa đơn do hệ thống thanh toán xử lý khi thanh toán. | Setiap pembelian mendapat faktur elektronik; invoice carrier dan pengaturan faktur ditangani sistem pembayaran saat checkout. |
| INV-04 | 統一編號 | 不好意思，電子發票目前不支援輸入統一編號。 | Sorry—the e-invoice doesn't support a business tax number. | Xin lỗi—hóa đơn điện tử hiện không hỗ trợ nhập business tax number. | Maaf—faktur elektronik tidak mendukung business tax number. |
| INV-05 | 發票中獎怎麼領 | 電子發票的對獎與中獎通知，依電子發票平台規定辦理。 | E-invoice prize draws follow the e-invoice platform's rules. | Việc dò và thông báo invoice prize theo quy định của nền tảng hóa đơn điện tử. | Pengundian invoice prize mengikuti aturan platform faktur elektronik. |
| INV-06 | 收據在哪 | 本店開立電子發票；付款明細也會顯示在畫面與手機操作頁面。 | We issue e-invoices; payment details also show on screen and your phone. | Chúng tôi xuất hóa đơn điện tử; chi tiết thanh toán cũng hiện trên màn hình và trang thao tác điện thoại. | Kami menerbitkan faktur elektronik; rincian pembayaran juga tampil di layar dan ponsel. |
| INV-07 | 發票寄到哪 | 電子發票會依付款時電子支付系統的設定開立與通知。 | The e-invoice is issued and notified per the payment system's settings. | Hóa đơn điện tử được xuất và thông báo theo cài đặt của hệ thống thanh toán khi thanh toán. | Faktur elektronik diterbitkan dan diberitahukan sesuai pengaturan sistem pembayaran. |
| INV-08 | 可以捐發票嗎 | 不好意思，目前沒有手機條碼自動捐贈公益的功能。 | Sorry—there's no mobile-barcode auto-donation to charity. | Xin lỗi—hiện không có chức năng tự động quyên góp từ thiện bằng mã vạch điện thoại. | Maaf—tidak ada donasi otomatis ke amal lewat barcode ponsel. |
| INV-09 | 重印發票 | 電子發票可於電子發票平台查詢；付款明細也會顯示在畫面。 | E-invoices can be checked on the e-invoice platform; payment details also show on screen. | Hóa đơn điện tử có thể tra trên nền tảng hóa đơn điện tử; chi tiết thanh toán cũng hiện trên màn hình. | Faktur elektronik bisa dicek di platform faktur elektronik; rincian pembayaran juga tampil di layar. |
| INV-10 | 發票金額不對 | 金額依實際列印計算，付款前畫面會顯示；電子發票依該金額開立。 | The amount reflects actual printing and shows before payment; the e-invoice is issued for that amount. | Số tiền tính theo bản in thực tế và hiện trước khi thanh toán; hóa đơn điện tử xuất theo số tiền đó. | Jumlah dihitung sesuai cetakan sebenarnya dan tampil sebelum pembayaran; faktur elektronik diterbitkan untuk jumlah itu. |

---

## ERR — machine_error｜機台狀況（20）

> 自助優先：①依機台螢幕圖示自行排除/加紙 ②**改用店內另外兩台機器**（未完成不扣款）。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| ERR-01 | 卡紙了 | 請依機台螢幕圖示打開紙匣、取出卡住的紙張即可；不想自行處理，旁邊還有另外兩台可直接用，未完成不扣款。 | Follow the on-screen diagram to clear the jam, or use the other two machines—unfinished jobs aren't charged. | Quý khách hãy theo hình trên màn hình để mở khay giấy và lấy tờ bị kẹt ra; nếu không muốn tự xử lý, bên cạnh còn hai máy nữa dùng được ngay, chưa xong thì không trừ tiền. | Ikuti gambar di layar untuk membuka baki kertas dan ambil kertas yang macet; jika tidak mau menangani sendiri, ada dua mesin lain di sebelahnya yang langsung bisa dipakai, pekerjaan yang belum selesai tidak ditagih. |
| ERR-02 | 沒紙了 | 請依機台螢幕指示打開紙匣補充紙張；或直接改用旁邊另一台，未完成不扣款。 | Refill paper per the screen, or use another machine—no charge for unfinished jobs. | Vui lòng làm theo hướng dẫn trên màn hình để mở khay và thêm giấy; hoặc chuyển thẳng sang máy bên cạnh, chưa hoàn thành thì không bị trừ tiền. | Silakan ikuti petunjuk di layar untuk membuka baki dan menambah kertas; atau langsung pakai mesin sebelah, yang belum selesai tidak dikenai biaya. |
| ERR-03 | 印出來是空白的 | 通常是檔案或設定問題，請檢查原始檔案後重印，或改用旁邊另一台試試。 | Usually a file/setting issue—check and reprint, or try another machine. | Thường là do tệp hoặc cài đặt, vui lòng kiểm tra tệp gốc rồi in lại, hoặc thử máy bên cạnh. | Biasanya masalah berkas atau pengaturan, mohon periksa berkas asli lalu cetak ulang, atau coba mesin di sebelahnya. |
| ERR-04 | 印出來有條紋很髒 | 列印品質不佳時，建議直接改用旁邊另一台機器。 | For poor quality, use one of the other machines. | Khi chất lượng in kém, quý khách nên đổi sang dùng máy bên cạnh. | Jika kualitas cetak kurang baik, sebaiknya gunakan mesin di sebelahnya. |
| ERR-05 | 機器沒反應 / 當機 | 請直接改用旁邊另一台機器操作，未完成的訂單不會扣款。 | Use one of the other machines—unfinished jobs aren't charged. | Bạn vui lòng chuyển thẳng sang máy bên cạnh để thao tác, đơn chưa hoàn thành sẽ không bị trừ tiền. | Silakan langsung gunakan mesin sebelah, pesanan yang belum selesai tidak akan dikenai biaya. |
| ERR-06 | 螢幕黑掉了 | 這台螢幕沒反應時，請改用旁邊另一台機器。 | If the screen is dead, use one of the other machines. | Khi máy này màn hình không phản hồi, vui lòng chuyển sang máy bên cạnh. | Kalau layar mesin ini tidak merespons, mohon gunakan mesin di sebelahnya. |
| ERR-07 | 印到一半停住 | 請稍候幾秒；若沒有恢復，可改用旁邊另一台重印。 | Wait a few seconds; if it doesn't resume, reprint on another machine. | Quý khách chờ vài giây; nếu không tiếp tục, có thể in lại trên máy bên cạnh. | Mohon tunggu beberapa detik; jika tidak lanjut, Anda bisa cetak ulang di mesin di sebelahnya. |
| ERR-08 | 顏色很淡 / 沒碳粉 | 列印偏淡時，建議改用旁邊另一台機器。 | If faded, use one of the other machines. | Khi in bị nhạt màu, bạn nên chuyển sang máy bên cạnh nhé. | Jika hasil cetak pudar, sebaiknya beralih ke mesin sebelah. |
| ERR-09 | 我可以自己拉紙嗎 | 可以，請依螢幕圖示慢慢取出卡紙，不要硬拉；不確定就改用旁邊另一台。 | Yes—follow the diagram and gently remove it; if unsure, use another machine. | Được, vui lòng làm theo hình trên màn hình để lấy giấy kẹt ra từ từ, đừng kéo mạnh; nếu không chắc thì dùng máy bên cạnh nhé. | Bisa, mohon ikuti gambar di layar untuk mengeluarkan kertas macet perlahan, jangan ditarik paksa; kalau ragu pakai mesin di sebelahnya. |
| ERR-10 | 紙要怎麼補 | 請依機台螢幕指示打開紙匣，放入紙張即可。 | Follow the on-screen steps to open the tray and add paper. | Hãy làm theo hướng dẫn trên màn hình để mở khay và cho giấy vào. | Ikuti petunjuk di layar untuk membuka baki dan memasukkan kertas. |
| ERR-11 | 我印錯了 | 已印出的內容無法收回；如需重印請重新操作，或改用旁邊另一台。 | Printed pages can't be undone; reprint here or on another machine. | Nội dung đã in ra không thể thu lại; nếu cần in lại xin thao tác lại, hoặc đổi sang máy bên cạnh. | Halaman yang sudah tercetak tidak bisa ditarik kembali; jika perlu cetak ulang silakan ulangi, atau gunakan mesin di sebelahnya. |
| ERR-12 | 機器有怪聲音 | 機台有異常聲響時，請停止使用這台，改用旁邊另一台。 | If it makes odd noises, stop and switch to another machine. | Khi máy có tiếng động lạ, bạn vui lòng ngừng dùng máy này và chuyển sang máy bên cạnh. | Jika mesin mengeluarkan suara aneh, hentikan pemakaian mesin ini dan beralih ke mesin sebelah. |
| ERR-13 | 蓋子 / 送稿器卡住 | 請依螢幕指示輕輕復位，不要強行扳動；不確定就改用旁邊另一台。 | Follow the screen to gently reset it; if unsure, use another machine. | Vui lòng làm theo hướng dẫn trên màn hình để nhẹ nhàng đặt lại, đừng cố cạy; nếu không chắc thì dùng máy bên cạnh. | Mohon ikuti petunjuk di layar untuk memasang kembali dengan lembut, jangan dipaksa; kalau ragu pakai mesin di sebelahnya. |
| ERR-14 | 機器壞掉了 | 這台無法使用時，請直接改用旁邊另一台，未完成不扣款。 | If it's broken, use one of the other machines—no charge for unfinished jobs. | Khi máy này không dùng được, quý khách hãy đổi sang máy bên cạnh, chưa xong thì không trừ tiền. | Jika mesin ini tidak bisa dipakai, silakan gunakan mesin di sebelahnya, pekerjaan yang belum selesai tidak ditagih. |
| ERR-15 | 出紙口卡住 | 請依螢幕指示輕輕取出，不要硬拉；不確定改用旁邊另一台。 | Gently remove it per the screen; if unsure, use another machine. | Vui lòng làm theo hướng dẫn trên màn hình để lấy ra nhẹ nhàng, đừng kéo mạnh; nếu không chắc thì chuyển sang máy bên cạnh. | Silakan ikuti petunjuk di layar untuk menariknya perlahan, jangan dipaksa; jika ragu, gunakan mesin sebelah. |
| ERR-16 | 印一半沒紙了 | 依螢幕補紙後可續印，或改用旁邊另一台重印。 | Refill to continue, or reprint on another machine. | Sau khi thêm giấy theo màn hình bạn có thể in tiếp, hoặc chuyển sang máy bên cạnh để in lại. | Setelah mengisi kertas sesuai layar bisa lanjut cetak, atau gunakan mesin di sebelahnya untuk cetak ulang. |
| ERR-17 | 螢幕觸控沒反應 | 請改用旁邊另一台機器操作。 | Use one of the other machines. | Quý khách hãy đổi sang dùng máy bên cạnh nhé. | Silakan gunakan mesin di sebelahnya. |
| ERR-18 | 機器一直轉沒動作 | 請稍候；若沒反應改用旁邊另一台，未完成不扣款。 | Wait; if nothing happens, use another machine—no charge. | Vui lòng đợi một chút; nếu không phản hồi thì chuyển sang máy bên cạnh, chưa hoàn thành thì không bị trừ tiền. | Mohon tunggu sebentar; jika tidak merespons, gunakan mesin sebelah, yang belum selesai tidak dikenai biaya. |
| ERR-19 | 印出來歪斜 | 文件或證件請對齊標示線；或改用旁邊另一台重印。 | Align to the marks, or reprint on another machine. | Với tài liệu hoặc giấy tờ, vui lòng căn theo vạch dấu; hoặc chuyển sang máy bên cạnh để in lại. | Untuk dokumen atau kartu, mohon luruskan ke garis penanda; atau gunakan mesin di sebelahnya untuk cetak ulang. |
| ERR-20 | 重複印了好幾張 | 請檢查份數設定，確認份數後再重印。 | Check the copy count and reprint after confirming. | Hãy kiểm tra cài đặt số bản, xác nhận số bản rồi in lại. | Periksa pengaturan jumlah salinan, konfirmasi lalu cetak ulang. |

---

## LOC — store_info｜店務 / 環境資訊（18）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| LOC-01 | 幾點營業 | 本店 24 小時營業、全年無休。 | We're open 24 hours, every day of the year. | Cửa hàng mở cửa 24 giờ, cả năm không nghỉ. | Kami buka 24 jam, setiap hari sepanjang tahun. |
| LOC-02 | 開到幾點 | 本店 24 小時營業，全天候開放。 | We're open 24 hours a day. | Cửa hàng mở cửa 24 giờ, suốt cả ngày. | Toko buka 24 jam sehari. |
| LOC-03 | 假日有開嗎 | 有，本店全年無休、24 小時營業。 | Yes—open 24 hours, every day, all year. | Có, cửa hàng mở cửa suốt cả năm, 24 giờ. | Ya, toko buka 24 jam, setiap hari, sepanjang tahun. |
| LOC-04 | 地址在哪 | 地址請參考門口告示或您的地圖定位。 | The address is on the door notice or your map app. | Vui lòng xem địa chỉ trên bảng thông báo ở cửa hoặc ứng dụng bản đồ của bạn. | Lihat alamat di pengumuman pintu atau aplikasi peta Anda. |
| LOC-05 | 怎麼去 / 在哪裡 | 位置請參考您手機的地圖定位。 | Please check your map app for the location. | Vui lòng xem vị trí trên ứng dụng bản đồ của điện thoại. | Silakan cek lokasi di aplikasi peta ponsel Anda. |
| LOC-06 | 有停車位嗎 | 不好意思，本店沒有提供停車位。 | Sorry—we don't have parking. | Xin lỗi, cửa hàng không có chỗ đậu xe ạ. | Maaf, toko ini tidak menyediakan tempat parkir. |
| LOC-07 | 可以停哪 | 本店沒有專用停車位，請利用周邊合法停車空間。 | We have no parking; please use nearby legal parking. | Cửa hàng không có chỗ đậu xe riêng, vui lòng dùng chỗ đậu xe hợp pháp gần đó. | Toko tidak punya parkir; silakan gunakan parkir legal di sekitar. |
| LOC-08 | 有廁所嗎 | 不好意思，本店是無人門市，沒有提供廁所與洗手設備。 | Sorry—this unmanned store has no restroom or handwashing. | Xin lỗi, đây là cửa hàng tự động không người, không có nhà vệ sinh và chỗ rửa tay. | Maaf, ini toko tanpa petugas, tidak tersedia toilet dan tempat cuci tangan. |
| LOC-09 | 可以洗手嗎 | 不好意思，本店沒有提供洗手設備。 | Sorry—no handwashing facilities here. | Xin lỗi, cửa hàng không có chỗ rửa tay. | Maaf, kami tidak menyediakan fasilitas cuci tangan. |
| LOC-10 | 有 wifi 嗎 | 店內掃碼連線僅用於傳送檔案到事務機，不提供一般上網；需上網請用手機行動網路。 | The in-store QR connection is only for sending files to the machine, not general internet—use mobile data for browsing. | Kết nối quét QR trong cửa hàng chỉ để gửi tệp tới máy, không dùng để vào mạng thông thường; cần lên mạng thì bạn dùng dữ liệu di động nhé. | Koneksi QR di toko hanya untuk mengirim file ke mesin, bukan untuk internet biasa; jika perlu internet, gunakan data seluler ya. |
| LOC-11 | 有冷氣嗎 | 環境相關以現場為準。 | Please refer to the on-site environment. | Về môi trường vui lòng xem tình hình tại chỗ. | Untuk lingkungan, mohon mengacu pada kondisi di tempat. |
| LOC-12 | 有幾台機器 | 本店有三台機器，可任選使用。 | There are three machines; use any of them. | Cửa hàng có ba máy, bạn có thể chọn dùng bất kỳ máy nào. | Ada tiga mesin; gunakan yang mana saja. |
| LOC-13 | 哪一台比較好 | 三台功能相同，任選一台即可；某台有狀況可換另一台。 | All three are the same; switch if one has an issue. | Ba máy có chức năng giống nhau, chọn máy nào cũng được; nếu một máy có vấn đề thì đổi sang máy khác. | Ketiganya sama; ganti jika satu bermasalah. |
| LOC-14 | 有監視器嗎 | 店內設有監視以維護安全，影像僅作安全用途。 | There's security monitoring for safety only. | Cửa hàng có lắp giám sát để đảm bảo an toàn, hình ảnh chỉ dùng cho mục đích an toàn. | Ada pemantauan keamanan hanya untuk keselamatan. |
| LOC-15 | 可以坐著休息嗎 | 本店為自助操作空間，沒有休息座位。 | This is a self-service space with no seating. | Cửa hàng là không gian tự phục vụ, không có chỗ ngồi nghỉ. | Ini ruang swalayan tanpa tempat duduk. |
| LOC-16 | 有賣文具嗎 | 不好意思，本店只提供列印、影印與掃描，不販售文具。 | Sorry—we only offer printing, copying, and scanning. | Xin lỗi, cửa hàng chỉ cung cấp in, photocopy và scan, không bán văn phòng phẩm. | Maaf, kami hanya menyediakan cetak, fotokopi, dan pindai. |
| LOC-17 | 可以換零錢嗎 | 不好意思，本店不提供換鈔，付款請用畫面顯示的方式。 | Sorry—no change service; pay via the on-screen methods. | Xin lỗi, cửa hàng không đổi tiền lẻ, vui lòng thanh toán theo cách hiển thị trên màn hình. | Maaf, toko ini tidak menyediakan penukaran uang, mohon bayar dengan cara yang tampil di layar. |
| LOC-18 | 有飲水機嗎 | 不好意思，本店沒有提供飲水設備。 | Sorry—no water facilities here. | Xin lỗi, cửa hàng không có nước uống. | Maaf, kami tidak menyediakan fasilitas air minum. |

---

## HLP — human_help｜需要協助（12）

> 無人門市：語音引導操作為主；不導真人。

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| HLP-01 | 有沒有人可以幫我 | 這是無人自助門市，我可以直接引導您操作，請告訴我您的需求。 | This is a self-service store—I can guide you; tell me what you need. | Đây là cửa hàng tự phục vụ không người, tôi có thể hướng dẫn bạn thao tác, hãy cho tôi biết bạn cần gì. | Ini toko swalayan tanpa staf, saya bisa memandu Anda; beri tahu apa yang Anda butuhkan. |
| HLP-02 | 哪裡有更多說明 | 機台螢幕都有操作指引，我也可以一步步引導您。 | The screen has guidance, and I can walk you through it. | Màn hình máy đều có hướng dẫn thao tác, tôi cũng có thể hướng dẫn bạn từng bước. | Layar mesin ada panduannya, dan saya juga bisa memandu Anda langkah demi langkah. |
| HLP-03 | 你們幾點營業 | 本店 24 小時營業、全年無休。 | We're open 24 hours, every day of the year. | Cửa hàng mở cửa 24 giờ, suốt cả năm không nghỉ. | Toko buka 24 jam, setiap hari sepanjang tahun. |
| HLP-04 | 現場都沒有店員嗎 | 對，這是無人門市，全部自助操作，我可以引導您。 | Yes—it's fully self-service, and I can help guide you. | Đúng vậy, đây là cửa hàng không người, hoàn toàn tự phục vụ, tôi có thể hướng dẫn bạn. | Ya, ini toko tanpa staf, sepenuhnya swalayan, dan saya bisa memandu Anda. |
| HLP-05 | 我不會用，可以教我嗎 | 沒問題，請告訴我您要列印、影印還是掃描，我一步步引導您。 | Of course—tell me what you need and I'll guide you step by step. | Không sao, hãy cho tôi biết bạn muốn in, photocopy hay quét, tôi sẽ hướng dẫn từng bước. | Tentu, beri tahu apakah Anda mau mencetak, fotokopi, atau pindai, saya pandu langkah demi langkah. |
| HLP-06 | 我遇到緊急狀況 | 若是火災、有人受傷等緊急狀況，請立即撥打 119 或 110。 | For a fire or injury, call 119 or 110 immediately. | Nếu có hỏa hoạn, có người bị thương hay tình huống khẩn cấp, vui lòng gọi ngay 119 hoặc 110. | Jika ada kebakaran, orang terluka, atau keadaan darurat, segera hubungi 119 atau 110. |
| HLP-07 | 廁所 / 洗手 / 其他問題 | 不好意思，本店是無人門市，沒有提供廁所與洗手設備；其他問題請參考現場告示。 | Sorry—no restroom or handwashing; for other questions see the in-store notices. | Xin lỗi, đây là cửa hàng không người, không có nhà vệ sinh và chỗ rửa tay; các câu hỏi khác xin xem bảng thông báo tại chỗ. | Maaf, ini toko tanpa petugas, tidak ada toilet dan fasilitas cuci tangan; untuk pertanyaan lain silakan lihat papan informasi di tempat. |
| HLP-08 | 我已經試很多次了 | 不好意思造成不便，您可以改用旁邊另一台機器，未完成不扣款。 | Sorry for the trouble—use another machine; unfinished jobs aren't charged. | Xin lỗi đã gây bất tiện, bạn có thể chuyển sang máy bên cạnh, chưa hoàn thành thì không bị trừ tiền. | Maaf atas ketidaknyamanannya, Anda bisa beralih ke mesin sebelah, yang belum selesai tidak dikenai biaya. |
| HLP-09 | 我看不懂螢幕 | 沒問題，告訴我您要列印、影印還是掃描，我一步步帶您。 | No problem—tell me what you need and I'll guide you. | Không sao, cho tôi biết bạn muốn in, photocopy hay quét, tôi sẽ hướng dẫn từng bước. | Tidak masalah, beri tahu apakah Anda mau mencetak, fotokopi, atau pindai, saya pandu langkah demi langkah. |
| HLP-10 | 卡在付款這一步 | 確認預覽後依畫面付款；卡住可重新操作或改用旁邊另一台。 | Pay per the screen after the preview; if stuck, retry or use another machine. | Sau khi xem trước, hãy thanh toán theo màn hình; nếu bị kẹt thì thao tác lại hoặc chuyển sang máy bên cạnh. | Setelah pratinjau, bayar sesuai layar; kalau tersangkut ulangi atau gunakan mesin di sebelahnya. |
| HLP-11 | 我東西不見了 | 請檢查出紙口與玻璃面板、送稿器是否留下原稿或成品。 | Check the output tray, glass, and feeder for your original or prints. | Hãy kiểm tra khay ra giấy, mặt kính và khay nạp giấy xem có còn bản gốc hoặc bản in không. | Periksa baki keluar kertas, kaca, dan pengumpan dokumen apakah ada dokumen asli atau hasil cetak Anda. |
| HLP-12 | 操作太複雜 | 別擔心，跟著螢幕步驟走，需要時我可以一步步引導您。 | Don't worry—follow the screen, and I can guide you step by step. | Đừng lo, hãy làm theo các bước trên màn hình, khi cần tôi có thể hướng dẫn bạn từng bước. | Jangan khawatir, ikuti langkah di layar, dan bila perlu saya bisa memandu Anda langkah demi langkah. |

---

## CMP — complaint｜客訴 / 抱怨（12）

> 過渡期：付款後沒印好 → 導重印不扣款；費用爭議 → 致歉＋保留交易紀錄＋告知線上申請即將開放。**不導真人、不承諾賠償。**

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| CMP-01 | 我被亂扣錢 | 不好意思造成困擾；目前現場無法直接處理扣款爭議，請先保留交易紀錄，線上退款申請即將開放。 | Sorry—charge disputes can't be handled on-site yet; keep your record, online refunds coming soon. | Xin lỗi vì sự bất tiện; hiện tại tranh chấp trừ tiền chưa thể xử lý tại chỗ, vui lòng giữ lại bản ghi giao dịch, đăng ký hoàn tiền trực tuyến sắp mở. | Maaf atas ketidaknyamanannya; sengketa penagihan belum bisa ditangani di tempat, simpan catatan transaksi Anda, pengajuan pengembalian dana online segera hadir. |
| CMP-02 | 我要退費 | 不好意思，若付款後沒印出來，可改用旁邊另一台重印，不扣款；線上退款申請即將開放。 | Sorry—if a paid job didn't print, reprint on another machine (no charge); online refunds coming soon. | Xin lỗi, nếu đã thanh toán mà không in ra, quý khách có thể in lại trên máy bên cạnh, không trừ tiền; đăng ký hoàn tiền trực tuyến sắp mở. | Maaf, jika sudah membayar tapi tidak tercetak, Anda bisa cetak ulang di mesin di sebelahnya tanpa biaya; pengajuan pengembalian dana online segera dibuka. |
| CMP-03 | 這台爛死了不能用 | 很抱歉造成不便，您可以直接改用旁邊另一台機器，未完成不扣款。 | Sorry—please use one of the other machines; unfinished jobs aren't charged. | Rất xin lỗi vì sự bất tiện, bạn có thể chuyển thẳng sang máy bên cạnh, chưa hoàn thành thì không bị trừ tiền. | Maaf atas ketidaknyamanannya, Anda bisa langsung beralih ke mesin sebelah, yang belum selesai tidak dikenai biaya. |
| CMP-04 | 印壞了你要賠我 | 很抱歉，若付款後沒印好，可改用旁邊另一台重印，不扣款；線上退款申請即將開放。 | Sorry—if a paid job printed badly, reprint on another machine (no charge); online refunds coming soon. | Rất xin lỗi, nếu đã thanh toán mà in không tốt, bạn có thể chuyển sang máy bên cạnh để in lại, không bị trừ tiền; tính năng yêu cầu hoàn tiền trực tuyến sắp mở. | Mohon maaf, jika sudah membayar tapi hasil cetak buruk, Anda bisa gunakan mesin di sebelahnya untuk cetak ulang tanpa biaya; pengajuan pengembalian dana online segera dibuka. |
| CMP-05 | 浪費我時間 | 很抱歉耽誤您的時間，您可以直接改用旁邊另一台機器，未完成不扣款。 | Sorry for the delay—use one of the other machines; unfinished jobs aren't charged. | Rất xin lỗi đã làm mất thời gian của quý khách, quý khách có thể đổi sang máy bên cạnh, chưa xong thì không trừ tiền. | Mohon maaf telah membuang waktu Anda, Anda bisa beralih ke mesin di sebelahnya, pekerjaan yang belum selesai tidak ditagih. |
| CMP-06 | 我要客訴 / 投訴 | 了解，您的意見對我們很重要；線上意見回報功能即將開放，屆時可留下意見。 | Understood—your feedback matters; an online channel is coming soon. | Đã hiểu, ý kiến của bạn rất quan trọng với chúng tôi; chức năng phản hồi ý kiến trực tuyến sắp mở, khi đó bạn có thể để lại ý kiến. | Mengerti, masukan Anda sangat berarti bagi kami; saluran masukan online segera hadir, nanti Anda bisa menyampaikan masukan. |
| CMP-07 | 我要找負責人 | 這是無人門市現場沒有專人；線上聯絡功能即將開放，屆時可留下聯絡方式。 | This is unmanned with no staff; an online contact channel is coming soon. | Đây là cửa hàng không người nên tại chỗ không có nhân viên; chức năng liên hệ trực tuyến sắp mở, khi đó bạn có thể để lại thông tin liên hệ. | Ini toko tanpa petugas di tempat; saluran kontak online segera hadir, nanti Anda bisa meninggalkan kontak. |
| CMP-08 | 你們服務很差 | 很抱歉讓您有不好的體驗，我們會持續改進；線上意見回報即將開放。 | Sorry for the poor experience—we'll improve; an online channel is coming soon. | Rất xin lỗi đã mang lại trải nghiệm không tốt, chúng tôi sẽ tiếp tục cải thiện; phản hồi ý kiến trực tuyến sắp mở. | Maaf atas pengalaman yang kurang baik, kami akan terus memperbaiki; saluran masukan online segera hadir. |
| CMP-09 | 等很久很煩 | 很抱歉久候，您可以改用旁邊另一台機器，未完成不扣款。 | Sorry for the wait—use one of the other machines; no charge for unfinished jobs. | Rất xin lỗi đã để bạn chờ lâu, bạn có thể chuyển sang máy bên cạnh, chưa hoàn thành thì không bị trừ tiền. | Maaf telah membuat Anda menunggu lama, Anda bisa beralih ke mesin sebelah, yang belum selesai tidak dikenai biaya. |
| CMP-10 | 機器很難用 | 抱歉造成不便，告訴我您卡在哪，我帶您操作。 | Sorry—tell me where you're stuck and I'll guide you. | Xin lỗi vì sự bất tiện, hãy cho tôi biết bạn đang vướng ở đâu, tôi sẽ hướng dẫn bạn thao tác. | Maaf atas ketidaknyamanannya, beri tahu di mana Anda tersangkut, saya akan memandu Anda. |
| CMP-11 | 我投訴都沒人理 | 本店為無人門市；線上意見回報功能即將開放，屆時可留言反映。 | This is unmanned; an online feedback channel is coming soon. | Cửa hàng này không có người trực; chức năng phản hồi ý kiến trực tuyến sắp mở, khi đó bạn có thể để lại lời nhắn phản ánh. | Toko ini tanpa petugas; saluran masukan online segera hadir, nanti Anda bisa meninggalkan pesan. |
| CMP-12 | 你們會偷看我檔案嗎 | 不會，檔案只在店內主機處理，完成後自動清除，不會上雲。 | No—files are processed in-store, cleared after, and never uploaded. | Không, tập tin chỉ được xử lý trên máy chủ trong cửa hàng, tự động xóa sau khi hoàn thành, không tải lên đám mây. | Tidak, file hanya diproses di mesin dalam toko, otomatis terhapus setelah selesai, tidak diunggah ke cloud. |

---

## PRIV — privacy｜隱私 / 資料安全（6）

| id | trigger | 中文引導（TTS） | English | Tiếng Việt | Bahasa Indonesia |
|---|---|---|---|---|---|
| PRIV-01 | 我的檔案安全嗎 | 檔案只暫存店內主機，列印後自動清除，不會上雲。 | Files are processed in-store and cleared after printing—never uploaded. | Tệp chỉ lưu tạm trên máy tại cửa hàng, tự động xóa sau khi in, không tải lên đám mây. | File hanya disimpan sementara di mesin toko, otomatis dihapus setelah dicetak, tidak diunggah ke cloud. |
| PRIV-02 | 掃描的會被留嗎 | 掃描檔完成寄送或存檔後即清除，不上雲。 | Scans are cleared after sending—never uploaded. | Tệp quét bị xóa sau khi gửi hoặc lưu xong, không tải lên đám mây. | File scan dihapus setelah dikirim atau disimpan, tidak diunggah ke cloud. |
| PRIV-03 | 會記錄我印什麼嗎 | 系統不保留您的檔案內容，列印後即清除。 | We don't keep your file content; it's cleared after printing. | Hệ thống không lưu nội dung tệp của bạn, xóa ngay sau khi in. | Sistem tidak menyimpan isi file Anda, langsung dihapus setelah dicetak. |
| PRIV-04 | 監視器會拍到我的檔案嗎 | 監視僅作環境安全用途，不針對您的檔案內容。 | Monitoring is for safety only, not your file content. | Giám sát chỉ dùng cho an toàn môi trường, không nhắm vào nội dung tệp của bạn. | Pemantauan hanya untuk keamanan lingkungan, bukan untuk isi file Anda. |
| PRIV-05 | 證件影印安全嗎 | 證件影像只在店內處理，完成後清除，不上雲。 | ID images are processed in-store and cleared—never uploaded. | Ảnh giấy tờ chỉ xử lý tại cửa hàng, xóa sau khi xong, không tải lên đám mây. | Gambar identitas hanya diproses di toko, dihapus setelah selesai, tidak diunggah ke cloud. |
| PRIV-06 | 個資會外洩嗎 | 您的檔案不上雲、完成即清除，請放心。 | Your files never go to the cloud and are cleared after use. | Tệp của bạn không tải lên đám mây, xóa ngay sau khi xong, xin yên tâm. | File Anda tidak diunggah ke cloud dan langsung dihapus setelah selesai, jangan khawatir. |

---

### 統計（v0.4）

| intent / 群組 | 句數 |
|---|---|---|---|
| SYS 系統句 | 4 |
| GEN 一般對話 | 16 |
| print_mobile 手機列印 | 30 |
| copy_id 證件影印 | 18 |
| copy_doc 一般影印 | 14 |
| scan 掃描 | 18 |
| advanced_func 進階功能 | 16 |
| supplies 紙張耗材 | 14 |
| payment 付款 | 22 |
| promo 優惠券 | 7 |
| invoice 發票收據 | 10 |
| machine_error 機台狀況 | 20 |
| store_info 店務資訊 | 18 |
| human_help 求助 | 12 |
| complaint 客訴 | 12 |
| privacy 隱私 | 6 |
| **合計** | **237** |

### 已確認的門市事實（v0.4.1）
- **營業時間：24 小時、全年無休** — LOC-01/02/03、HLP-03
- **停車：無停車位** — LOC-06/07
- **店內 WiFi：掃碼僅供傳檔到事務機，不提供一般上網** — LOC-10、PM-17
- **加值服務：不提供護貝 / 裁切 / 相片紙 / 照片沖印 / 裝訂 / 騎馬釘 / 打孔 / 海報 / 信封 / 特殊紙材**；紙張提供 A4、A3、80 磅優良紙 — FN-01/02/03/04/06/07/13、SUP-02/03
- **付款：多元電子支付（LINE Pay、信用卡）**，不收現金、不支援實體悠遊卡；低消 2 元；無法分開付款（每筆訂單一次付清）— PAY-02/03/04/05/06/15/18/19
- **檔案/列印：支援 PDF 與 Word/Excel/PPT 免轉檔直印、JPG/PNG**；單檔上限 150MB；掃描僅 Email（附檔上限 15MB）、不支援 USB；因著作權不支援影印書本；放大縮小僅少數固定倍率（最大 A3）— PM-03、SCN-02/03/04、CPY-03、各放大縮小條
- **發票：所有消費開立電子發票**（無紙本、不支援統編、無手機條碼自動捐贈公益；低消 2 元）— INV 全組、PAY-11/15/17
- **優惠：有優惠/折扣，以「優惠碼」(一串代碼)在手機操作頁面輸入折抵；機台無掃描功能** — PRO 全組

### 仍需店家確認 / 現場張貼
- （無）門市事實已全數確認；地址統一導向「地圖定位 / 門口告示」，不另填入。

### v0.4 擴充摘要
- 由 100 句擴到 **230 句**，新增 GEN(招呼互動)、CPY(一般影印)、FN(進階功能)、SUP(紙張耗材)、INV(發票)、LOC(店務環境)、PRIV(隱私) 七個常用會話群組，並補各類口語/台味變體。
- **收錄範圍限定 iPrintOS 無人門市相關**：與營業無關的閒聊（年齡/時間/天氣/純聊天）不收，無關發問由 GEN-16 拉回主題。
- 全程沿用既定決策：自助優先、不靠真人、退款過渡(1B)、三台機器、無廁所/洗手、檔案不上雲、永遠回最接近一句。
- 系統負擔評估見規劃文件 §13：句數對效能影響可忽略。
- **v0.4.2**：依門市規格修正既有事實（發票/紙張/付款/掃描/進階/放大縮小），並新增 **PRO（優惠券 / 優惠碼）** 群組 7 句，合計 237 句。