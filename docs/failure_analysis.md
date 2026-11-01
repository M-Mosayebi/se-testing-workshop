# تحلیل Failureهای تست Login

## Failure ۱: `test_empty_password` (TC-LOGIN-004)

**۱. انتظار در برابر واقعیت**
انتظار: پیام شامل `Password is required` باشد. واقعاً دیده شد: `Epic sadface: Password required` (کلمه‌ی «is» ندارد).

**۲. نوع failure: باگ اپ**
دلیل: Acceptance Criteria شماره ۴ صراحتاً متن `Password is required` را مشخص کرده و تست دقیقاً همین را چک می‌کند. پیام اپ با spec مغایرت دارد. هم‌چنین پیام نام‌گذاری مشابهِ `Username is required` را نقض می‌کند و ناسازگار است.

**۳. علت ریشه‌ای**
در اسکریپت اپ، این خط:
```js
if (pass === "") return showError("Password required");
```
یک typo/غلط املایی (حذف «is») است. خط قبلی آن (`"Username is required"`) درست است.

**۴. پیشنهاد اصلاح**
فایل اپ (HTML/JS)، همان خط:
```js
if (pass === "") return showError("Password is required");
```
نیازی به تغییر تست نیست.

**۵. شدت: Low**
عملکرد درست است (کاربر وارد نمی‌شود و خطا می‌بیند) ولی متن پیام با spec نمی‌خواند. تأثیر روی کاربر کم است، اما چون مغایرت مستقیم با AC است، باید اصلاح شود.

---

## Failure ۲: `test_locked_out_user` (TC-LOGIN-005)

**۱. انتظار در برابر واقعیت**
انتظار: پیام شامل `locked out` باشد. واقعاً دیده شد: `Username and password do not match any user in this service`.

**۲. نوع failure: باگ اپ**
دلیل: AC شماره ۵ می‌گوید کاربر قفل‌شده باید پیام مشخصی ببیند که قفل شده است. اپ اصلاً مفهوم «locked out» را پیاده‌سازی نکرده و این کاربر را مثل یک کاربر ناشناس رد می‌کند. تست درست و منطبق با spec است.

**۳. علت ریشه‌ای**
در اسکریپت اپ:
```js
const VALID_USERS = ["standard_user", "problem_user"];
```
`locked_out_user` در این لیست نیست، پس شرط `VALID_USERS.includes(user) && pass === PASSWORD` برایش false می‌شود و به پیام عمومی `Username and password do not match...` می‌رسد. هیچ شاخه‌ی جداگانه‌ای برای کاربر قفل‌شده وجود ندارد.

**۴. پیشنهاد اصلاح**
فایل اپ: تعریف لیست کاربران قفل‌شده و بررسی آن قبل از شرط اعتبارسنجی عادی:
```js
const LOCKED_USERS = ["locked_out_user"];
...
if (LOCKED_USERS.includes(user) && pass === PASSWORD)
  return showError("Sorry, this user has been locked out.");
```
نکته: اگر بخواهید برای رمز اشتباه هم همین پیام بیاید، شرط `pass === PASSWORD` را بردارید (از نظر امنیتی بهتر است برای رمز اشتباه، پیام عمومی بماند تا وضعیت قفل بودن حساب لو نرود). این تصمیم طراحی است و باید با تیم محصول هماهنگ شود. تست نیاز به تغییر ندارد.

**۵. شدت: High**
یک ویژگی کامل از AC (مسدودسازی کاربر قفل‌شده با پیام مناسب) پیاده‌سازی نشده است. کاربر قفل‌شده دلیل مشکل را نمی‌فهمد و ممکن است بارها تلاش کند یا با پشتیبانی تماس بگیرد. یک نکته‌ی مثبت: دسترسی واقعی داده نمی‌شود (login رد می‌شود)، پس مشکل امنیتی نیست و فقط UX/عملکردی است. شدت High به خاطر پیاده‌نشدن کامل یک AC است.

---

## نکات تکمیلی و موارد نامطمئن

- **محیط**: هشدار `PytestRemovedIn10Warning` ربطی به این دو failure ندارد (مربوط به fixture از نوع session-scoped در plugin است) و باید جدا پیگیری شود. من به کد `LoginPage` دسترسی ندارم، پس درباره‌ی locatorها فقط از روی لاگ نتیجه می‌گیرم که `error_message` درست resolve می‌شود (`[data-test='error']`).
- **پوشش AC**: AC شماره ۲ (رمز اشتباه) با پارامتر `standard_user/wrong_pass` پوشش داده شده و پاس است. موارد `STANDARD_USER` و `SECRET_SAUCE` هم پاس شدند، چون اپ مقایسه‌ی case-sensitive دارد. اما spec در مورد case-sensitivity چیزی نگفته و این فرض تست‌هاست (TC-008/009)، پس مطمئن نیستم که این رفتار الزام رسمی باشد.
- **ضعف احتمالی تست**: `test_invalid_credentials` فقط وجود متن خطا را چک می‌کند، نه «ماندن در صفحه‌ی login» که بخشی از AC شماره ۲ است. پیشنهاد: افزودن `expect(page).not_to_have_url(...inventory)` یا چک نمایان‌بودن فرم login.
- **تست ناقص**: TC-LOGIN-001 فقط URL و عنوان را چک می‌کند و مورد دیگری (مثل نمایش لیست محصولات) ندارد، ولی با AC شماره ۱ کفایت می‌کند.

